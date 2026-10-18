# Actividad 2: Pipeline y empaquetado

**Módulo:** 2. Pipelines, Entrenamiento Automatizado y Despliegue
**Entregable:** repositorio + memoria 2 (ver [plantilla](./plantilla-memoria.md))

## Objetivo

Cada grupo construye sus propias pipelines de entrenamiento e inferencia en Prefect, las conecta a través de MLflow y sirve el modelo con una API.

## Temas del módulo que cubre

- Concepto de pipeline y modularidad.
- Orquestación de tareas con Prefect y despliegues programados.
- Separación entre datos, código y configuración.
- Evaluación, reentrenamiento y control de versiones de modelos.
- Creación de una API de inferencia.

## Qué debe entregar el grupo

1. Una **pipeline de entrenamiento** en Prefect, con sus propios pasos de ingesta, entrenamiento, evaluación y registro.
2. Una **pipeline de inferencia** en Prefect, desplegada para ejecutarse **una vez al día**.
3. La **conexión** entre ambas a través de MLflow: la inferencia usa el modelo con el alias `champion`.
4. Una **API con FastAPI** que sirve el modelo `champion`.
5. La **configuración** de los parámetros en un archivo YAML, separada del código.

## Requisitos de cada pieza

### Pipeline de entrenamiento

- Debe tener los pasos ingesta → entrenamiento → evaluación → registro.
- Cada ejecución crea un run en MLflow con el tag `fase = entrenamiento`.
- El modelo nuevo se compara con el champion actual. Solo se registra como nueva versión y pasa a ser `champion` si supera un AUC mínimo y también el AUC del champion vigente. Si no, el run queda registrado pero el alias no cambia. Así, en cada momento hay un único champion, y solo se reemplaza por un modelo que mejora. El grupo puede definir criterios adicionales (por ejemplo, otra métrica o una mejora mínima).

### Pipeline de inferencia

- Debe cargar el modelo por su alias `champion`, no por un número de versión fijo.
- Debe tomar un lote de datos y calcular predicciones. Puede ser una muestra de datos que simule clientes nuevos.
- Debe guardar las predicciones en un archivo con la fecha de ejecución.

### API de inferencia

- Debe cargar el modelo `champion` y exponer al menos un endpoint para predecir con los datos de un cliente.
- Debe incluir una predicción de ejemplo en la documentación del grupo.

### Despliegue en Prefect

- La pipeline de entrenamiento y la de inferencia deben aparecer como despliegues separados.
- La inferencia debe tener un horario diario. El entrenamiento puede lanzarse a mano.

## Configuración

Los valores que pueden cambiar (umbral de AUC, tamaño del lote, nombre del modelo o hiperparámetros) deben estar en un archivo YAML, no escritos en el código. Así, el grupo puede ajustar la pipeline sin tocar el código.

Las variables del experimento se eligen en `configs/features.yaml`, con un alias en `seleccion`:

- `ALL`: todas las variables, numéricas y categóricas.
- `NUMERIC`: solo las variables numéricas.
- `CUSTOM`: solo las variables que listes en `custom`. Los nombres deben coincidir con las columnas del CSV.

Cada run registra en MLflow el alias usado (`features`) y el número de variables (`n_features`), para poder comparar experimentos.

## Pasos sugeridos

Estos pasos son una forma de ordenar el trabajo. El grupo puede seguir otro orden si tiene sentido para su diseño.

1. **Entorno.** Usa el repositorio del grupo con el entorno de la actividad 1 (`poetry install`). Necesitas los servicios de MLflow y Prefect levantados (ver [services/README.md](../services/README.md)). En cada terminal donde ejecutes un flow o la API, define las variables:

   ```powershell
   $env:PREFECT_API_URL = "http://localhost:4200/api"
   $env:MLFLOW_TRACKING_URI = "http://localhost:5000"
   ```

2. **config.** Define en el YAML los valores que usará la pipeline.
3. **Entrenamiento.** Escribe el flow de entrenamiento, ejecútalo y revisa sus logs en Prefect y el registro en MLflow.
5. **Inferencia.** Escribe el flow de inferencia y ejecútalo. Revisa en MLflow que el run de inferencia aparece en el experimento.
6. **API.** Sirve el modelo `champion` con FastAPI y prueba una predicción. Recuerda que, si cambia el champion, hay que reiniciar la API.
7. **Despliegue.** Registra los dos despliegues en Prefect, con el horario diario en la inferencia, y comprueba que aparecen en la UI.

## Ejemplo de referencia

El repositorio incluye un ejemplo funcionando en `actividades/actividad-2/`, con el caso de churn de la actividad 1:

- `domain/modelo.py`: lógica de negocio del modelo (variables, pipeline y métricas). No usa Prefect ni MLflow.
- `scripts/load_data.py`: carga del CSV con validación de columnas.
- `infraestructure/flows/entrenamiento_flow.py`: pipeline de entrenamiento en Prefect, con el registro en MLflow.
- `infraestructure/flows/inferencia_flow.py`: pipeline de inferencia en Prefect.
- `infraestructure/flows/desplegar.py`: despliegues en Prefect.
- `infraestructure/api/main.py`: API de FastAPI.
- `configs/config.yaml`: configuración.
- `configs/features.yaml`: selección de variables del experimento (`ALL`, `NUMERIC` o `CUSTOM`).

Úsalo para entender cómo se conectan las piezas. El grupo debe escribir su propia versión adaptada a su caso de uso, en lugar de copiar el ejemplo.

## Criterio de éxito

Una nueva ejecución del entrenamiento genera una versión nueva del modelo y el alias `champion` pasa a apuntar a ella. Después de reiniciar la API, el servicio responde con la nueva versión sin cambiar código.

## Entregables

- [ ] Pipeline de entrenamiento en Prefect con los pasos ingesta → entrenamiento → evaluación → registro.
- [ ] Configuración separada del código, en YAML.
- [ ] Modelo registrado en MLflow con alias `champion`, y run de entrenamiento con tag `fase = entrenamiento`.
- [ ] Pipeline de inferencia en Prefect con horario diario, que carga el modelo `champion` y guarda sus predicciones.
- [ ] API de inferencia que sirve el modelo `champion`, con una predicción de ejemplo documentada.
- [ ] Memoria 2 completa.

## Recursos:
- Libro Guía (Capitulos 1, 2, 4 y 8): https://soclibrary.futa.edu.ng/books/Reliable%20Machine%20Learning%20(Chen,%20CathyMurphy,%20Niall%20RichardParisa%20etc.)%20(Z-Library).pdf

- Documentación especifica:
    - MLFlow: https://mlflow.org/docs/latest/ml/
    - Prefect (orquestación): https://docs.prefect.io/
    - Control de paquetes - Poetry: https://github.com/python-poetry/poetry

- Lecturas complementarias:
    - docs/boocks/mlops-guide.pdf: Una lectura sobre MLOPs de IBM
    - docs\books\2023-10-EB-Big-Book-of-MLOps-2nd-Edition.pdf: MLOPs en Databricks
    - https://learn.microsoft.com/es-es/training/paths/introduction-machine-learn-operations/
    - https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/ml-operations-planning/ml-operations-planning.pdf
    - https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning?hl=es-419
    - https://developers.google.com/machine-learning/guides/rules-of-ml?hl=es-419

- Repos interesantes:
    - https://github.com/dair-ai/MLOPs-Primer
    - https://ljvmiranda921.github.io/notebook/2020/11/15/data-science-swe/
    - https://github.com/visenger/awesome-mlops
