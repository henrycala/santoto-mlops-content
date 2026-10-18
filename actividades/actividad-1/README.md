# Actividad 1: Fundamentos, versionamiento y tracking

Base reproducible del proyecto: estructura de código, entorno fijado con Poetry, carga y validación del dataset de churn, y un primer experimento registrado en MLflow mediante un flow de Prefect.

Los servicios (MLflow y Prefect) no están en esta carpeta: se levantan desde [`services/`](../../services/README.md).

## Estructura

```
actividad-1/
├── configs/config.yaml           # datos, división, modelo, MLflow y umbral (sin valores en el código)
├── flows/
│   ├── prueba_flow.py            # flow mínimo para comprobar que Prefect y MLflow responden
│   └── experimento_flow.py       # flow de la actividad: cargar datos → entrenar → resumen
├── notebooks/
│   ├── eda_churn.ipynb           # análisis exploratorio del dataset y riesgos de fuga de datos
│   ├── train.ipynb               # el mismo experimento del flow, paso a paso y sin Prefect
│   └── mock_mlflow.ipynb         # mock: registra un experimento y un modelo falso, sin entrenar
├── scripts/
│   ├── load_data.py              # carga el CSV de churn y valida sus columnas
│   └── generate_data.py          # genera un CSV sintético con el mismo esquema y semilla fija
├── tests/
│   ├── test_data.py              # carga y validación del dataset real
│   ├── test_generate_data.py     # datos sintéticos: esquema, proporción, semilla y errores
│   └── test_experimento_flow.py  # entrenamiento, registro en MLflow y ejecución del flow
├── docs/git.md                   # material de apoyo sobre Git
├── poetry.lock                   # versiones exactas resueltas (no editar a mano)
└── pyproject.toml                # dependencias declaradas con versión fijada
```

El dataset no está dentro de esta carpeta: `actividades/data/Customer-Churn-Records.csv`. `mlflow.db` y `mlruns/` se generan al ejecutar y no se versionan.

## Entorno con Poetry

Desde `actividades/actividad-1`:

```powershell
poetry install                  # crea el entorno e instala dependencias + grupo dev
poetry run pytest -q            # pruebas
```

El proyecto requiere Python entre 3.12 y 3.14, porque Prefect 3.8.8 no admite 3.15 o superior. Si Poetry usa otra versión, indícale cuál usar con `poetry env use python3.12` antes de instalar.

Las pruebas usan rutas relativas, así que ejecútalas siempre desde `actividades/actividad-1`. Las del flow usan una base temporal de MLflow, así que no escriben en el servidor del curso.

## Configuración

Todo lo que puede cambiar vive en `configs/config.yaml`:

| Clave | Para qué |
|---|---|
| `datos.ruta` | CSV que lee el flow, relativo a `actividades/actividad-1` |
| `division` | `test_size` y `random_state` (la semilla también se registra en MLflow) |
| `modelo` | `tipo` (`logistic_regression` o `gradient_boosting`) y `parametros` del estimador de sklearn |
| `mlflow.tracking_uri` | Servidor de MLflow (`http://localhost:5000` con `services/`). Sin servidor, `sqlite:///mlflow.db` |
| `mlflow.experimento` | Experimento donde se agrupan los runs |
| `mlflow.nombre_run` | Nombre de cada run dentro del experimento |
| `metricas.umbral` | Probabilidad a partir de la cual se predice churn (`Exited = 1`). Se registra como parámetro del run |

Si defines `MLFLOW_TRACKING_URI`, esa variable tiene prioridad sobre `mlflow.tracking_uri`.

## Datos: scripts

- `scripts/load_data.py`: carga el CSV de `datos.ruta` (o el que pongas en `main()`), valida sus columnas y muestra su tamaño. Es la misma función que usa el flow.
- `scripts/generate_data.py`: genera un CSV sintético con el mismo esquema, con semilla fija. Los parámetros están en `main()`. Escribe `../data/churn_sintetico.csv` y no sobrescribe un archivo que ya exista.

```powershell
poetry run python scripts/load_data.py
poetry run python scripts/generate_data.py
```

## Flows de Prefect

### Prueba de Prefect y MLflow (`flows/prueba_flow.py`)

No usa datos ni entrena nada: suma de 1 a 5 y registra el resultado en MLflow. Sirve para comprobar que ambos servicios responden antes del flow de la actividad. Consulta el paso 3 de la [guía de la actividad](../../docs/actividad-1.md).

```powershell
$env:PREFECT_API_URL = "http://localhost:4200/api"
$env:MLFLOW_TRACKING_URI = "http://localhost:5000"
poetry run python flows/prueba_flow.py
```

El run `prueba` debe quedar en **Completed** en http://localhost:4200/runs, y el experimento `prueba-validacion` debe tener un run en http://localhost:5000.

### Experimento de la actividad (`flows/experimento_flow.py`)

Tres pasos:

1. **Cargar datos**: lee el CSV de `datos.ruta` con `scripts/load_data.py`.
2. **Entrenar y registrar**: divide los datos en entrenamiento y prueba (estratificado), entrena el modelo elegido en `modelo.tipo`, calcula AUC, accuracy, precision, recall y F1 sobre la prueba, y registra parámetros, métricas y el modelo en MLflow.
3. **Resumen**: crea un artefacto Markdown en Prefect con el modelo, el número de filas, el AUC, el recall y el ID del run.

Antes de ejecutarlo, levanta MLflow y Prefect desde `services/` (`docker compose up -d`). Luego, desde `actividades/actividad-1`:

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

Es importante definir `PREFECT_API_URL`: si no está, Prefect crea un servidor temporal y el run no aparece en http://localhost:4200. Cada ejecución crea un run nuevo: aparece en http://localhost:4200/runs y el experimento en http://localhost:5000.

Si MLflow responde con `Cannot set a deleted experiment`, el experimento de `mlflow.experimento` está borrado en el servidor. Restáuralo desde la UI de MLflow o cambia `mlflow.experimento` en el config.

## Notebooks

- `notebooks/eda_churn.ipynb`: análisis exploratorio. Revisa la calidad de los datos, la distribución de cada variable, la asociación con `Exited`, los outliers y las correlaciones. Termina con los riesgos de fuga de información y los próximos pasos.
- `notebooks/train.ipynb`: replica el experimento del flow paso a paso, sin funciones ni `@task`/`@flow`, para seguir cada operación. No importa nada del proyecto, así que lee el config directamente con `yaml`. Requiere MLflow en marcha para la sección de registro.
- `notebooks/mock_mlflow.ipynb`: **no entrena nada**. Registra un experimento con métricas fijas y un modelo falso en el Model Registry, y lo carga de nuevo. Sirve para comprobar la conexión con MLflow.

Los notebooks de MLflow usan `MLFLOW_TRACKING_URI` o, si no está definida, `http://localhost:5000`, así que MLflow debe estar en marcha antes de ejecutarlos.

## Notas sobre los datos

- Los datos vienen de `actividades/data/Customer-Churn-Records.csv` (10 000 clientes, objetivo `Exited`, sin nulos).
- Las columnas `RowNumber`, `CustomerId` y `Surname` son identificadores y no se usan en el modelo.
- `Complain` coincide con `Exited` en 9 966 de 10 000 filas: es una fuga de datos. Por eso el AUC sale ≈ 0.999 y no es realista. Se mantiene en el modelo para que el experimento sea reproducible; quitarla es una decisión pendiente.