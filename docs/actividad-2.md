# Actividad 2: Pipeline y empaquetado

**Módulo:** 2. Pipelines, Entrenamiento Automatizado y Despliegue
**Entregable:** repositorio + memoria 2 (ver [plantilla](./plantilla-memoria.md))

## Objetivo

Convertir el experimento de la actividad 1 en un pipeline automatizado, con validación de datos, registro del modelo y un servicio de inferencia que consume la versión aprobada.

## Temas del módulo que cubre

- Concepto de pipeline y modularidad.
- Orquestación de tareas con Prefect.
- Separación entre datos, código y configuración.
- Evaluación, reentrenamiento y control de versiones de modelos.
- Serialización de modelos con MLflow Models.
- Creación de una API de inferencia.
- Contenerización con Docker (opcional).

## Tareas

1. **Pipeline completo en Prefect.** Pasos: `ingesta → validación de datos → preprocesado → entrenamiento → evaluación → registro`.
2. **Validación de datos.** Comprobar esquema, tipos, rangos y nulos. Si la validación falla, el pipeline debe detenerse con un error explícito.
3. **Configuración separada.** Parámetros del pipeline (semilla, tamaño de prueba, hiperparámetros) en un archivo de configuración, no en el código.
4. **Registro en MLflow Model Registry.** Registrar cada modelo aprobado y asignarle el alias `champion`.
5. **Servicio de inferencia.** Publicar el modelo con `mlflow models serve` o con una API mínima (FastAPI) que cargue el modelo con alias `champion`.
6. **Contenerización (opcional).** Empaquetar el servicio con Docker.

## Criterio de éxito

Una nueva ejecución del flow genera una versión nueva del modelo, el alias `champion` se actualiza y el servicio responde con la nueva versión sin cambiar código.

## Caso de uso sugerido

El mismo caso de la actividad 1. La configuración debe permitir cambiar el modelo o los hiperparámetros sin tocar el código del pipeline.

## Entregables

- [ ] Flow de Prefect con los pasos del pipeline.
- [ ] Validación de datos con fallo controlado y evidencia de al menos un caso de fallo.
- [ ] Archivo de configuración separado del código.
- [ ] Modelo registrado en MLflow con alias `champion`.
- [ ] Servicio de inferencia funcionando, con una predicción de ejemplo documentada.
- [ ] Memoria 2 completa.


## Recursos:
- Libro Guía (Capitulos 1, 2, 4 y 8): https://soclibrary.futa.edu.ng/books/Reliable%20Machine%20Learning%20(Chen,%20CathyMurphy,%20Niall%20RichardParisa%20etc.)%20(Z-Library).pdf

- Documentación especifica:
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
