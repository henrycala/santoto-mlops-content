"""Carga de configuración YAML y ruta raíz del proyecto."""
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]


def load_config(ruta):
    """Devuelve el archivo YAML como diccionario."""
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)
