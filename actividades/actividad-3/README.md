# Actividad 3: monitoreo, drift y CI

Enunciado completo, tareas y entregables: [`docs/actividad-3.md`](../../docs/actividad-3.md).

Cada estudiante entrega **su propio** pipeline de entrenamiento, de inferencia y su API, con un algoritmo propio. El código de `domain/`, `infraestructure/` y `scripts/` es la referencia de la actividad 2, no la entrega.

## Comandos

Desde `actividades/actividad-3/`, en este orden:

```bash
poetry install                                                # dependencias (incluye pytest)
poetry run pytest                                             # tests (lo mismo que corre el CI en cada PR)
poetry run python -m infraestructure.flows.inferencia_flow    # puntúa un lote con drift emulado (inferencia.nivel_drift) con champion
poetry run python -m infraestructure.flows.drift_features_flow  # drift de features del lote: reporte HTML en reports/ y alerta
poetry run python -m infraestructure.flows.drift_evento_flow    # drift del target (Exited) del lote y alerta
```

La inferencia necesita MLflow con un champion. Los dos flows de drift leen el lote que deja la inferencia (`monitoreo.lote_actual`) y no necesitan MLflow ni Prefect levantados.

Para levantar la API hace falta un modelo con el alias `champion` en MLflow (ver el README raíz para levantar los servicios):

```bash
MLFLOW_TRACKING_URI=http://localhost:5000 poetry run uvicorn infraestructure.api.main:app --port 8000
```

Documentación interactiva: http://localhost:8000/docs

## Estructura

```
configs/            configuración (datos, modelo, MLflow, inferencia con drift emulado y drift)
domain/             lógica del modelo y de drift, sin MLflow ni Prefect
infraestructure/    API (api/) y flows de Prefect (flows/)
scripts/            carga de datos y utilidades
tests/              tests unitarios
```
