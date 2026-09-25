# Metodología y reproducción

## Correspondencia con la actividad

Se consultó el módulo el 24 de septiembre de 2026, hora de Colombia. Su enlace de ejercicio conduce a [Explore computer vision](https://microsoftlearning.github.io/mslearn-ai-concepts/Instructions/exercises/05-vision.html), que propone un Chat Playground con clasificación visual y conversación. El [adicional](https://microsoftlearning.github.io/mslearn-ai-fundamentals/Instructions/Exercises/05a-image-analysis.html) usa Microsoft Foundry.

La reproducción local implementa únicamente la etapa de clasificación con MobileNetV2 en TorchVision. Comparte arquitectura con la descrita en el ejercicio, pero no se afirma identidad de pesos, preprocesamiento o resultados con el modelo del navegador. Tampoco incluye inferencia de Phi. La ejecución local no acredita la realización de la conversación en el portal ni el aprobado de Microsoft Learn.

## Datos y trazabilidad

Las imágenes proceden de los archivos oficiales enlazados por Microsoft. El archivo del módulo contiene cinco imágenes; el del adicional contiene las tres primeras, verificadas byte a byte. [El manifiesto](../datos/manifiesto.json) conserva direcciones de origen, tamaños y SHA-256. Se conserva la [licencia MIT de Microsoft](../licencias/Microsoft-MIT.txt), obtenida del repositorio de origen. No se incorporan imágenes personales.

## Entorno

Python 3.11; versiones directas fijadas en `requirements.txt`. Para revisar la ejecución original, consulte las versiones, los pesos, su huella, el preprocesamiento y las dimensiones de entrada en [clasificacion-local.json](../evidencias/clasificacion-local.json). Las dependencias transitivas del entorno original constan en [entorno.txt](../evidencias/entorno.txt).

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export PYTHONPATH=src
python -m vision_lab local
python -m vision_lab filtros
python -m unittest discover -s tests -v
```

En Windows, la activación es `.venv\Scripts\Activate.ps1` y la variable se establece con `$env:PYTHONPATH="src"` en PowerShell. Ejecute los comandos desde la raíz del repositorio.

La primera clasificación descarga aproximadamente 14 MB de pesos desde PyTorch y los guarda en `.cache/`. Las siguientes ejecuciones reutilizan esa copia. El modelo se ejecuta en CPU. Si Python de Homebrew no encuentra certificados en macOS, puede usar el almacén del sistema: `export SSL_CERT_FILE=/etc/ssl/cert.pem`. No se debe desactivar la validación TLS.

## Procedimiento local

1. Validar la carpeta y ordenar los archivos por nombre.
2. Corregir la orientación EXIF y convertir cada imagen a RGB.
3. Aplicar el preprocesamiento de `MobileNet_V2_Weights.IMAGENET1K_V2`.
4. Ejecutar el modelo en modo evaluación, sin gradientes.
5. Calcular softmax sobre las 1.000 clases y registrar las cinco primeras.
6. Guardar las huellas de las entradas y de los pesos para poder contrastar la ejecución.

Los resultados nuevos se guardan en `resultados/`, excluido de Git. Las evidencias publicadas son una captura de la ejecución original y no se sobrescriben con los comandos anteriores. Para guardar una nueva evidencia explícita se utiliza `--salida ruta/archivo.json`.

## Verificación

Las pruebas comprueban los datos, el cálculo del filtro, la construcción de la solicitud de Azure, la validación de destinos y el manejo de respuestas incompletas. Las pruebas del cliente Azure usan respuestas simuladas identificadas como tales; no consumen crédito ni demuestran ejecución en la nube. El flujo de GitHub Actions comprueba estos mismos casos. La inferencia local se ejecutó por separado y quedó registrada en JSON.
