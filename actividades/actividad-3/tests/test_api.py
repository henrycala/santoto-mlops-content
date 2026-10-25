"""Tests de la API con un modelo falso (sin MLflow)."""
import sys
from types import SimpleNamespace

import mlflow.sklearn  # noqa: F401  (importarlo aquí permite parchear load_model)
import mlflow.tracking
import numpy as np
import pytest
from fastapi.testclient import TestClient

from scripts.load_data import COLUMNAS

CLIENTE = {
    "CreditScore": 600, "Geography": "France", "Gender": "Female", "Age": 40, "Tenure": 3,
    "Balance": 60000.0, "NumOfProducts": 2, "HasCrCard": 1, "IsActiveMember": 1,
    "EstimatedSalary": 50000.0, "Complain": 0, "Satisfaction Score": 3,
    "Card Type": "GOLD", "Point Earned": 400,
}


class ModeloFalso:
    feature_names_in_ = np.array([c for c in COLUMNAS if c != "Exited"])

    def predict_proba(self, X):
        return np.tile([0.3, 0.7], (len(X), 1))


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr("mlflow.sklearn.load_model", lambda uri: ModeloFalso())
    monkeypatch.setattr("mlflow.tracking.MlflowClient", lambda: SimpleNamespace(
        get_model_version_by_alias=lambda nombre, alias: SimpleNamespace(version="7")))
    sys.modules.pop("infraestructure.api.main", None)

    import infraestructure.api.main as main

    monkeypatch.setattr(main, "REGISTRO", tmp_path / "peticiones.csv")
    return TestClient(main.app)


def test_health_y_predict(client):
    assert client.get("/health").json()["version"] == "7"
    assert client.post("/predict", json=CLIENTE).json() == {
        "probabilidad_churn": 0.7, "prediccion": 1, "version_modelo": "7",
    }


def test_cada_prediccion_queda_en_el_monitoreo(client):
    assert client.get("/monitoreo").json()["peticiones"] == 0
    client.post("/predict", json=CLIENTE)
    client.post("/predict", json=CLIENTE)
    resumen = client.get("/monitoreo").json()
    assert resumen["peticiones"] == 2
    assert resumen["proporcion_positivas"] == 1.0
