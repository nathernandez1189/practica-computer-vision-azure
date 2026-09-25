# Resultados y discusión

## Clasificación de hardware

La ejecución se realizó en CPU con MobileNetV2 y pesos `IMAGENET1K_V2`. El archivo [clasificacion-local.json](../evidencias/clasificacion-local.json) contiene los resultados de inferencia, los identificadores de los pesos y las huellas de las entradas.

| Imagen | Primera clase | Puntuación | Segunda clase | Puntuación |
|---|---|---:|---|---:|
| 01 | desktop computer | 49,71 % | screen | 7,00 % |
| 02 | mouse | 4,30 % | whistle | 2,39 % |
| 03 | modem | 14,14 % | radio | 4,65 % |
| 04 | hard disc | 96,74 % | CD player | 0,21 % |
| 05 | notebook | 24,05 % | laptop | 9,41 % |

**Computador de escritorio.** La primera clase representa el conjunto. Las alternativas `screen`, `monitor`, `mouse` y `computer keyboard` guardan relación con partes visibles. Sin embargo, la salida es una clasificación global y no demuestra detección espacial de esos componentes.

**Ratón.** `mouse` aparece primero, pero con solo 4,30 %. Las alternativas incluyen objetos visualmente diferentes. La distribución sugiere ambigüedad y justifica revisión; no se debe convertir el resultado en una identificación definitiva mediante un umbral arbitrario.

**Módem.** La clase principal coincide con la función aparente del dispositivo. El modelo también puntúa `radio` y `projector`, lo cual muestra que la forma de la carcasa y los controles no resuelven por sí solos la categoría. La imagen no demuestra una velocidad de transmisión, marca o año exacto.

**Disco duro.** `hard disc` concentra 96,74 %. La imagen muestra platos y un brazo interno que resultan compatibles con la identificación. Esta observación no permite concluir que el modelo mantendrá ese rendimiento ante un disco cerrado, otro ángulo o una fotografía de baja calidad.

**Portátil.** Las clases `notebook` y `laptop` están relacionadas semánticamente. Se conservan separadas porque así están definidas en el clasificador; no se suman ni se cambian las etiquetas para mejorar la presentación del resultado.

## Filtro Laplaciano

El [resultado del filtro](../evidencias/filtro-laplaciano.json) reproduce las dos primeras operaciones numéricas del ejemplo del módulo: −255 y −510. La salida central es 0 en una zona uniforme. Los valores del contorno son distintos de cero, por lo que el filtro destaca cambios locales. Es una operación matemática ejecutada con un kernel fijo y no un modelo entrenado.

## Interpretación del alcance

La práctica demuestra que una misma arquitectura puede producir una etiqueta plausible con distribuciones de puntuación muy distintas. Con cinco ejemplos seleccionados para enseñanza no se calcula una exactitud de validación, F1 ni una estimación de generalización. No existe un proceso de separación de entrenamiento y prueba porque se utiliza un modelo ya entrenado y no se realiza ajuste.

La combinación posterior con lenguaje natural debe conservar esta incertidumbre. Un sistema conversacional puede redactar una explicación convincente aun cuando la clasificación previa sea ambigua. Para el cliente Azure se solicita explícitamente distinguir lo observable de lo inferido. Sus respuestas reales solo se incorporarán cuando se ejecute el servicio.
