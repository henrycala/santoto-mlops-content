"""Dataset de churn: columnas esperadas y carga. Específico de este caso de uso."""
from utils.datos import leer_csv

# Las columnas de identificación no son variables predictivas, así que se descartan antes de entrenar.
IDENTIFICADORES = ["RowNumber", "CustomerId", "Surname"]
NUMERICAS = [
    "CreditScore",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Complain",
    "Satisfaction Score",
    "Point Earned",
]
CATEGORICAS = ["Geography", "Gender", "Card Type"]
OBJETIVO = "Exited"
COLUMNAS = NUMERICAS + CATEGORICAS + [OBJETIVO]


def load_churn_data(ruta):
    """Lee el CSV de churn y devuelve solo las variables predictivas y el objetivo."""
    return leer_csv(ruta, COLUMNAS)
