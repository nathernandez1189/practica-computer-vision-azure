# Fundamentos de visión por computadora

Este documento desarrolla los conceptos del módulo de Microsoft Learn y los relaciona con los experimentos del repositorio.

## Tareas de visión

| Tarea | Resultado | Ejemplo aplicado al hardware |
|---|---|---|
| Clasificación | Una o varias etiquetas de la imagen | Identificar un ratón |
| Detección de objetos | Etiquetas y cajas delimitadoras | Localizar monitor, teclado y torre |
| Segmentación semántica | Categoría por píxel | Separar el dispositivo del fondo |
| Análisis contextual | Descripción de objetos y relaciones | Explicar cómo se conectan los periféricos |

La clasificación implementada aquí asigna puntuaciones a 1.000 clases. No entrega coordenadas ni máscaras. Por ello, una etiqueta `desktop computer` no demuestra que se hayan detectado todos los componentes de un computador. [Fuente: tareas de visión](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/2-overview).

## Píxeles y filtros

Una imagen RGB contiene tres canales de valores. Un filtro calcula una combinación ponderada de píxeles vecinos. El experimento `filtros` aplica el kernel Laplaciano del módulo a una matriz de 7 × 7 con un cuadrado blanco:

```text
-1 -1 -1
-1  8 -1
-1 -1 -1
```

Se calcula la convolución sin relleno: la salida tiene 5 × 5 posiciones. Los dos primeros valores son −255 y −510; el centro uniforme produce 0. El archivo de resultados conserva tanto los valores con signo como su recorte al intervalo 0–255. El recorte pierde información numérica, por lo que no se utiliza como sustituto del cálculo original. [Fuente: procesamiento de imágenes](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/3-understand-image-processing).

## Redes neuronales convolucionales

Una CNN aprende filtros durante el entrenamiento y transforma imágenes en representaciones útiles para predecir clases. MobileNetV2 es la arquitectura utilizada en este repositorio. Se cargan pesos preentrenados y se ejecuta inferencia; no se entrena una red nueva ni se ajustan parámetros con las cinco imágenes. El preprocesamiento asociado a los pesos se aplica de forma consistente. [Fuente: CNN](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/4-computer-vision-models).

## Transformadores y modelos multimodales

Un transformador de visión representa una imagen mediante parches y usa atención para relacionarlos. Un sistema multimodal puede combinar representaciones visuales y lenguaje para responder preguntas sobre una imagen. Esto permite descripciones más amplias que una etiqueta de clasificación, pero no garantiza que todos los detalles de la respuesta estén respaldados visualmente. [Fuente: transformadores y multimodalidad](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/5-modern-vision-models).

En el experimento de Azure se solicita separar observaciones e inferencias. Una fotografía de un módem puede permitir reconocer su función probable, pero no necesariamente su fabricante, velocidad o año exacto. Esa distinción guía la revisión de las respuestas.

## Generación de imágenes

Los modelos generativos crean una imagen a partir de una descripción. Muchos emplean difusión: transforman ruido en una estructura visual condicionada por el texto. Esta tarea produce contenido nuevo; no equivale a clasificar una imagen existente. El ejercicio adicional incluye una prueba de generación, cuya ejecución depende del acceso a un modelo compatible. [Fuente: generación](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/5a-generate-images).

## Limitaciones de la práctica

Las cinco imágenes son ejemplos didácticos y no constituyen un conjunto de evaluación representativo. La puntuación softmax no debe interpretarse como una probabilidad calibrada de que la identificación sea correcta. La descripción visual de referencia se documentó mediante inspección asistida y no corresponde a etiquetas oficiales de Microsoft. La demostración no permite afirmar rendimiento en imágenes reales con oclusión, ruido, iluminación variable o categorías ajenas a ImageNet.
