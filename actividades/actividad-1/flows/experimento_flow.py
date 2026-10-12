"""Actividad 1: primer flow de Prefect con tracking en MLflow.

Pasos: cargar datos → entrenar y registrar en MLflow → resumen (artefacto de Prefect)

Requisitos: servicios levantados (ver services/README.md) y las variables de entorno:
    PREFECT_API_URL=http://localhost:4200/api
    MLFLOW_TRACKING_URI=http://localhost:5000

Ejecución (desde la raíz del repositorio):
    python flows/experimento_flow.py
    python flows/experimento_flow.py --config configs/config.yaml
"""
import argparse

from prefect import flow, task
from prefect.artifacts import create_markdown_artifact

from usecase.churn_model.datos import load_churn_data
from usecase.churn_model.modelo import evaluate_model, split_df, train_model
from usecase.churn_model.registro import log_run
from utils.config import RAIZ, load_config

RUTA_CONFIG = RAIZ / "configs" / "config.yaml"


@task
def entrenar_y_registrar(df, cfg):
    train_df, test_df = split_df(df, cfg["division"])
    modelo = train_model(train_df, cfg)
    metricas, X_test = evaluate_model(modelo, test_df)
    run_id, _ = log_run(
        modelo,
        metricas,
        X_test,
        cfg,
        nombre_run="experimento-a1",
    )
    return run_id, metricas


@flow(name="experimento-a1", log_prints=True)
def experimento_flow(config: str = str(RUTA_CONFIG)):
    cfg = load_config(config)
    df = load_churn_data(cfg["datos"]["ruta"])
    run_id, metricas = entrenar_y_registrar(df, cfg)

    create_markdown_artifact(
        key="experimento-a1",
        markdown=(
            "## Experimento A1\n\n"
            f"- Modelo: `{cfg['modelo']['tipo']}`\n"
            f"- Filas: {len(df)}\n"
            f"- AUC: **{metricas['auc']:.4f}**\n"
            f"- Recall: {metricas['recall']:.4f}\n"
            f"- Run de MLflow: `{run_id}`"
        ),
    )
    print(f"Run de MLflow: {run_id} | AUC = {metricas['auc']:.4f}")
    return run_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Experimento de la actividad 1")
    parser.add_argument("--config", default=str(RUTA_CONFIG), help="Ruta al YAML de configuración")
    args = parser.parse_args()
    experimento_flow(config=args.config)
