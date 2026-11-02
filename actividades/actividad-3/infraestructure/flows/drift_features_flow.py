"""Actividad 3: monitoreo de drift de features (tarea 2 de docs/actividad-3.md).

Compara las variables de entrada del lote que puntúa la inferencia (`monitoreo.lote_actual`) con los datos
de entrenamiento usando Evidently. Guarda un reporte HTML en `monitoreo.carpeta_reportes` y emite una alerta si
la fracción de variables con drift supera `monitoreo.umbral_drift`. No necesita MLflow ni etiquetas.

Ejecución (desde la raíz de actividad-3, después de la inferencia):
    poetry run python -m infraestructure.flows.drift_features_flow
"""
from pathlib import Path

import yaml
from evidently import Report
from evidently.presets import DataDriftPreset
from prefect import flow, task

from domain.modelo import VARIABLES
from domain.monitoreo import dividir, fraccion_desde_evidently
from scripts.load_data import cargar_datos

CONFIG = "configs/config.yaml"


@task
def referencia(cfg):
    """Variables de entrada de los datos de entrenamiento: la referencia contra la que se compara el lote."""
    entrenamiento, _ = dividir(cargar_datos(cfg["datos"]["ruta"]), cfg["division"])
    return entrenamiento[VARIABLES]


@task
def calcular_drift(datos_referencia, ruta_lote, cfg):
    """Ejecuta el preset de drift de Evidently y guarda el reporte HTML. Devuelve la fracción de variables con drift."""
    lote = cargar_datos(ruta_lote)
    resultado = Report([DataDriftPreset()]).run(reference_data=datos_referencia, current_data=lote[VARIABLES])

    carpeta = Path(cfg["monitoreo"]["carpeta_reportes"])
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta_html = carpeta / f"drift_features_{Path(ruta_lote).stem}.html"
    resultado.save_html(str(ruta_html))
    print(f"Reporte de drift de features guardado en {ruta_html}")

    return fraccion_desde_evidently(resultado.dict())


@task
def alerta(fraccion, umbral):
    """Avisa si la fracción de variables con drift supera el umbral. Devuelve si hay alerta."""
    hay_alerta = fraccion > umbral
    if hay_alerta:
        print(f"ALERTA: drift de features en {fraccion:.0%} de las variables (umbral {umbral:.0%})")
    else:
        print(f"Sin alerta: drift de features en {fraccion:.0%} de las variables (umbral {umbral:.0%})")
    return hay_alerta


@flow(name="drift-features", log_prints=True)
def drift_features_flow():
    with open(CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    fraccion = calcular_drift(referencia(cfg), cfg["monitoreo"]["lote_actual"], cfg)
    return alerta(fraccion, cfg["monitoreo"]["umbral_drift"])


if __name__ == "__main__":
    drift_features_flow()
