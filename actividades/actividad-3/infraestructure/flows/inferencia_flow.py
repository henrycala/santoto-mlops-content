"""Actividad 3: pipeline de inferencia (se ejecuta cada día, ver infraestructure/flows/desplegar.py).

Pasos: cargar modelo champion → ingesta del lote (con drift emulado) → predicción → guardar CSV → registrar en MLflow

El lote sale de la parte de prueba del dataset y se le aplica un drift emulado con `inferencia.nivel_drift`
(ver domain/monitoreo.py). Es una simulación: la pipeline «viene con drift» y el nivel se controla desde config.yaml.
Una copia del lote puntuado se guarda en `monitoreo.lote_actual`, que leen los flows de drift.

El modelo se busca por el alias `champion`, así que cuando el pipeline de entrenamiento
asigna un nuevo champion, la inferencia usa ese modelo sin cambiar código.
El run de inferencia guarda la versión del modelo usada y el nivel de drift en sus tags.

Requisitos: servicios levantados, un champion registrado (lo registra tu pipeline de entrenamiento)
y las variables:
    PREFECT_API_URL=http://localhost:4200/api
    MLFLOW_TRACKING_URI=http://localhost:5000

Ejecución (desde la raíz de actividad-3):
    poetry run python -m infraestructure.flows.inferencia_flow
"""
import os
from datetime import date
from pathlib import Path

import mlflow
import yaml
from mlflow.tracking import MlflowClient
from prefect import flow, task

from domain.monitoreo import aplicar_drift, dividir
from scripts.load_data import cargar_datos

CONFIG = "configs/config.yaml"


@task
def cargar_champion(cfg):
    """Carga el modelo con el alias champion. Devuelve el modelo, su número de versión y su run de entrenamiento."""
    nombre = cfg["registro"]["nombre_modelo"]
    version = MlflowClient().get_model_version_by_alias(nombre, "champion")
    modelo = mlflow.sklearn.load_model(f"models:/{nombre}@champion")
    print(f"Modelo cargado: {nombre} versión {version.version}")
    return modelo, version.version, version.run_id


@task
def ingesta(cfg):
    """Toma un lote de la parte de prueba del dataset y le aplica el drift emulado. Guarda una copia para el monitoreo."""
    _, prueba = dividir(cargar_datos(cfg["datos"]["ruta"]), cfg["division"])
    base = prueba.sample(n=cfg["inferencia"]["tamano_lote"], random_state=cfg["division"]["random_state"])
    lote = aplicar_drift(base, cfg["inferencia"]["nivel_drift"], cfg["division"]["random_state"])

    ruta_lote = Path(cfg["monitoreo"]["lote_actual"])
    ruta_lote.parent.mkdir(parents=True, exist_ok=True)
    lote.to_csv(ruta_lote, index=False)
    print(f"Lote con drift {cfg['inferencia']['nivel_drift']} guardado en {ruta_lote} ({len(lote)} filas)")
    return lote


@task
def predecir(modelo, lote, cfg):
    """Calcula la probabilidad de churn y guarda el resultado en un CSV con la fecha de hoy."""
    # Usa las mismas columnas con las que se entrenó el modelo (según la sección features de config.yaml en ese momento).
    proba = modelo.predict_proba(lote[list(modelo.feature_names_in_)])[:, 1]
    resultado = lote.copy()
    resultado["probabilidad_churn"] = proba
    resultado["prediccion"] = (proba >= 0.5).astype(int)

    carpeta = Path(cfg["inferencia"]["carpeta_salida"])
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"prediccion_{date.today().isoformat()}.csv"
    resultado.to_csv(ruta, index=False)
    print(f"Predicciones guardadas en {ruta}")
    # Se devuelven solo valores simples (no arreglos) para que Prefect pueda pasarlos entre tareas.
    return str(ruta), len(proba), float(proba.mean())


@task
def registrar_inferencia(version, run_id_entrenamiento, nivel_drift, ruta, filas, proba_media):
    """Crea un run de inferencia con tags que apuntan a la versión del modelo, a su run de entrenamiento y al drift."""
    with mlflow.start_run(run_name=f"inferencia-{date.today().isoformat()}"):
        mlflow.set_tag("fase", "inferencia")
        mlflow.set_tag("modelo_version", version)
        mlflow.set_tag("modelo_run_id", run_id_entrenamiento)
        mlflow.set_tag("nivel_drift", nivel_drift)
        mlflow.log_metric("filas_predichas", filas)
        mlflow.log_metric("probabilidad_media", proba_media)
        mlflow.log_artifact(ruta)


@flow(name="inferencia-churn", log_prints=True)
def inferencia_flow():
    with open(CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", cfg["mlflow"]["tracking_uri"]))
    mlflow.set_experiment(cfg["mlflow"]["experimento"])
    modelo, version, run_id_entrenamiento = cargar_champion(cfg)
    lote = ingesta(cfg)
    ruta, filas, proba_media = predecir(modelo, lote, cfg)
    registrar_inferencia(version, run_id_entrenamiento, cfg["inferencia"]["nivel_drift"], ruta, filas, proba_media)


if __name__ == "__main__":
    inferencia_flow()
