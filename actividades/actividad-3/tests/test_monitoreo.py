"""Tests de drift y de monitoreo. No necesitan servicios."""
import numpy as np
import pandas as pd
import pytest

from domain.modelo import NUMERICAS, OBJETIVO
from domain.monitoreo import aplicar_drift, drift_de_target, fraccion_con_drift, registrar_peticion, resumen_peticiones, validar_lote


@pytest.fixture
def datos():
    rng = np.random.default_rng(0)
    df = pd.DataFrame({columna: rng.normal(0, 1, 500) for columna in NUMERICAS})
    df[OBJETIVO] = rng.integers(0, 2, 500)
    return df


def test_drift_cero_no_cambia_los_datos(datos):
    assert aplicar_drift(datos, 0.0).equals(datos)


def test_drift_cambia_la_fraccion_indicada_de_variables(datos):
    lote = aplicar_drift(datos, 0.6)
    cambiadas = [c for c in NUMERICAS if not np.allclose(lote[c], datos[c])]
    assert len(cambiadas) == round(0.6 * len(NUMERICAS))


def test_fraccion_con_drift():
    assert fraccion_con_drift({"a": True, "b": False, "c": False, "d": True}) == 0.5


def test_validar_lote_exige_objetivo(datos):
    with pytest.raises(ValueError, match=OBJETIVO):
        validar_lote(datos.drop(columns=[OBJETIVO]))


def test_drift_de_target_detecta_cambio_de_tasa():
    referencia = pd.Series([0] * 800 + [1] * 200)
    lote = pd.Series([0] * 400 + [1] * 600)
    assert drift_de_target(referencia, lote, alfa=0.05)["drift"] is True


def test_drift_de_target_no_alerta_con_la_misma_tasa():
    referencia = pd.Series([0] * 800 + [1] * 200)
    lote = pd.Series([0] * 80 + [1] * 20)
    assert drift_de_target(referencia, lote, alfa=0.05)["drift"] is False


def test_resumen_de_peticiones_registradas(tmp_path):
    ruta = tmp_path / "peticiones.csv"
    for latencia, prediccion in [(2.0, 1), (4.0, 0), (6.0, 1), (8.0, 0)]:
        registrar_peticion(ruta, {"fecha": "x", "latencia_ms": latencia, "version_modelo": "1",
                                  "probabilidad": 0.5, "prediccion": prediccion})
    assert resumen_peticiones(pd.read_csv(ruta)) == {
        "peticiones": 4,
        "latencia_media_ms": 5.0,
        "proporcion_positivas": 0.5,
    }
