"""Registro de experimentos en MLflow: configuración, parámetros, métricas y modelo."""
import os
from pathlib import Path

import mlflow
from mlflow.models import infer_signature

from utils.config import RAIZ


def _uri_absoluta(uri):
    """Resuelve sqlite:///ruta relativa desde la raíz del proyecto, no desde el directorio actual."""
    prefijo = "sqlite:///"
    if uri.startswith(prefijo) and not Path(uri[len(prefijo):]).is_absolute():
        return prefijo + (RAIZ / uri[len(prefijo):]).as_posix()
    return uri


def configurar_mlflow(tracking_uri, experimento):
    """Apunta MLflow al servidor o a la base indicados. MLFLOW_TRACKING_URI tiene prioridad sobre el YAML."""
    uri = os.environ.get("MLFLOW_TRACKING_URI") or _uri_absoluta(tracking_uri)
    mlflow.set_tracking_uri(uri)
    mlflow.set_experiment(experimento)


def aplanar(diccionario):
    """Convierte {'a': {'b': 1}} en {'a.b': 1}. MLflow registra parámetros planos."""
    planos = {}
    for clave, valor in diccionario.items():
        if isinstance(valor, dict):
            for sub, v in aplanar(valor).items():
                planos[f"{clave}.{sub}"] = v
        else:
            planos[clave] = valor
    return planos


def registrar_run(modelo, parametros, metricas, ejemplo_entrada, ejemplo_salida, nombre_run, tags=None):
    """Registra parámetros, métricas y un modelo de sklearn en un run. Devuelve (run_id, model_uri)."""
    signature = infer_signature(ejemplo_entrada, ejemplo_salida)
    with mlflow.start_run(run_name=nombre_run, tags=tags or {}) as run:
        mlflow.log_params(aplanar(parametros))
        mlflow.log_metrics(metricas)
        info = mlflow.sklearn.log_model(
            modelo,
            name="model",
            signature=signature,
            input_example=ejemplo_entrada.head(3),
        )
        return run.info.run_id, info.model_uri
