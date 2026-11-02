# Actividad 4: Sistema end-to-end y reflexión

**Módulo:** Integración de los módulos 1 a 3
**Entregable:** documento de máximo 2 páginas

## Objetivo

Validar el entendimiento y el proceso de principio a fin: qué decisiones se tomaron y qué quedó pendiente.

## Temas del módulo que cubre

- Integración de pipelines de entrenamiento, inferencia, monitoreo y CI.
- Trazabilidad: qué componente produce qué artefacto y dónde queda registrado.
- Documentación técnica de un sistema de ML.
- Evaluación crítica del trabajo realizado.

## Qué debe entregar el grupo

Un documento de reflexión que incluya:

1. Una narrativa sobre el sistema que construyeron en las actividades 1 a 3 y cómo funciona de principio a fin. No es un informe por actividad: lo importante es cómo se conectan las piezas (datos, entrenamiento, champion, inferencia, API, drift y CI) y qué decisiones tomaron en el camino.
2. Una sección sobre qué componentes del sistema les causaron mayor dificultad.
3. Una sección sobre qué temas del curso les hubiera gustado profundizar más.
4. Qué fue lo más valioso del curso y qué debería mejorar.

Pueden guiarse con estas preguntas, sin seguir un orden fijo:

- ¿Qué hace el sistema hoy de punta a punta? ¿Cómo viaja un dato desde el CSV hasta una alerta de drift?
- ¿Qué decisiones les costaron más y por qué las tomaron así?
- ¿Qué trabajo quedó por mejorar, y qué harían con más tiempo?

## Criterio de éxito

- Otra persona puede leer el documento y entender cómo funciona el sistema.
- Lo que afirma el documento coincide con lo que hay en el repositorio.

## Entregables

- [ ] Documento de reflexión de máximo 2 páginas.
- [ ] Evidencias (capturas o enlaces) de los puntos que el documento menciona.

## Recursos:
- Libro Guía (Capítulos 1 a 9): https://soclibrary.futa.edu.ng/books/Reliable%20Machine%20Learning%20(Chen,%20CathyMurphy,%20Niall%20RichardParisa%20etc.)%20(Z-Library).pdf

- Documentación específica:
    - Version control: https://git-scm.com/book/en/v2
    - MLflow: https://mlflow.org/docs/latest/ml/
    - Prefect (orquestación): https://docs.prefect.io/
    - Control de paquetes - Poetry: https://github.com/python-poetry/poetry
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
