"""Tests de datos: esquema, nulos y rangos del dataset de churn."""
import pytest

from scripts.load_data import COLUMNAS, cargar_datos


@pytest.fixture(scope="module")
def df():
    return cargar_datos()


def test_tiene_todas_las_columnas_esperadas(df):
    assert list(df.columns) == COLUMNAS


def test_no_hay_nulos(df):
    assert int(df.isna().sum().sum()) == 0


def test_objetivo_es_binario(df):
    assert set(df["Exited"].unique()) <= {0, 1}