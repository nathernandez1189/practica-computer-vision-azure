"""Clasificación real en CPU con MobileNetV2 de TorchVision.

Reproduce la etapa de clasificación, no la conversación Phi del portal.
"""

import platform
import time
from pathlib import Path

from .common import image_paths, save_json, sha256, timestamp


def classify(folder: Path, output: Path) -> dict:
    import torch
    import torchvision
    from PIL import Image, ImageOps
    from torchvision.models import MobileNet_V2_Weights, mobilenet_v2

    paths = image_paths(folder)
    torch.set_num_threads(2)
    torch.manual_seed(0)
    # Evita guardar pesos y cachés dentro del directorio de usuario o en Git.
    torch.hub.set_dir(str(Path(".cache") / "torch"))
    weights = MobileNet_V2_Weights.IMAGENET1K_V2
    model = mobilenet_v2(weights=weights).cpu().eval()
    transform = weights.transforms()
    rows = []
    for path in paths:
        with Image.open(path) as original:
            original.load()
            rgb = ImageOps.exif_transpose(original).convert("RGB")
            dimensions = list(rgb.size)
            tensor = transform(rgb).unsqueeze(0)
        started = time.perf_counter()
        with torch.inference_mode():
            probabilities = model(tensor)[0].softmax(dim=0)
            scores, indices = probabilities.topk(5)
        rows.append({
            "imagen": path.name,
            "sha256": sha256(path),
            "dimensiones_ancho_alto": dimensions,
            "latencia_ms": round((time.perf_counter() - started) * 1000, 3),
            "suma_probabilidades_1000_clases": float(probabilities.sum()),
            "top5": [
                {"clase": weights.meta["categories"][int(index)], "puntuacion": float(score)}
                for score, index in zip(scores, indices)
            ],
        })
    checkpoint = Path(torch.hub.get_dir()) / "checkpoints" / weights.url.rsplit("/", 1)[-1]
    result = {
        "estado": "ejecutado",
        "fecha_utc": timestamp(),
        "motor": "TorchVision / CPU",
        "modelo": "MobileNetV2",
        "pesos": weights.name,
        "pesos_url": weights.url,
        "pesos_sha256": sha256(checkpoint),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torchvision": torchvision.__version__,
        "preprocesamiento": str(transform),
        "alcance": "Clasificación local; no es ejecución de Chat Playground ni de Azure.",
        "resultados": rows,
    }
    save_json(output, result)
    return result
