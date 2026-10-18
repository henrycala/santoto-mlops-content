# Actividad 2: pipelines de entrenamiento e inferencia, y API

Proyecto de la actividad 2: pipeline de entrenamiento y pipeline de inferencia en Prefect, conectados por el alias `champion` en MLflow, y una API de FastAPI que sirve el modelo.

Los servicios (MLflow y Prefect) no están en esta carpeta: se levantan desde [`services/`](../../services/README.md).

## Estructura

```
actividad-2/
├── configs/
│   ├── config.yaml            # datos, división, modelo, MLflow, registro e inferencia
│   └── features.yaml          # variables del experimento: ALL, NUMERIC o CUSTOM
├── domain/
│   └── modelo.py              # lógica del modelo: variables, pipeline y métricas (sin Prefect ni MLflow)
├── scripts/
│   └── load_data.py           # carga del CSV con validación de columnas
├── infraestructure/
│   ├── flows/
│   │   ├── entrenamiento_flow.py   # pipeline de entrenamiento
│   │   ├── inferencia_flow.py      # pipeline de inferencia (se ejecuta cada día)
│   │   └── desplegar.py            # registra los despliegues en Prefect
│   └── api/
│       └── main.py            # API de FastAPI que sirve el modelo champion
├── poetry.lock                # versiones exactas resueltas (no editar a mano)
└── pyproject.toml             # dependencias declaradas con versión fijada
```

El CSV de entrada está en `actividades/data/Customer-Churn-Records.csv`, y las predicciones diarias se guardan en esa misma carpeta.

## Requisitos

- Python entre 3.12 y 3.14.
- Poetry 2.x.
- Los servicios de MLflow y Prefect levantados desde `services/`.

## Entorno

Desde `actividades/actividad-2`:

```powershell
poetry install
```

## Variables de entorno

Define estas variables en cada terminal donde ejecutes un flow o la API:

```powershell
$env:PREFECT_API_URL = "http://localhost:4200/api"
$env:MLFLOW_TRACKING_URI = "http://localhost:5000"
```

`MLFLOW_TRACKING_URI` tiene prioridad sobre `mlflow.tracking_uri` de `configs/config.yaml`.

**Ejecuta todos los comandos desde la raíz de `actividad-2`.** Las rutas de la configuración (`configs/config.yaml`, `configs/features.yaml`, `../data/...`) se resuelven desde la carpeta donde estás.

## 1. Entrenamiento

Entrena el modelo, lo registra en MLflow y, si supera el umbral mínimo y el AUC del champion actual, le asigna el alias `champion`:

```powershell
poetry run python infraestructure/flows/entrenamiento_flow.py
```

Al terminar, la consola muestra el resultado. Por ejemplo:

- `Versión 1 registrada como champion (AUC 0.9992)`: el modelo pasó a ser champion.
- `AUC ... no supera al champion ...`: el run queda en MLflow, pero el alias no cambia.
- `AUC ... por debajo del mínimo ...`: el modelo no se registra como champion.

El flow hace tres tareas: `cargar_datos`, `entrenar_y_registrar` y `promover_si_mejora`.

**Dónde verlo:**

- En MLflow (http://localhost:5000), experimento `churn-training-mlops`, run `churn-training`. Tiene el tag `fase = entrenamiento`, los parámetros (`modelo`, sus hiperparámetros, `semilla`, `umbral`, `features`, `n_features`), las métricas (`auc`, `accuracy`, `precision`, `recall`, `f1`) y el modelo como artefacto.
- En MLflow, en el Model Registry, el modelo `churn-modelo` tiene el alias `champion` y el tag `estado = aprobado` en su versión.
- En Prefect (http://localhost:4200/runs), el flow `entrenamiento-churn`.

### Cambiar las variables del experimento

Edita `configs/features.yaml`:

- `ALL`: todas las variables.
- `NUMERIC`: solo las numéricas.
- `CUSTOM`: solo las que listes en `custom`. Los nombres deben coincidir con las columnas del CSV.

El modelo se entrena solo con las variables seleccionadas, y el run registra el alias en el parámetro `features`.

### Cambiar el modelo o sus hiperparámetros

Edita `modelo` en `configs/config.yaml`. El umbral mínimo para ser champion está en `registro.umbral_auc`, y el umbral de clasificación (probabilidad a partir de la que se predice churn) en `metricas.umbral`.

## 2. Inferencia

Carga el modelo `champion`, puntúa un lote de clientes, guarda las predicciones y registra un run en MLflow:

```powershell
poetry run python infraestructure/flows/inferencia_flow.py
```

Necesitas un champion registrado: ejecuta antes el entrenamiento.

- **Lote:** `inferencia.tamano_lote` clientes tomados al azar del CSV. Como simulación de clientes nuevos, el lote cambia en cada ejecución.
- **Predicciones:** se guardan en `actividades/data/prediccion_<fecha>.csv`. Cada fila tiene las columnas del cliente, la columna `Exited` del CSV original, `probabilidad_churn` y `prediccion` (1 si predice abandono). Estos archivos no se versionan en Git.
- **Run en MLflow:** experimento `churn-training-mlops`, run `inferencia-<fecha>`. Tiene las tags `fase = inferencia`, `modelo_version` (versión del champion usada) y `modelo_run_id` (run de entrenamiento de esa versión); las métricas `filas_predichas` y `probabilidad_media`; y el CSV de predicciones como artefacto.
- **Columnas del modelo:** la inferencia usa las mismas columnas con las que se entrenó el champion, aunque `features.yaml` haya cambiado después.

## 3. Despliegues en Prefect

Registra dos despliegues y mantén la terminal abierta:

```powershell
poetry run python infraestructure/flows/desplegar.py
```

- `entrenamiento-churn/entrenamiento-churn`: sin horario. Se lanza a mano.
- `inferencia-churn/inferencia-diaria`: se ejecuta todos los días a las 06:00 en hora UTC (cron `0 6 * * *`).

Mientras la terminal esté abierta, Prefect puede lanzar las ejecuciones. Si la cierras, las ejecuciones programadas no se lanzan.

Para lanzar un despliegue a mano, desde otra terminal con las variables definidas:

```powershell
poetry run prefect deployment run "entrenamiento-churn/entrenamiento-churn"
poetry run prefect deployment run "inferencia-churn/inferencia-diaria"
```

También puedes lanzarlos desde la UI de Prefect, en http://localhost:4200/deployments.

## 4. API de inferencia

La API carga el champion al arrancar. Si el entrenamiento asigna un champion nuevo, reinicia la API.

```powershell
poetry run uvicorn infraestructure.api.main:app --port 8000
```

- Documentación interactiva: http://localhost:8000/docs
- Estado y versión del modelo: http://localhost:8000/health
- Predicción para un cliente: `POST http://localhost:8000/predict`

Ejemplo de predicción desde PowerShell, en otra terminal:

```powershell
$cliente = @{
    CreditScore = 619; Geography = "France"; Gender = "Female"; Age = 42
    Tenure = 2; Balance = 0.0; NumOfProducts = 1; HasCrCard = 1
    IsActiveMember = 1; EstimatedSalary = 101348.88; Complain = 1
    "Satisfaction Score" = 2; "Card Type" = "DIAMOND"; "Point Earned" = 464
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/predict -Method Post -ContentType "application/json" -Body $cliente
```

La respuesta incluye `probabilidad_churn`, `prediccion` (1 si el cliente abandona, 0 si no) y `version_modelo`.

La API recibe todas las columnas del cliente aunque el modelo use solo algunas, según `features.yaml`; usa solo las que necesita el champion.

## Orden recomendado

1. Levantar los servicios desde `services/`.
2. Entrenar: `infraestructure/flows/entrenamiento_flow.py`.
3. Inferir: `infraestructure/flows/inferencia_flow.py`.
4. Desplegar en Prefect: `infraestructure/flows/desplegar.py`.
5. Levantar la API: `infraestructure.api.main:app`.

## Solución de problemas

- **`Registered Model with name=churn-modelo not found`:** no hay champion todavía. Ejecuta el entrenamiento y revisa que el AUC supere `registro.umbral_auc`. Con `features.yaml` en `CUSTOM` el AUC puede bajar del umbral.
- **`ModuleNotFoundError: No module named 'scripts'`:** ejecuta `poetry install` de nuevo desde `actividad-2`, para que los paquetes `scripts`, `domain` e `infraestructure` queden instalados.
- **La API no encuentra el modelo al arrancar:** entrena primero y revisa que `MLFLOW_TRACKING_URI` apunte al servidor correcto.
- **`httpx.InvalidURL: Invalid non-printable ASCII character in URL, '\n'`:** la variable `PREFECT_API_URL` tiene un salto de línea al final, probablemente por haberla copiado con un salto. Comprueba su longitud con `$env:PREFECT_API_URL.Length`: debe ser `25`. Si no lo es, vuelve a definirla en una terminal nueva con `$env:PREFECT_API_URL = "http://localhost:4200/api"` y revisa que `$env:MLFLOW_TRACKING_URI.Length` sea `21`.
- **La UI de Prefect no muestra despliegues:** ejecuta `desplegar.py` con `PREFECT_API_URL` definida y deja la terminal abierta.
