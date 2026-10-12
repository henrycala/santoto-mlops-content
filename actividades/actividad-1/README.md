# Actividad 1: Fundamentos, versionamiento y tracking

Base reproducible del proyecto: estructura de código, entorno fijado con Poetry, carga del dataset real de churn y un primer experimento registrado en MLflow mediante un flow de Prefect.

Los servicios (MLflow y Prefect) no están en esta carpeta: se levantan desde [`services/`](../../services/README.md).

## Estructura

```
actividad-1/
├── configs/config.yaml           # datos, modelo y MLflow (sin valores en el código)
├── flows/
│   ├── prueba_prefect_flow.py    # flow mínimo para comprobar que Prefect funciona
│   └── experimento_flow.py       # flow de la actividad: cargar datos → entrenar → resumen
├── notebooks/
│   └── mock_mlflow.ipynb         # mock: experimento y modelo registrados en MLflow, sin entrenar
├── docs/                         # material de apoyo (git)
├── utils/                        # general: sirve para cualquier caso de uso
│   ├── config.py                 # carga del YAML y ruta raíz del proyecto
│   ├── datos.py                  # lectura de CSV con validación de columnas
│   ├── modelado.py               # partición estratificada y métricas binarias
│   └── tracking.py               # configurar MLflow y registrar un run
├── usecase/churn_model/          # específico del caso de uso de churn
│   ├── datos.py                  # columnas del dataset real (../data/Customer-Churn-Records.csv)
│   ├── modelo.py                 # preprocesado, modelos disponibles y entrenamiento
│   └── registro.py               # parámetros de churn que se registran en MLflow
├── tests/                        # pruebas de la carga de datos
├── poetry.lock                   # versiones exactas resueltas (no editar a mano)
└── pyproject.toml                # dependencias declaradas con versión fijada
```

## Entorno con Poetry

Desde `actividades/actividad-1`:

```powershell
poetry install                  # crea el entorno e instala dependencias + grupo dev
poetry run pytest -q            # pruebas
```

El proyecto requiere Python entre 3.12 y 3.14, porque Prefect 3.8.8 no admite 3.15 o superior. Si Poetry usa otra versión, indícale cuál usar con `poetry env use python3.12` antes de instalar.

## Ejecución

1. Levanta MLflow desde `services/` (`docker compose up -d`).
2. Define dónde registrar los runs y ejecuta el flow:

En **PowerShell** (Windows):

```powershell
$env:PREFECT_API_URL = "http://localhost:4200/api"
$env:MLFLOW_TRACKING_URI = "http://localhost:5000"
poetry run python flows/experimento_flow.py
```

En **bash** (Linux o WSL):

```bash
export PREFECT_API_URL=http://localhost:4200/api
export MLFLOW_TRACKING_URI=http://localhost:5000
poetry run python flows/experimento_flow.py
```

Prefect y MLflow deben estar levantados (ver [services/README.md](../../services/README.md)). Cada ejecución crea un run nuevo en MLflow y en Prefect: el run aparece en http://localhost:4200/runs y el experimento en http://localhost:5000.

**Prueba de Prefect** (antes del flow de la actividad, para comprobar que el servidor responde):

```bash
poetry run python flows/prueba_prefect_flow.py
```

## Notebooks

- `notebooks/mock_mlflow.ipynb`: **no entrena nada**. Registra un experimento con métricas fijas y un modelo falso en el Model Registry, y lo carga de nuevo. Sirve para comprobar la conexión con MLflow.

El notebook se conecta a `MLFLOW_TRACKING_URI` o, si no está definida, a `http://localhost:5000`, así que MLflow debe estar en marcha antes de ejecutarlo.

## Notas sobre los datos

- Los datos vienen de `actividades/data/Customer-Churn-Records.csv` (10 000 clientes, objetivo `Exited`, sin nulos).
- `Complain` coincide con `Exited` en 9 966 de 10 000 filas: es una fuga de datos. Por eso el AUC sale ≈ 0.999 y no es realista. Se mantiene en el modelo para que el experimento sea reproducible; quitarla es una decisión pendiente.

## Criterio de éxito

Otra persona clona el repositorio, levanta los servicios desde `services/`, ejecuta el flow y obtiene el mismo AUC: el dataset es fijo, la partición usa `random_state` fijo y las versiones de las librerías vienen de `poetry.lock`.

## Entregables

- [x] Repositorio con estructura definida y README.
- [x] Entorno fijado en `pyproject.toml` y bloqueado en `poetry.lock`.
- [x] `usecase/churn_model/datos.py` carga el dataset real y descarta las columnas identificadoras. `utils/datos.py` valida las columnas.
- [x] Flow de Prefect ejecutable con `python flows/experimento_flow.py`.
- [ ] Memoria 1 (la escribe el estudiante con la plantilla del curso).
