# Actividad 3: Monitoreo, drift y CI

**Módulo:** 3. Operaciones, Monitoreo y Automatización Continua (CI/CD)
**Entregable:** repositorio con pipelines de drift y tests, más memoria 3 (ver [plantilla](./plantilla-memoria.md))

## Objetivo

Pasar un modelo de machine learning de «entrenado una vez» a «vigilado en el tiempo»: detectar cuándo cambian los datos, alertar cuando el drift supera un umbral y comprobar cambios de código con tests.

## Temas del módulo que cubre

- Conceptos de *data drift* y *target drift*.
- Seguimiento del rendimiento en producción.
- Herramientas de monitoreo (Evidently AI).
- Principios de CI/CD y tests automatizados de datos, modelos y pipelines.

## Definición

Cada estudiante construye **su propio sistema de machine learning**, con **su propio dataset y su propio caso de estudio**. Eso incluye:

- **Pipeline de entrenamiento** propio, con su propio algoritmo.
- **Pipeline de inferencia** propio, que puntúa lotes con su modelo.
- **API** propia de inferencia.
- Los pipelines de drift y el CI descritos abajo.

## Tareas

1. **Drift emulado en la pipeline de inferencia.** Tu pipeline de inferencia viene con drift: puntúa lotes tomados de la parte de prueba de tu propio dataset, a los que aplica un drift emulado controlado por un parámetro de configuración (nivel de 0.0 a 1.0, por ejemplo `0.0`, `0.3` o `0.6`). El nivel no lo introduce el usuario al ejecutar la pipeline. La emulación cambia la distribución de algunas variables de entrada y la tasa de la variable objetivo, y guarda una copia del lote que puntúa para que los pipelines de drift la lean. Documenta cómo emulas el drift y qué nivel usas.

2. **Pipelines de detección de drift.** Dos pipelines de Prefect que comparan cada lote con los datos de entrenamiento:
   - **Drift de features:** distribución de cada variable de entrada, con Evidently. Guarda un reporte por lote.
   - **Drift de evento (target):** distribución de la variable objetivo de tu problema en el lote frente al entrenamiento. El lote debe traer las etiquetas reales, que en producción pueden llegar con retraso.

3. **Tests.**:
   - tests de datos (esquema, rangos, nulos);
   - tests de tu modelo, tu inferencia, tu API y de la lógica de drift;
   - (Opcional) tests ejecutados en github a través de una pipeline de CI.
   
   Separa la lógica de MLflow y Prefect en funciones que puedan probarse sin servicios levantados. Para probar la API sin MLflow puedes usar mocks.

## Paso a paso

Sigue el orden. Cada paso deja algo que puedes comprobar antes de pasar al siguiente.

1. **Preparar el entorno.** Levanta MLflow y Prefect desde `services/`, instala las dependencias con Poetry y ejecuta los tests de la referencia para comprobar que tu entorno funciona.
2. **Tarea 1: drift emulado en la inferencia.**
   1. Añade a tu pipeline de inferencia la ingesta de un lote de la parte de prueba de tu dataset.
   2. Añade el parámetro de nivel de drift en la configuración y aplica la emulación al lote antes de predecir.
   3. Guarda una copia del lote que puntúa, para que los pipelines de drift la lean.
   4. Ejecuta la inferencia con nivel 0.0, 0.3 y 0.6 y comprueba que cada ejecución guarda su lote.
3. **Tarea 2: pipelines de detección de drift.**
   1. Drift de features: calcula el reporte por lote con Evidently y guárdalo.
   2. Drift de evento: compara la variable objetivo del lote con la del entrenamiento. Rechaza los lotes sin etiquetas con un mensaje claro.
   3. Alerta: si la fracción de variables con drift supera el umbral configurable, el pipeline emite una alerta (un log o un mensaje, a tu elección).
   4. Escribe tests de la lógica de cada drift, sin MLflow ni Prefect.
   5. Comprueba que los lotes 0.0 y 0.6 producen reportes distintos y que solo el 0.6 supera el umbral.
4. **Tarea 3: tests.**
   1. Escribe tests de datos (esquema, rangos, nulos), del modelo, de la inferencia, de la API y de la lógica de drift. Prueba la API con `httpx` o `TestClient`, usando un modelo falso si no hay MLflow.
   2. Ejecuta `poetry run pytest` en local hasta que todos pasen.
   3. (Opcional) Crea una rama, abre un PR y comprueba que el workflow de CI ejecuta los tests.


## Criterio de éxito

- tests visibles y exitosos.
- Un lote con drift por encima del umbral genera una alerta. Un lote sin drift no la genera.
- Las ejecuciones de la inferencia con nivel de drift 0.0 y 0.6 producen reportes de drift distintos.

## Entregables

- [ ] Pipelines de entrenamiento, inferencia y API propios, con algoritmo propio.
- [ ] Drift emulado en la pipeline de inferencia, con su nivel configurable y documentado (0.0, 0.3 y 0.6).
- [ ] Reporte de drift de features por lote y comparación del target.
- [ ] Pipelines de drift con umbral configurable y alerta cuando se supera.
- [ ] Ejecución de los tests (datos, modelo, inferencia, API y drift).
- [ ] Memoria 3 completa.

## Recursos

- Libro Guía (Capítulos 5, 6 y 9): https://soclibrary.futa.edu.ng/books/Reliable%20Machine%20Learning%20(Chen,%20CathyMurphy,%20Niall%20RichardParisa%20etc.)%20(Z-Library).pdf

- Documentación específica:
    - MLflow: https://mlflow.org/docs/latest/ml/
    - Prefect (orquestación): https://docs.prefect.io/
    - Monitoreo: https://www.evidentlyai.com/

- Lecturas complementarias:
    - docs/boocks/mlops-guide.pdf: Una lectura sobre MLOps de IBM
    - docs\books\2023-10-EB-Big-Book-of-MLOps-2nd-Edition.pdf: MLOps en Databricks
    - https://learn.microsoft.com/es-es/training/paths/introduction-machine-learn-operations/
    - https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/ml-operations-planning/ml-operations-planning.pdf
    - https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning?hl=es-419
    - https://developers.google.com/machine-learning/guides/rules-of-ml?hl=es-419

- Repos interesantes:
    - https://github.com/dair-ai/MLOPs-Primer
    - https://ljvmiranda921.github.io/notebook/2020/11/15/data-science-swe/
    - https://github.com/visenger/awesome-mlops
