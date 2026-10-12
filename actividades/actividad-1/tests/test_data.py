import pandas as pd
import pytest

from usecase.churn_model.datos import COLUMNAS, IDENTIFICADORES, OBJETIVO, load_churn_data
from utils.config import RAIZ

CSV = RAIZ / ".." / "data" / "Customer-Churn-Records.csv"


def test_carga_el_csv_con_las_columnas_esperadas():
    df = load_churn_data(CSV)
    assert list(df.columns) == COLUMNAS
    assert len(df) == 10000


def test_sin_nulos_y_objetivo_binario():
    df = load_churn_data(CSV)
    assert df.isna().sum().sum() == 0
    assert set(df[OBJETIVO].unique()) <= {0, 1}


def test_no_incluye_identificadores():
    df = load_churn_data(CSV)
    assert not set(IDENTIFICADORES) & set(df.columns)


def test_columna_faltante_falla(tmp_path):
    ruta = tmp_path / "incompleto.csv"
    pd.DataFrame({"Age": [1], "Exited": [0]}).to_csv(ruta, index=False)
    with pytest.raises(ValueError):
        load_churn_data(ruta)
