import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Práctica de Computer Vision: clasificación, filtros y Azure.")
    parser.add_argument("modo", choices=["local", "filtros", "azure", "generar"])
    parser.add_argument("--imagenes", type=Path, default=Path("datos/imagenes"))
    parser.add_argument("--salida", type=Path, help="Archivo de salida; por defecto se guarda en resultados/.")
    args = parser.parse_args()
    output = args.salida or Path("resultados") / (args.modo + (".png" if args.modo == "generar" else ".json"))
    try:
        if args.modo == "local":
            from .local import classify
            result = classify(args.imagenes, output)
        elif args.modo == "filtros":
            from .filters import experiment
            result = experiment(output)
        elif args.modo == "azure":
            from .azure import analyze
            result = analyze(args.imagenes, output)
        else:
            from .azure import generate
            result = generate(output)
    except (ValueError, RuntimeError, OSError, ImportError) as exc:
        print(f"No se completó la ejecución: {exc}", file=sys.stderr)
        return 1
    print(f"Estado: {result['estado']}. Resultado guardado en {output}")
    for row in result.get("resultados", []):
        if "top5" in row:
            first = row["top5"][0]
            print(f"{row['imagen']}: {first['clase']} ({first['puntuacion']:.2%})")
        else:
            print(f"{row['imagen']}: análisis recibido de Azure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
