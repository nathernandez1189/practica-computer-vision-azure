# Práctica de Computer Vision en Azure

Desarrollo académico del módulo **Introducción a los conceptos de computer vision** de Microsoft Learn: clasificación de imágenes de hardware, procesamiento mediante filtros y preparación del análisis multimodal en Azure.

**Integrantes**

- Miguel Angel Diuza
- Juan Ospina Tenorio
- Natalia Hernandez Piedrahita

## Estado de la entrega

| Componente | Estado | Evidencia |
|---|---|---|
| Fundamentos: tareas de visión, filtros, CNN, ViT y generación | Documentado | [Fundamentos](docs/fundamentos.md) |
| Clasificación local de las cinco imágenes oficiales | Ejecutado | [Resultados originales](evidencias/clasificacion-local.json) |
| Experimento numérico del filtro Laplaciano | Ejecutado | [Matriz de resultados](evidencias/filtro-laplaciano.json) |
| Comprobaciones automatizadas | 14 pruebas correctas | [Registro de validación](evidencias/pruebas.txt) |
| Conversación del ejercicio en Chat Playground | Pendiente de ejecución en el portal | [Alcance de la reproducción](docs/metodologia.md) |
| Análisis y generación en Microsoft Foundry | Cliente preparado; ejecución pendiente | [Procedimiento de Azure](docs/azure.md) |
| Aprobado del módulo en el perfil Microsoft Learn | No acreditado en esta entrega | La evaluación se realiza en la cuenta personal |

La clasificación local usa MobileNetV2 de TorchVision y reproduce la etapa de reconocimiento visual. **No sustituye la conversación completa del portal ni acredita una ejecución de Azure.** El estado exacto y las limitaciones se mantienen explícitos para facilitar la evaluación.

## Resultados de clasificación

| Imagen oficial | Referencia visual¹ | Primera clase del modelo | Puntuación² |
|---|---|---|---:|
| [image_01.png](datos/imagenes/image_01.png) | Computador de escritorio | `desktop computer` | 49,71 % |
| [image_02.png](datos/imagenes/image_02.png) | Ratón con cable | `mouse` | 4,30 % |
| [image_03.png](datos/imagenes/image_03.png) | Módem externo aparente | `modem` | 14,14 % |
| [image_04.png](datos/imagenes/image_04.png) | Disco duro abierto | `hard disc` | 96,74 % |
| [image_05.png](datos/imagenes/image_05.png) | Computador portátil | `notebook` | 24,05 % |

¹ Referencia obtenida mediante inspección visual asistida; no es una etiqueta oficial de Microsoft.
² Puntuación softmax entre 1.000 clases, no exactitud del modelo ni certeza calibrada.

Las primeras etiquetas resultan semánticamente coherentes con las referencias visuales en estos cinco ejemplos. El ratón presenta una distribución muy dispersa; el disco duro concentra una puntuación mucho mayor. No se infiere rendimiento general a partir de esta muestra. [Análisis de resultados](docs/resultados.md).

## Ejecutar la práctica

Requisitos: Python 3.11, conexión para instalar dependencias y descargar los pesos en la primera ejecución.

```bash
git clone https://github.com/nathernandez1189/practica-computer-vision-azure.git
cd practica-computer-vision-azure
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export PYTHONPATH=src
python -m vision_lab local
python -m vision_lab filtros
python -m unittest discover -s tests -v
```

Los resultados nuevos se guardan en `resultados/`. Para Azure se deben configurar las variables de `.env.example` siguiendo [estas instrucciones](docs/azure.md). La clasificación local no requiere una cuenta de Azure. Consulte [metodología](docs/metodologia.md) para Windows, certificados, pesos y trazabilidad.

## Contenido del repositorio

```text
src/vision_lab/    Clasificación, filtros y cliente Azure
datos/imagenes/   Cinco imágenes oficiales del laboratorio
datos/manifiesto.json
docs/             Fundamentos, metodología, resultados y uso de Azure
evidencias/       Resultados reales y registro de validación
tests/            Comprobaciones automatizadas
licencias/        Licencia de los materiales de Microsoft
```

Las claves, cachés, entornos virtuales y salidas de nuevas ejecuciones están excluidos de Git. Las pruebas de integración del cliente usan respuestas simuladas y se distinguen de las evidencias de ejecución real.

## Fuentes

- [Módulo asignado de Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/).
- [Ejercicio enlazado actualmente por el módulo](https://microsoftlearning.github.io/mslearn-ai-concepts/Instructions/exercises/05-vision.html).
- [Ejercicio adicional de Microsoft Foundry](https://microsoftlearning.github.io/mslearn-ai-fundamentals/Instructions/Exercises/05a-image-analysis.html).
- [MobileNetV2 en TorchVision](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.mobilenet_v2.html).

Consulta y ejecución local: **24 de septiembre de 2026, Colombia**. Los registros utilizan fecha y hora UTC. Los enlaces educativos pueden cambiar; se describe la versión consultada. Los materiales de Microsoft conservan su [licencia original](licencias/Microsoft-MIT.txt).
