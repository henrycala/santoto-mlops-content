# Actividad 3: Monitoreo, CI/CD y gobernanza

**Módulo:** 3. Operaciones, Monitoreo y Automatización Continua (CI/CD)
**Entregable:** repositorio con workflow de CI + memoria 3 (ver [plantilla](./plantilla-memoria.md))

## Objetivo

Poner el modelo en condiciones de operación: detectar drift, reentrenar cuando sea necesario, bloquear despliegues que degraden el modelo y documentar el análisis de equidad y gobierno.

## Temas del módulo que cubre

- Conceptos de *data drift* y *model drift*.
- Seguimiento del rendimiento en producción.
- Herramientas de monitoreo (Evidently AI).
- Retraining programado y gestión del ciclo de actualización.
- Principios de CI/CD y tests automatizados de datos, modelos y pipelines.
- Auditoría, documentación y control de calidad.
- Gobierno del modelo, sesgos y equidad.

## Tareas

1. **Lotes con drift controlado.** Usar el generador de la actividad 1 para crear lotes por periodo con distintos niveles de drift (por ejemplo, `drift = 0.0, 0.3, 0.6`).
2. **Reporte de drift.** Comparar cada lote con los datos de entrenamiento y documentar qué variables cambian.
3. **Workflow de CI.** Ejecuta:
   - tests de datos (esquema, rangos, nulos);
   - tests del modelo;
   - un *quality gate*: si el AUC queda por debajo de un umbral, el cambio no se despliega.
5. **Análisis de equidad.** Calcular el rendimiento por subgrupos y documentar las diferencias encontradas.
6. **Nota de gobernanza.** Describir quién aprueba un modelo, qué información se registra y cómo se audita una decisión.

## Criterio de éxito

- Un cambio que degrada el modelo es bloqueado por el CI.
- Un lote con drift simulado produce un reentrenamiento y una nueva versión registrada.

## Entregables

- [ ] Lotes de datos con drift controlado y documentados.
- [ ] Reporte por lote.
- [ ] Flow de reentrenamiento ejecutable con umbral de drift configurable.
- [ ] Workflow de CI con tests de datos, tests del modelo y quality gate.
- [ ] Evidencia de al menos un despliegue bloqueado por el gate.
- [ ] Memoria 3 completa.


## Recursos:
- Libro Guía (Capitulos 5, 6 y 9): https://soclibrary.futa.edu.ng/books/Reliable%20Machine%20Learning%20(Chen,%20CathyMurphy,%20Niall%20RichardParisa%20etc.)%20(Z-Library).pdf

- Documentación especifica:
    - MLFlow: https://mlflow.org/docs/latest/ml/
    - Prefect (orquestación): https://docs.prefect.io/
    - Monitoreo: https://www.evidentlyai.com/

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
