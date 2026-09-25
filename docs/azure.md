# Ejercicio adicional en Microsoft Foundry

El [ejercicio oficial](https://microsoftlearning.github.io/mslearn-ai-fundamentals/Instructions/Exercises/05a-image-analysis.html) propone analizar imágenes de hardware y explorar la generación visual. Este repositorio incluye un cliente de análisis con Azure OpenAI Responses v1 y un cliente de generación compatible con GPT Image. El estado de ejecución se declara en el README y en las evidencias; disponer del código no acredita una llamada al servicio.

## Configuración del recurso

Se necesita una suscripción habilitada, un recurso compatible con Azure OpenAI y un despliegue multimodal. El modelo propuesto por el laboratorio es `gpt-5-mini`. La región y el tipo de despliegue deben estar permitidos tanto por las políticas de la suscripción como por la disponibilidad y cuota del modelo. No utilice capacidad aprovisionada para esta prueba breve sin revisar sus costes.

En Microsoft Foundry, cree o seleccione un proyecto, despliegue el modelo y obtenga el endpoint y la clave desde su recurso. Cree `.env` a partir de `.env.example` y complete los valores localmente. Nunca copie las claves al README, a capturas de pantalla o a archivos versionados.

En macOS/Linux, después de editar `.env`:

```bash
source .venv/bin/activate
set -a
source .env
set +a
export PYTHONPATH=src
python -m vision_lab azure
```

La ejecución envía las cinco imágenes incluidas. Las tres primeras coinciden con los datos del adicional y las otras dos amplían la comparación. Puede usar `--imagenes carpeta` para escoger otro conjunto de hasta diez archivos.

El cliente envía los bytes en base64 junto con una pregunta, limita la salida a 1.800 tokens por solicitud y utiliza `store: false`. Esta opción no implica ausencia absoluta de tratamiento o retención de datos por Azure. El registro local contiene las respuestas, identificadores, modelo, tokens y huellas de las imágenes; no guarda la clave ni el endpoint. [Referencia de Azure Responses](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses?view=foundry-classic), [entrada de imágenes](https://developers.openai.com/api/docs/guides/images-vision).

## Revisión de respuestas

Contraste los objetos mencionados con la imagen. Separe los rasgos visibles de las inferencias históricas o técnicas. No tome una descripción verosímil como prueba de marca o modelo. Compare especialmente el ratón y el módem con las puntuaciones locales, que presentan mayor ambigüedad.

## Generación de una imagen

Con un despliegue GPT Image compatible y autorizado en `AZURE_IMAGE_DEPLOYMENT`:

```bash
python -m vision_lab generar
```

Se solicita una única imagen de 1.024 × 1.024 en calidad baja. El cliente guarda el PNG y un registro de su origen. Si solo se dispone de FLUX u otro modelo, utilice el playground correspondiente: este cliente no presume compatibilidad con esos proveedores. La sección de vídeo del laboratorio está condicionada a disponibilidad y no forma parte del cliente incluido.

## Coste y cierre

Las llamadas pueden consumir crédito. El límite de archivos y tokens reduce el alcance de cada ejecución, pero no es un tope de facturación de Azure. No hay reintentos automáticos. Si se recibe un error o una respuesta incompleta, revíselo antes de volver a llamar al servicio.

Al terminar, revise Cost Management y los despliegues creados para la práctica. Conserve las evidencias antes de retirar recursos. No elimine un grupo compartido con otras actividades. El repositorio no incluye operaciones automáticas de borrado.
