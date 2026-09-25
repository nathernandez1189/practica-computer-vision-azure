import base64
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from vision_lab.azure import analyze, build_payload, configuration, response_text
from vision_lab.common import image_paths, sha256
from vision_lab.filters import convolve_valid, experiment

ROOT = Path(__file__).resolve().parents[1]


class FilterTests(unittest.TestCase):
    def test_microsoft_example_preserves_signed_values(self):
        with tempfile.TemporaryDirectory() as folder:
            result = experiment(Path(folder) / "filter.json")
        values = result["salida_sin_relleno_5x5"]
        self.assertEqual(values[0][:2], [-255, -510])
        self.assertEqual(values[2][2], 0)
        self.assertEqual((len(values), len(values[0])), (5, 5))
        self.assertTrue(all(0 <= v <= 255 for row in result["salida_recortada_0_255"] for v in row))

    def test_asymmetric_kernel_is_convolution_not_correlation(self):
        self.assertEqual(convolve_valid([[1, 2], [3, 4]], [[1, 0], [0, 0]]), [[4]])

    def test_invalid_matrices(self):
        for image, kernel in [([], [[1]]), ([[1], [1, 2]], [[1]]), ([[1]], [[1, 1]])]:
            with self.subTest(image=image, kernel=kernel), self.assertRaises(ValueError):
                convolve_valid(image, kernel)


class AzureTests(unittest.TestCase):
    def test_payload_contains_actual_image(self):
        path = ROOT / "datos/imagenes/image_01.png"
        payload = build_payload(path, "lab")
        content = payload["input"][0]["content"]
        self.assertEqual(base64.b64decode(content[1]["image_url"].split(",", 1)[1]), path.read_bytes())
        self.assertFalse(payload["store"])
        self.assertNotIn("api_key", payload)
        self.assertEqual(payload["model"], "lab")

    def test_rejects_disguised_non_image(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "fake.png"
            path.write_text("esto no es una imagen")
            with self.assertRaises(ValueError):
                build_payload(path, "lab")

    def test_endpoint_normalization(self):
        for endpoint in ["https://example.openai.azure.com/", "https://example.openai.azure.com/openai/v1/"]:
            with patch.dict(os.environ, {"AZURE_OPENAI_ENDPOINT": endpoint, "AZURE_OPENAI_API_KEY": "test-only"}, clear=True):
                self.assertEqual(configuration()[0], "https://example.openai.azure.com/openai/v1")

    def test_rejects_unsafe_endpoints_before_sending_key(self):
        for endpoint in ["http://example.openai.azure.com", "https://example.org", "https://example.openai.azure.com.attacker.org", "https://user:pass@example.openai.azure.com", "https://example.openai.azure.com?x=1"]:
            with self.subTest(endpoint=endpoint), patch.dict(os.environ, {"AZURE_OPENAI_ENDPOINT": endpoint, "AZURE_OPENAI_API_KEY": "test-only"}, clear=True):
                with self.assertRaises(ValueError):
                    configuration()

    def test_missing_key(self):
        with patch.dict(os.environ, {"AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com"}, clear=True):
            with self.assertRaises(ValueError):
                configuration()

    def test_incomplete_or_empty_response_is_not_success(self):
        for response in [{"status": "incomplete"}, {"status": "completed", "output": []}]:
            with self.subTest(response=response), self.assertRaises(RuntimeError):
                response_text(response)

    def test_extracts_only_output_text(self):
        self.assertEqual(response_text({"status": "completed", "output": [
            {"type": "reasoning", "content": [{"type": "output_text", "text": "ignored"}]},
            {"type": "message", "content": [{"type": "output_text", "text": "Ratón"}]},
        ]}), "Ratón")

    def test_preserves_partial_results_without_claiming_completion(self):
        response = {"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": "prueba simulada"}]}]}
        with tempfile.TemporaryDirectory() as folder, patch("vision_lab.azure.configuration", return_value=("endpoint", "key")), patch.dict(os.environ, {"AZURE_OPENAI_DEPLOYMENT": "test-only"}), patch("vision_lab.azure.post", side_effect=[response, RuntimeError("fallo simulado")]):
            output = Path(folder) / "azure.json"
            with self.assertRaises(RuntimeError):
                analyze(ROOT / "datos/imagenes", output)
            saved = json.loads(output.read_text())
            self.assertEqual(saved["estado"], "en_progreso")
            self.assertEqual(len(saved["resultados"]), 1)


class DataTests(unittest.TestCase):
    def test_official_images_match_manifest(self):
        manifest = json.loads((ROOT / "datos/manifiesto.json").read_text())
        for item in manifest["imagenes"]:
            self.assertEqual(sha256(ROOT / "datos/imagenes" / item["archivo"]), item["sha256"])

    def test_empty_folder_is_error(self):
        with tempfile.TemporaryDirectory() as folder, self.assertRaises(ValueError):
            image_paths(Path(folder))

    def test_local_evidence_if_present(self):
        evidence = ROOT / "evidencias/clasificacion-local.json"
        if not evidence.exists():
            self.skipTest("Todavía no existe evidencia local.")
        result = json.loads(evidence.read_text())
        self.assertEqual(result["estado"], "ejecutado")
        self.assertEqual(len(result["resultados"]), 5)
        for row in result["resultados"]:
            self.assertEqual(row["sha256"], sha256(ROOT / "datos/imagenes" / row["imagen"]))
            self.assertAlmostEqual(row["suma_probabilidades_1000_clases"], 1, places=5)
            scores = [r["puntuacion"] for r in row["top5"]]
            self.assertEqual(len(scores), 5)
            self.assertEqual(scores, sorted(scores, reverse=True))
            self.assertTrue(all(0 <= x <= 1 for x in scores))


if __name__ == "__main__":
    unittest.main()
