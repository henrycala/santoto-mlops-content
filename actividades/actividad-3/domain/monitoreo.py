import numpy as np
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split
import pandas as pd

from domain.modelo import NUMERICAS, OBJETIVO


def dividir(df, division):
    """Parte los datos igual que el entrenamiento. Devuelve (entrenamiento, prueba)."""
    return train_test_split(
        df,
        test_size=division["test_size"],
        random_state=division["random_state"],
        stratify=df[OBJETIVO],
    )


# Subida máxima de la tasa de la variable objetivo (en puntos decimales: 0.3 = +30%).
SUBIDA_TASA_MAXIMA = 0.3


def aplicar_drift(df, nivel, semilla=42):
    """Emula drift en un lote: de features y del target de forma controlada."""
    if not 0 <= nivel <= 1:
        raise ValueError(f"El nivel de drift debe estar entre 0 y 1, no {nivel}")
    
    out = df.copy()
    rng = np.random.default_rng(semilla)

    # 1. Drift en features numéricas (desplaza la media una desviación típica)
    n = round(nivel * len(NUMERICAS))
    if n > 0:
        columnas_afectadas = rng.choice(NUMERICAS, size=n, replace=False)
        for columna in columnas_afectadas:
            std_val = out[columna].std()
            if pd.notna(std_val) and std_val > 0:
                out[columna] = out[columna] + 2*std_val

    # 2. Drift en el target (etiqueta)
    out[OBJETIVO] = _subir_tasa(out[OBJETIVO], nivel * SUBIDA_TASA_MAXIMA, rng)
    return out


def _subir_tasa(objetivo, subida, rng):
    """Convierte negativos en positivos (al azar) hasta que la tasa sube `subida` puntos."""
    # Asegurar que el objetivo sea numérico entero (0 o 1) para evitar errores de tipo
    objetivo_int = objetivo.astype(int)
    
    tasa_actual = objetivo_int.mean()
    nueva_tasa = min(tasa_actual + subida, 1.0)
    
    pos_objetivo = round(nueva_tasa * len(objetivo_int))
    faltan = pos_objetivo - int(objetivo_int.sum())
    
    if faltan <= 0:
        return objetivo

    subidos = objetivo.copy()
    indices_ceros = objetivo_int.index[objetivo_int == 0]
    
    # Evitar IndexError si piden más elementos de los que hay disponibles en 0
    faltan = min(faltan, len(indices_ceros))
    if faltan > 0:
        a_cambiar = rng.choice(indices_ceros, size=faltan, replace=False)
        subidos.loc[a_cambiar] = 1

    return subidos


def fraccion_desde_evidently(resultado):
    """Saca la fracción de variables con drift del resultado de Evidently (`snapshot.dict()`)."""
    for metrica in resultado["metrics"]:
        if metrica["metric_name"].startswith("DriftedColumnsCount"):
            return float(metrica["value"]["share"])
    raise ValueError("El resultado de Evidently no incluye DriftedColumnsCount")


def validar_lote(lote):
    """Falla si el lote no trae la variable objetivo con valores."""
    if OBJETIVO not in lote.columns:
        raise ValueError(f"El lote no tiene la columna '{OBJETIVO}': no se puede calcular el drift de evento")
    if lote[OBJETIVO].isna().any():
        raise ValueError(f"El lote tiene '{OBJETIVO}' sin valor: no se puede calcular el drift de evento")


def drift_de_target(referencia, lote, alfa):
    """Compara la proporción de la variable objetivo entre referencia y lote (test chi-cuadrado)."""
    # Convertir a enteros por seguridad en los conteos
    ref_int = referencia.astype(int)
    lote_int = lote.astype(int)
    
    pos_ref = int(ref_int.sum())
    neg_ref = len(ref_int) - pos_ref
    pos_lote = int(lote_int.sum())
    neg_lote = len(lote_int) - pos_lote
    
    _, p_valor, _, _ = chi2_contingency([[pos_ref, neg_ref], [pos_lote, neg_lote]])
    return {
        "tasa_referencia": pos_ref / len(ref_int),
        "tasa_lote": pos_lote / len(lote_int),
        "p_valor": float(p_valor),
        "drift": bool(p_valor < alfa),
    }