"""Actividad 3: monitoreo de drift de evento, es decir, del target (tarea 2 de docs/actividad-3.md).

Compara la proporción de la variable objetivo del lote con la de los datos de entrenamiento
(test chi-cuadrado). Rechaza los lotes sin etiquetas, porque sin ellas no hay drift de evento.
Emite una alerta si el p-valor queda por debajo de `monitoreo.alfa_evento`. Lee el lote que puntúa la
inferencia (`monitoreo.lote_actual`).

Ejecución (desde la raíz de actividad-3, después de la inferencia):
    poetry run python -m infraestructure.flows.drift_evento_flow
"""
import pandas as pd
import yaml
from prefect import flow, task

from domain.modelo import OBJETIVO
from domain.monitoreo import dividir, drift_de_target, validar_lote
from scripts.load_data import cargar_datos

CONFIG = "configs/config.yaml"


@task
def referencia(cfg):
    """Variable objetivo de los datos de entrenamiento."""
    entrenamiento, _ = dividir(cargar_datos(cfg["datos"]["ruta"]), cfg["division"])
    return entrenamiento[OBJETIVO]


@task
def evaluar_evento(referencia_objetivo, ruta_lote, cfg):
    """Compara el target del lote con la referencia. Falla con un mensaje claro si el lote no trae etiquetas."""
    lote = pd.read_csv(ruta_lote)
    validar_lote(lote)
    resultado = drift_de_target(referencia_objetivo, lote[OBJETIVO], cfg["monitoreo"]["alfa_evento"])
    print(
        f"Tasa de {OBJETIVO}: entrenamiento {resultado['tasa_referencia']:.1%}, lote {resultado['tasa_lote']:.1%} "
        f"(p-valor {resultado['p_valor']:.4f})"
    )
    return resultado


@task
def alerta(resultado, alfa):
    """Avisa si el drift del target supera el nivel de significación. Devuelve si hay alerta."""
    hay_alerta = resultado["drift"]
    if hay_alerta:
        print(f"ALERTA: drift del target {OBJETIVO} (p-valor {resultado['p_valor']:.4f} < {alfa})")
    else:
        print(f"Sin alerta: drift del target {OBJETIVO} (p-valor {resultado['p_valor']:.4f} >= {alfa})")
    return hay_alerta


@flow(name="drift-evento", log_prints=True)
def drift_evento_flow():
    with open(CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    resultado = evaluar_evento(referencia(cfg), cfg["monitoreo"]["lote_actual"], cfg)
    return alerta(resultado, cfg["monitoreo"]["alfa_evento"])


if __name__ == "__main__":
    drift_evento_flow()
