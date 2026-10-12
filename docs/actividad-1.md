# Actividad 1: Fundamentos, versionamiento y tracking

**Módulo:** 1. Fundamentos de MLOps y Gestión del Ciclo de Vida
**Entregable:** repositorio Git con código + memoria 1 (ver [plantilla](./plantilla-memoria.md))

## Objetivo

Construir la base reproducible del proyecto: estructura de código, entorno controlado, datos dummy versionables y un primer experimento registrado con trazabilidad.

## Temas del módulo que cubre

- Control de versiones con Git/GitHub.
- Control de entornos (requirements, Conda o Poetry).
- Estructuración profesional de proyectos ML.
- Registro de experimentos: métricas, parámetros y artefactos.
- Reproducibilidad y auditoría del proceso experimental.

## Tareas

1. **Estructura del proyecto.** Crear el repositorio con carpetas `src/`, `flows/`, `configs/`, `tests/`, `notebooks/` y un README que explique cómo ejecutar el proyecto.
2. **Entorno reproducible.** Fijar versiones de dependencias con `pyproject.toml`
3. **Datos dummy.** Implementar `generate_data.py` con semilla fija y parámetros documentados. Los datos no se escriben a mano: se generan con el script.
4. **Primer flow de Prefect.** Crear un flow con las tareas `cargar datos → entrenar → resumen`, donde un modelo de machine learning se genere.
5. **Tracking con MLflow.** Registrar el experimento con parámetros, métricas y artefactos.
6. **Trazabilidad.** Presentar el experimento en la UI de MLflow y en la de Prefect

## Criterio de éxito

Otra persona clona el repositorio, instala el entorno y reproduce el experimento.

## Caso de uso

Como propuesta ideal, se espera que el estudiante plantee un desafío propio de su área de desempeño en el que sea viable aplicar técnicas de Machine Learning, ya sea mediante modelos de clasificación, regresión o forecasting. En caso de no contar con una problemática definida, se podrá optar por un caso de estudio simulado utilizando conjuntos de datos públicos de Kaggle. https://www.kaggle.com/datasets

## Entregables

- [ ] Repositorio Git con estructura definida y README.
- [ ] Entorno fijado y verificado en una instalación limpia.
- [ ] Script `generate_data.py` con semilla y documentación de parámetros.
- [ ] Flow de Prefect ejecutable con `python flows/<flow>.py`.
- [ ] Memoria 1 completa.


## Recursos:
- Libro Guía (Capitulos 1 y 2): https://soclibrary.futa.edu.ng/books/Reliable%20Machine%20Learning%20(Chen,%20CathyMurphy,%20Niall%20RichardParisa%20etc.)%20(Z-Library).pdf

- Documentación especifica:
    - Version control: https://git-scm.com/book/en/v2
    - MLFlow: https://mlflow.org/docs/latest/ml/
    - Prefect (orquestación): https://docs.prefect.io/
    - Control de paquetes - Poetry: https://github.com/python-poetry/poetry

- Lecturas complementarias:
    - docs/boocks/mlops-guide.pdf: Una lectura sobre MLOPs de IBM
    - docs\books\2023-10-EB-Big-Book-of-MLOps-2nd-Edition.pdf: MLOPs en Databricks
    - https://learn.microsoft.com/es-es/training/paths/introduction-machine-learn-operations/
    - https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/ml-operations-planning/ml-operations-planning.pdf
    - https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning?hl=es-419
    - https://developers.google.com/machine-learning/guides/rules-of-ml?hl=es-419

- Repos interesantes:
    - https://github.com/dair-ai/MLOPs-Primer
    - https://ljvmiranda921.github.io/notebook/2020/11/15/data-science-swe/
    - https://github.com/visenger/awesome-mlops
