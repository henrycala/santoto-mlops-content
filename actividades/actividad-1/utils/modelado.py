"""Partición de datos y métricas para clasificación binaria."""
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split


def particion_estratificada(df, columna_objetivo, test_size, random_state):
    """Divide en entrenamiento y prueba manteniendo la proporción de la clase objetivo."""
    return train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[columna_objetivo],
    )


def metricas_binarias(y_true, proba, umbral=0.5):
    """Métricas de un clasificador binario a partir de probabilidades de la clase positiva."""
    pred = (proba >= umbral).astype(int)
    return {
        "auc": float(roc_auc_score(y_true, proba)),
        "accuracy": float(accuracy_score(y_true, pred)),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred, zero_division=0)),
        "f1": float(f1_score(y_true, pred, zero_division=0)),
    }
