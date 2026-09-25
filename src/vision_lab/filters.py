"""Ejemplo numérico del filtro Laplaciano presentado en Microsoft Learn."""

from pathlib import Path
from .common import save_json


def convolve_valid(image: list[list[int]], kernel: list[list[int]]) -> list[list[int]]:
    if not image or not image[0] or any(len(row) != len(image[0]) for row in image):
        raise ValueError("La imagen debe ser una matriz rectangular no vacía.")
    if not kernel or not kernel[0] or any(len(row) != len(kernel[0]) for row in kernel):
        raise ValueError("El kernel debe ser una matriz rectangular no vacía.")
    h, w, kh, kw = len(image), len(image[0]), len(kernel), len(kernel[0])
    if kh > h or kw > w:
        raise ValueError("El kernel no puede superar las dimensiones de la imagen.")
    # Convolución matemática: invierte el kernel; el Laplaciano es simétrico.
    return [[sum(image[y + j][x + i] * kernel[kh - 1 - j][kw - 1 - i]
                 for j in range(kh) for i in range(kw))
             for x in range(w - kw + 1)] for y in range(h - kh + 1)]


def experiment(output: Path) -> dict:
    image = [[255 if 2 <= y <= 4 and 2 <= x <= 4 else 0 for x in range(7)] for y in range(7)]
    kernel = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    filtered = convolve_valid(image, kernel)
    result = {
        "estado": "ejecutado", "imagen_7x7": image, "kernel_3x3": kernel,
        "salida_sin_relleno_5x5": filtered,
        "salida_recortada_0_255": [[min(255, max(0, v)) for v in row] for row in filtered],
        "interpretacion": "Los cambios locales producen respuestas altas en el contorno; el centro uniforme produce 0.",
    }
    save_json(output, result)
    return result
