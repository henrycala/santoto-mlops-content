"""Genera lotes de prueba con drift controlado a partir de la parte de prueba del dataset.

Cada lote sale de la parte de prueba (no de la de entrenamiento), así que el drift se mide contra
datos que el modelo no ha visto. Un archivo por nivel de `monitoreo.niveles_drift`, en `monitoreo.carpeta_lotes`.

Ejecución (desde la raíz de actividad-3):
    poetry run python -m scripts.generar_lotes_drift
"""
from pathlib import Path

import yaml

from domain.monitoreo import aplicar_drift, dividir
from scripts.load_data import cargar_datos

CONFIG = "configs/config.yaml"


def main():
    with open(CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    mon = cfg["monitoreo"]
    _, prueba = dividir(cargar_datos(cfg["datos"]["ruta"]), cfg["division"])
    base = prueba.sample(n=mon["tamano_lote"], random_state=cfg["division"]["random_state"])

    carpeta = Path(mon["carpeta_lotes"])
    carpeta.mkdir(parents=True, exist_ok=True)
    for nivel in mon["niveles_drift"]:
        ruta = carpeta / f"lote_drift_{nivel:.1f}.csv"
        aplicar_drift(base, nivel, cfg["division"]["random_state"]).to_csv(ruta, index=False)
        print(f"Lote con drift {nivel:.1f} guardado en {ruta} ({len(base)} filas)")


if __name__ == "__main__":
    main()
