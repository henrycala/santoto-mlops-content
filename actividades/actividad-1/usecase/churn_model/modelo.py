"""Modelo de churn: preprocesado, estimadores y entrenamiento. Específico de este caso de uso."""
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from usecase.churn_model.datos import CATEGORICAS, NUMERICAS, OBJETIVO
from utils.modelado import metricas_binarias, particion_estratificada

# Para añadir un modelo: registrarlo aquí y usar su nombre en configs/config.yaml.
MODELOS = {
    "logistic_regression": LogisticRegression,
    "gradient_boosting": GradientBoostingClassifier,
}

FEATURES = NUMERICAS + CATEGORICAS


def split_df(df, division_cfg):
    """Partición estratificada en entrenamiento y prueba según la configuración."""
    return particion_estratificada(
        df,
        OBJETIVO,
        test_size=division_cfg["test_size"],
        random_state=division_cfg["random_state"],
    )


def build_pipeline(modelo_cfg):
    """Pipeline = preprocesado (escalado + one-hot) + estimador, según la configuración."""
    tipo = modelo_cfg["tipo"]
    if tipo not in MODELOS:
        raise ValueError(f"modelo '{tipo}' no soportado. Opciones: {list(MODELOS)}")
    estimador = MODELOS[tipo](**(modelo_cfg.get("parametros") or {}))
    preprocesado = ColumnTransformer(
        [
            ("num", StandardScaler(), NUMERICAS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
        ]
    )
    return Pipeline([("preprocesado", preprocesado), ("modelo", estimador)])


def train_model(train_df, cfg):
    """Ajusta el pipeline completo sobre el conjunto de entrenamiento."""
    return build_pipeline(cfg["modelo"]).fit(train_df[FEATURES], train_df[OBJETIVO])


def evaluate_model(modelo, test_df, umbral=0.5):
    """Calcula métricas sobre el conjunto de prueba. Devuelve (métricas, X_test)."""
    X_test = test_df[FEATURES]
    proba = modelo.predict_proba(X_test)[:, 1]
    return metricas_binarias(test_df[OBJETIVO], proba, umbral), X_test
