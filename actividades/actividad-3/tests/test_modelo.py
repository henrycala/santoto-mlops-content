"""Tests del modelo: features, pipeline y métricas. No necesitan MLflow ni Prefect."""
import numpy as np
import pandas as pd
import pytest

from domain.modelo import NUMERICAS, CATEGORICAS, calcular_metricas, construir_modelo, resolver_features


def test_resolver_features_all():
    numericas, categoricas = resolver_features("ALL")
    assert numericas == NUMERICAS
    assert categoricas == CATEGORICAS


def test_resolver_features_lista_separa_numericas_y_categoricas():
    numericas, categoricas = resolver_features(["Age", "Geography"])
    assert numericas == ["Age"]
    assert categoricas == ["Geography"]


def test_resolver_features_rechaza_variables_desconocidas():
    with pytest.raises(ValueError):
        resolver_features(["NoExiste"])


@pytest.mark.parametrize("tipo, parametros", [
    ("logistic_regression", {"C": 1.0, "max_iter": 1000}),
    ("gradient_boosting", {"n_estimators": 10, "max_depth": 2, "random_state": 42}),
])
def test_modelo_predice_probabilidades_validas(tipo, parametros):
    rng = np.random.default_rng(0)
    X = pd.DataFrame({
        "Age": rng.integers(18, 80, 200),
        "Balance": rng.random(200) * 1000,
        "Geography": rng.choice(["France", "Spain", "Germany"], 200),
    })
    y = (X["Age"] > 50).astype(int)

    modelo = construir_modelo(tipo, parametros, ["Age", "Balance"], ["Geography"])
    modelo.fit(X, y)
    proba = modelo.predict_proba(X)[:, 1]

    assert proba.shape == (200,)
    assert ((proba >= 0) & (proba <= 1)).all()


def test_calcular_metricas_perfecto():
    y = np.array([0, 0, 1, 1])
    proba = np.array([0.1, 0.2, 0.8, 0.9])
    metricas = calcular_metricas(y, proba, umbral=0.5)
    assert metricas["auc"] == 1.0
    assert metricas["accuracy"] == 1.0
