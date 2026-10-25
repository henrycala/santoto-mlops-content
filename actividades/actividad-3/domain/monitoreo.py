"""Lógica de drift y de monitoreo de la API: sin MLflow, Prefect ni Evidently.

Evidently se usa solo en los flows de drift (infraestructure/flows/). Aquí queda lo que se puede
probar sin servicios levantados.
"""
import csv
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split

from domain.modelo import NUMERICAS, OBJETIVO

# Columnas que se guardan por cada petición a /predict.
COLUMNAS_PETICION = ["fecha", "latencia_ms", "version_modelo", "probabilidad", "prediccion"]


def dividir(df, division):
    """Parte los datos igual que el entrenamiento. Devuelve (entrenamiento, prueba)."""
    return train_test_split(
        df,
        test_size=division["test_size"],
        random_state=division["random_state"],
        stratify=df[OBJETIVO],
    )


def aplicar_drift(df, nivel, semilla=42):
    """Desplaza la media de una fracción `nivel` de las variables numéricas, una desviación típica.

    nivel 0.0 no cambia nada. nivel 0.6 desplaza 6 de las 11 variables numéricas (las mismas en cada ejecución
    con la misma semilla). Sirve para crear lotes con drift controlado.
    """
    if not 0 <= nivel <= 1:
        raise ValueError(f"el nivel de drift debe estar entre 0 y 1, no {nivel}")
    out = df.copy()
    n = round(nivel * len(NUMERICAS))
    if n == 0:
        return out
    rng = np.random.default_rng(semilla)
    for columna in rng.choice(NUMERICAS, size=n, replace=False):
        out[columna] = out[columna] + out[columna].std()
    return out


def fraccion_con_drift(drift_por_variable):
    """Fracción de variables con drift. Recibe un dict {variable: True/False}."""
    if not drift_por_variable:
        raise ValueError("no hay variables para calcular el drift")
    return sum(bool(v) for v in drift_por_variable.values()) / len(drift_por_variable)


def validar_lote(lote):
    """Falla si el lote no trae la variable objetivo con valores, porque sin ella no hay drift de evento."""
    if OBJETIVO not in lote.columns:
        raise ValueError(f"el lote no tiene la columna '{OBJETIVO}': no se puede calcular el drift de evento")
    if lote[OBJETIVO].isna().any():
        raise ValueError(f"el lote tiene '{OBJETIVO}' sin valor: no se puede calcular el drift de evento")


def drift_de_target(referencia, lote, alfa):
    """Compara la proporción de la variable objetivo entre la referencia y el lote (test chi-cuadrado).

    Devuelve un dict con las tasas, el p-valor y si hay drift (p-valor menor que `alfa`).
    """
    pos_ref = int(referencia.sum())
    neg_ref = len(referencia) - pos_ref
    pos_lote = int(lote.sum())
    neg_lote = len(lote) - pos_lote
    _, p_valor, _, _ = chi2_contingency([[pos_ref, neg_ref], [pos_lote, neg_lote]])
    return {
        "tasa_referencia": pos_ref / len(referencia),
        "tasa_lote": pos_lote / len(lote),
        "p_valor": float(p_valor),
        "drift": bool(p_valor < alfa),
    }


def registrar_peticion(ruta, fila):
    """Añade una fila al registro CSV de peticiones. Crea el archivo con cabecera si no existe."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not ruta.exists()
    with ruta.open("a", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUMNAS_PETICION)
        if nuevo:
            escritor.writeheader()
        escritor.writerow({k: fila[k] for k in COLUMNAS_PETICION})


def resumen_peticiones(registro):
    """Resume el registro de peticiones: número, latencia media y proporción de predicciones positivas."""
    if registro.empty:
        return {"peticiones": 0, "latencia_media_ms": None, "proporcion_positivas": None}
    return {
        "peticiones": int(len(registro)),
        "latencia_media_ms": round(float(registro["latencia_ms"].mean()), 2),
        "proporcion_positivas": round(float(registro["prediccion"].mean()), 4),
    }


def leer_registro(ruta):
    """Lee el registro de peticiones. Si aún no existe, devuelve un DataFrame vacío."""
    if not Path(ruta).exists():
        return pd.DataFrame(columns=COLUMNAS_PETICION)
    return pd.read_csv(ruta)
