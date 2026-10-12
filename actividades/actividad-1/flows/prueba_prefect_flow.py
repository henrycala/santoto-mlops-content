"""Flow mínimo para comprobar que Prefect funciona. No usa MLflow ni el dataset.

Pasos: sumar → informar

Requisito: el servidor de Prefect levantado (ver services/README.md) y la variable:
    PREFECT_API_URL=http://localhost:4200/api

Ejecución (desde la raíz de actividad-1):
    python flows/prueba_prefect_flow.py
    python flows/prueba_prefect_flow.py --n 10
Después, el run aparece en http://localhost:4200/runs con estado Completed.
"""
import argparse

from prefect import flow, task


@task
def sumar(n: int) -> int:
    return sum(range(1, n + 1))


@task
def informar(total: int) -> str:
    return f"Suma de 1 a n = {total}"


@flow(name="prueba-prefect", log_prints=True)
def prueba_prefect(n: int = 5) -> str:
    mensaje = informar(sumar(n))
    print(mensaje)
    return mensaje


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prueba mínima de Prefect")
    parser.add_argument("--n", type=int, default=5, help="Hasta qué número sumar")
    args = parser.parse_args()
    prueba_prefect(n=args.n)
