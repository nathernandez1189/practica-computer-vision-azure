"""Validación de entradas y registros sin credenciales."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_paths(folder: Path) -> list[Path]:
    if not folder.is_dir():
        raise ValueError(f"No existe la carpeta de imágenes: {folder}")
    paths = sorted(p for p in folder.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
    if not paths:
        raise ValueError("La carpeta no contiene imágenes PNG o JPEG.")
    if len(paths) > 10:
        raise ValueError("Use como máximo diez imágenes por ejecución.")
    for path in paths:
        if not path.is_file() or path.stat().st_size > 10 * 1024 * 1024:
            raise ValueError(f"Archivo no válido o mayor que 10 MiB: {path.name}")
    return paths


def save_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
