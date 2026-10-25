"""Actividad 3: despliegue de las pipelines en Prefect.

- inferencia-diaria: se ejecuta todos los días a las 06:00 (cron "0 6 * * *", en hora UTC).

El entrenamiento se lanza a mano desde la UI de Prefect (http://localhost:4200) cuando tu pipeline esté desplegado.

Ejecución (desde la raíz de actividad-3):
    poetry run python -m infraestructure.flows.desplegar

Deja esta terminal abierta: mientras esté abierta, Prefect puede lanzar las ejecuciones.
"""
from prefect import serve

from infraestructure.flows.inferencia_flow import inferencia_flow

if __name__ == "__main__":
    despliegue_inferencia = inferencia_flow.to_deployment(name="inferencia-diaria", cron="0 6 * * *")
    serve(despliegue_inferencia)
