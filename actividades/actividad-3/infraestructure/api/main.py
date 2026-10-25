"""Actividad 3: API de inferencia. Sirve el modelo con el alias de MLflow indicado en MODELO_ALIAS.

Ejecución (desde la raíz de actividad-3, con MLFLOW_TRACKING_URI definida):
    poetry run uvicorn infraestructure.api.main:app --port 8000
Documentación interactiva: http://localhost:8000/docs

El alias por defecto es `champion`. Puedes servir otro alias (por ejemplo, `produccion`) con la variable MODELO_ALIAS.

El modelo se carga al arrancar la API. Si el pipeline de entrenamiento asigna un nuevo
champion, hay que reiniciar la API para que lo use.
"""
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import mlflow
import pandas as pd
import yaml
from fastapi import FastAPI
from mlflow.tracking import MlflowClient
from pydantic import BaseModel, Field

from domain.monitoreo import leer_registro, registrar_peticion, resumen_peticiones


with open("configs/config.yaml", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)
NOMBRE_MODELO = cfg["registro"]["nombre_modelo"]
ALIAS = os.environ.get("MODELO_ALIAS", "champion")
# Cada petición a /predict se añade a este CSV (ver domain/monitoreo.py).
REGISTRO = Path(cfg["monitoreo"]["carpeta_reportes"]) / "peticiones.csv"

mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", cfg["mlflow"]["tracking_uri"]))
modelo = mlflow.sklearn.load_model(f"models:/{NOMBRE_MODELO}@{ALIAS}")
VERSION = MlflowClient().get_model_version_by_alias(NOMBRE_MODELO, ALIAS).version

app = FastAPI(title="API de churn", description="Predicción de abandono de clientes con el modelo champion.")


class Cliente(BaseModel):
    """Datos de un cliente. Los nombres son los mismos que las columnas del CSV."""

    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float
    Complain: int
    satisfaction_score: int = Field(alias="Satisfaction Score")
    card_type: str = Field(alias="Card Type")
    point_earned: int = Field(alias="Point Earned")


@app.get("/health")
def health():
    return {"estado": "ok", "modelo": NOMBRE_MODELO, "version": VERSION}


@app.post("/predict")
def predict(cliente: Cliente):
    inicio = time.perf_counter()
    # Usa las mismas columnas con las que se entrenó el modelo.
    datos = pd.DataFrame([cliente.model_dump(by_alias=True)])[list(modelo.feature_names_in_)]
    proba = float(modelo.predict_proba(datos)[0, 1])
    respuesta = {
        "probabilidad_churn": round(proba, 4),
        "prediccion": int(proba >= 0.5),
        "version_modelo": VERSION,
    }
    registrar_peticion(REGISTRO, {
        "fecha": datetime.now(timezone.utc).isoformat(),
        "latencia_ms": round((time.perf_counter() - inicio) * 1000, 3),
        "version_modelo": VERSION,
        "probabilidad": respuesta["probabilidad_churn"],
        "prediccion": respuesta["prediccion"],
    })
    return respuesta


@app.get("/monitoreo")
def monitoreo():
    """Resumen de las peticiones registradas desde que existe el archivo de registro."""
    return resumen_peticiones(leer_registro(REGISTRO))
