"""Cliente REST de Azure OpenAI v1; secretos solo mediante variables de entorno."""

import base64
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .common import image_paths, save_json, sha256, timestamp

INSTRUCTIONS = (
    "Ayuda a identificar hardware informático antiguo. Responde en español. "
    "Distingue lo que se ve de las inferencias. No inventes marca, modelo, "
    "año exacto ni especificaciones que no se puedan confirmar en la imagen."
)
PROMPT = "¿Qué puedes decir de este dispositivo? Describe sus rasgos visibles, función probable y limitaciones de la identificación."


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Una redirección nunca debe reenviar la credencial a otro servidor.
        return None


def configuration() -> tuple[str, str]:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    parts = urlparse(endpoint)
    if (parts.scheme != "https" or not parts.hostname or
        not parts.hostname.endswith(".openai.azure.com") or
        parts.username or parts.password or parts.query or parts.fragment or
        parts.port not in (None, 443) or parts.path not in ("", "/openai/v1")):
        raise ValueError("Configure AZURE_OPENAI_ENDPOINT con la URL HTTPS de su recurso .openai.azure.com.")
    if not key:
        raise ValueError("Falta AZURE_OPENAI_API_KEY; no la escriba en el código ni en Git.")
    base = endpoint if parts.path == "/openai/v1" else endpoint + "/openai/v1"
    return base, key


def post(operation: str, payload: dict) -> dict:
    base, key = configuration()
    request = Request(base + "/" + operation,
                      data=json.dumps(payload).encode("utf-8"),
                      headers={"Content-Type": "application/json", "api-key": key}, method="POST")
    try:
        with build_opener(NoRedirect()).open(request, timeout=180) as response:
            return json.load(response)
    except HTTPError as exc:
        # El cuerpo de error puede contener información del recurso; no se registra.
        raise RuntimeError(f"Azure devolvió HTTP {exc.code}. Revise permisos, cuota y despliegue.") from None
    except (URLError, TimeoutError):
        raise RuntimeError("No se pudo obtener la respuesta de Azure; revise la conexión antes de repetir.") from None


def build_payload(path: Path, deployment: str) -> dict:
    raw = path.read_bytes()
    if not raw or len(raw) > 10 * 1024 * 1024:
        raise ValueError("La imagen debe tener entre 1 byte y 10 MiB.")
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        mime = "image/png"
    elif raw.startswith(b"\xff\xd8\xff"):
        mime = "image/jpeg"
    else:
        raise ValueError(f"Contenido PNG/JPEG no válido: {path.name}")
    encoded = base64.b64encode(raw).decode("ascii")
    return {
        "model": deployment, "instructions": INSTRUCTIONS,
        "max_output_tokens": 1800, "store": False,
        "input": [{"role": "user", "content": [
            {"type": "input_text", "text": PROMPT},
            {"type": "input_image", "image_url": f"data:{mime};base64,{encoded}", "detail": "low"},
        ]}],
    }


def response_text(response: dict) -> str:
    if response.get("status") != "completed":
        raise RuntimeError("Azure no completó la respuesta. No se registra como evidencia exitosa.")
    texts = [item["text"] for message in response.get("output", [])
             if message.get("type") == "message"
             for item in message.get("content", []) if item.get("type") == "output_text"]
    if not texts:
        raise RuntimeError("Azure devolvió una respuesta sin texto de análisis.")
    return "\n".join(texts)


def analyze(folder: Path, output: Path) -> dict:
    configuration()
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    if not deployment:
        raise ValueError("Falta AZURE_OPENAI_DEPLOYMENT.")
    paths = image_paths(folder)
    # Valida todos los archivos antes de realizar una petición con coste.
    payloads = [build_payload(path, deployment) for path in paths]
    result = {"estado": "en_progreso", "fecha_utc": timestamp(), "motor": "Azure OpenAI Responses v1",
              "despliegue": deployment, "instrucciones": INSTRUCTIONS, "pregunta": PROMPT, "resultados": []}
    for path, payload in zip(paths, payloads):
        response = post("responses", payload)
        result["resultados"].append({
            "imagen": path.name, "sha256": sha256(path), "respuesta": response_text(response),
            "modelo": response.get("model"), "id_respuesta": response.get("id"),
            "uso_tokens": response.get("usage"),
        })
        # Conserva avances si falla una petición posterior; no se reintenta automáticamente.
        save_json(output, result)
    result["estado"] = "ejecutado"
    save_json(output, result)
    return result


def generate(output: Path) -> dict:
    configuration()
    deployment = os.environ.get("AZURE_IMAGE_DEPLOYMENT", "")
    if not deployment:
        raise ValueError("Falta AZURE_IMAGE_DEPLOYMENT (modelo GPT Image disponible en su suscripción).")
    prompt = "Un computador personal antiguo con monitor CRT, teclado y ratón sobre una mesa, sin marcas ni texto, estilo fotografía de catálogo."
    response = post("images/generations", {"model": deployment, "prompt": prompt,
                                           "n": 1, "size": "1024x1024", "quality": "low"})
    data = response.get("data", [])
    if not data or not data[0].get("b64_json"):
        raise RuntimeError("El despliegue no devolvió una imagen en base64.")
    raw = base64.b64decode(data[0]["b64_json"], validate=True)
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("La imagen generada no es PNG; no se guardó con una extensión incorrecta.")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(raw)
    result = {"estado": "ejecutado", "fecha_utc": timestamp(), "motor": "Azure OpenAI Images v1",
              "despliegue": deployment, "prompt": prompt, "archivo": output.name,
              "sha256": sha256(output), "uso": response.get("usage")}
    save_json(output.with_suffix(".json"), result)
    return result
