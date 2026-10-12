"""Lectura de CSV con validación de columnas."""
from pathlib import Path

import pandas as pd

from utils.config import RAIZ


def leer_csv(ruta, columnas=None):
    """Lee un CSV. Una ruta relativa se resuelve desde la raíz del proyecto, no desde el directorio actual.

    Si se indican `columnas`, falla si falta alguna y devuelve solo esas columnas.
    """
    ruta = Path(ruta)
    if not ruta.is_absolute():
        ruta = RAIZ / ruta
    df = pd.read_csv(ruta)
    if columnas is None:
        return df
    faltan = [c for c in columnas if c not in df.columns]
    if faltan:
        raise ValueError(f"Al CSV le faltan columnas: {faltan}")
    return df[columnas].copy()
