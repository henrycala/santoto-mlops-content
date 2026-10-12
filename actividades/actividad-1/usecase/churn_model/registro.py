"""Registro del run de churn en MLflow: qué parámetros y datos de ejemplo usa este caso de uso."""
from utils.tracking import configurar_mlflow, registrar_run


def setup_mlflow(cfg):
    configurar_mlflow(cfg["mlflow"]["tracking_uri"], cfg["mlflow"]["experimento"])


def log_run(modelo, metricas, X_test, cfg, nombre_run, extra_params=None, tags=None):
    """Registra el modelo de churn con sus parámetros. Devuelve (run_id, model_uri)."""
    setup_mlflow(cfg)
    parametros = {
        "modelo": cfg["modelo"]["tipo"],
        **(cfg["modelo"].get("parametros") or {}),
        "semilla": cfg["division"]["random_state"],
        **(extra_params or {}),
    }
    return registrar_run(
        modelo,
        parametros,
        metricas,
        ejemplo_entrada=X_test,
        ejemplo_salida=modelo.predict_proba(X_test)[:, 1],
        nombre_run=nombre_run,
        tags=tags,
    )
