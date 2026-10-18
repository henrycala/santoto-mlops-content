# Actividad 1: Fundamentos, versionamiento y tracking

**Módulo:** 1. Fundamentos de MLOps y Gestión del Ciclo de Vida
**Entregable:** repositorio Git con código + memoria 1 (ver [plantilla](./plantilla-memoria.md))

## Objetivo

Construir la base reproducible del proyecto: estructura de código, entorno controlado, datos dummy versionables y un primer experimento registrado con trazabilidad.

## Temas del módulo que cubre

- Control de versiones con Git/GitHub.
- Control de entornos (requirements, Conda o Poetry).
- Estructuración profesional de proyectos ML.
- Registro de experimentos: métricas, parámetros y artefactos.
- Reproducibilidad y auditoría del proceso experimental.

## Actividades (Pasos recomendados)

### Paso 1. Estructura y entorno

Trabajarás con un repositorio nuevo, creado desde cero. Antes de empezar, instala:

| Herramienta | Versión | Para qué | Cómo comprobarlo |
|---|---|---|---|
| Python | 3.12 a 3.14 | Intérprete del proyecto | `python --version` |
| Poetry | 2.x | Gestiona dependencias, `pyproject.toml` y `poetry.lock` | `poetry --version` |
| Git | reciente | Control de versiones | `git --version` |
| Docker Desktop | reciente | Solo para levantar MLflow y Prefect con `services/` | `docker --version` |

Para instalar Poetry en Windows (PowerShell), usa el instalador oficial:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Si el comando `poetry` no se reconoce al terminar, añade a `PATH` la carpeta de scripts que indica el instalador, cierra la terminal y vuelve a abrirla. Alternativa: `pip install poetry`.

**Crear el repositorio (grupos de 3):**

El grupo trabaja sobre un único repositorio de GitHub. Un integrante lo crea, agrega a los demás como colaboradores y sube la estructura inicial. Los demás solo lo clonan.

1. **Crear el repositorio en GitHub** (lo hace un integrante, desde el navegador):

   1. Entra en https://github.com/new.
   2. En **Repository name**, agrega el nombre de tu proyecto `PROJECTO_DE_EQUIPO`.
   3. Marca **Add a README file**.
   4. En **Add .gitignore**, elige la plantilla **Python**.
   5. Pulsa **Create repository**.

2. **Agregar a los integrantes del grupo como colaboradores** (lo hace el mismo integrante):

   1. En el repositorio, entra en **Settings → Collaborators** (en el menú lateral, en *Access*).
   2. Pulsa **Add people**, escribe el usuario de GitHub de cada compañero y elige **Add**.
   3. Cada compañero debe aceptar la invitación que le llega por correo o en GitHub (**Notifications**) antes de poder hacer `push`.

3. **Clonar el repositorio en tu computador** (dueño del repositorio). Desde PowerShell, en la carpeta donde guardas tus proyectos:

   ```powershell
   git clone URL_DEL_REPOSITORIO.git
   cd MY_REPO
   ```

4. **Crear la estructura y el entorno** (lo hace un integrante y sube los cambios). Git no versiona carpetas vacías, así que cada una lleva debe llevar un archivo init.py

5. Añade al `.gitignore` las carpetas que no se versionan y que la plantilla de Python no cubre: `mlruns/`, `mlflow.db` y `mlflow_store/`.

6. Genera `pyproject.toml` sin preguntas y fija la versión de Python del entorno:

   ```powershell
   poetry init --no-interaction --name mi-proyecto-mlops --python ">=3.12,<3.15"
   poetry env use 3.12
   ```

   Si `poetry env use 3.12` falla, instala Python 3.12 o indica la ruta completa a su `python.exe`.

7. Añade las dependencias con versión fijada (`==`). Cada `poetry add` actualiza `pyproject.toml`, escribe las versiones resueltas en `poetry.lock` e instala en el entorno virtual:

   ```powershell
   poetry add "prefect==3.8.8" "mlflow==3.17.0" "scikit-learn==1.9.1" "pandas==3.0.6" "numpy==2.5.4" "pyyaml==6.0.3"
   poetry add --group dev "pytest==9.1.1"
   ```

8. Si `poetry install` falla con un error sobre archivos de instalación, abre `pyproject.toml` y añade, debajo de `[tool.poetry]`, la línea `package-mode = false`. El proyecto no es una librería, así que no hace falta empaquetarlo.

9. Escribe el README con los pasos de ejecución y sube los cambios. `pyproject.toml` y `poetry.lock` deben estar en el repositorio:

   ```powershell
   git add .
   git commit -m "chore: estructura inicial y entorno con Poetry"
   git push
   ```

**Clonar y preparar el entorno (los demás integrantes):**

1. Clona el repositorio con el enlace que aparece en la página de GitHub (botón verde **Code → HTTPS**):

   ```powershell
    git clone URL_DEL_REPOSITORIO.git
    cd MY_REPO
   ```

2. Crea el entorno desde `poetry.lock` y comprueba que funciona:

   ```powershell
   poetry install
   poetry run python -c "import prefect, mlflow, sklearn; print('ok')"
   ```

   Si el lock no coincide con `pyproject.toml`, Poetry avisa de que hay que ejecutar `poetry lock`. Eso lo hace solo quien cambió las dependencias.

**Evidencia:** repositorio en GitHub con los tres integrantes como colaboradores, `pyproject.toml`, `poetry.lock` y README; y `poetry install` funcionando en la clonación de cada integrante.

**Qué debe entender el alumno:**

- `pyproject.toml` declara lo que se necesita. `poetry.lock` registra lo que se instaló. Se versionan los dos y no se edita el lock a mano.
- `poetry run` ejecuta un comando dentro del entorno virtual sin activarlo.
- Para reproducir el entorno, otra persona clona el repo y ejecuta `poetry install`; no necesita volver a añadir dependencias.

### Paso 2. Caso de uso

Cada grupo va a desarrollar un modelo de machine learning a lo largo del curso. El cual puede ser:

- Un problema propio de su área de trabajo.
- Un caso de estudio público, como los datasets de Kaggle.

En esta actividad no es necesario implementar la lógica específica del caso de uso (preprocesado, entrenamiento, métricas). Se recomienda, sin embargo, empezar por el cargue de datos, de modo que la pipeline del paso 4 ya trabaje con datos reales o generados.

Para preparar los datos, el grupo puede elegir entre dos opciones:

- **Datos sintéticos:** un script `generate_data.py` puede generar el dataset con una semilla fija (`random_state`) y parámetros documentados (número de filas, columnas, proporción de la clase objetivo, etc.). Con la misma semilla, el resultado es igual en cada ejecución.
- **Dataset real:** un script `load_data.py` puede leer un CSV (por ejemplo, descargado de Kaggle o del área de trabajo), comprobar que tiene las columnas esperadas y devolverlo listo para usar. Si el archivo es grande, puede quedar fuera de Git; en ese caso conviene documentar de dónde sale y cómo descargarlo.

Cualquiera de los dos scripts puede vivir en el repositorio y ejecutarse con `poetry run python`. Si se usa, es recomendable que el flow del paso 4 llame a esa función en lugar de escribir rutas a mano.

### Paso 3. Levantar los servicios y comprobar Prefect

MLflow (tracking y registro de modelos) y Prefect (orquestación de flows) se ejecutan desde [`services/`](../services/README.md)

1. Abre Docker Desktop y, desde la ruta `services/`, ejecuta `docker compose up -d`. Si Docker no funciona, usa la opción B de la guía de servicios (sin Docker). No uses las dos a la vez.
2. Comprueba que los servicios responden:
   - http://localhost:5000: debe cargar la UI de MLflow.
   - http://localhost:4200: debe cargar la UI de Prefect.
3. Antes de la pipeline de la actividad, puedes ejecutar `flows/prueba_flow.py`. Es un flow corto que comprueba que Prefect recibe runs y que MLflow registra experimentos.

   Este archivo no viene en el repositorio que creaste en el paso 1. Cópialo desde `actividades/actividad-1/flows/prueba_flow.py` del repositorio del curso a la carpeta `flows/` de tu repositorio (si la carpeta no existe, créala). Después, desde la raíz de tu repositorio:

   ```powershell
   $env:PREFECT_API_URL = "http://localhost:4200/api"
   $env:MLFLOW_TRACKING_URI = "http://localhost:5000"
   poetry run python flows/prueba_flow.py
   ```

4. En http://localhost:4200/runs, el run `prueba` aparece con estado **Completed**. En sus logs aparece `Suma de 1 a 5 = 15`, porque el flow tiene `log_prints=True`.
5. En http://localhost:5000, el experimento `prueba-validacion` tiene un run `prueba-mlflow` con el parámetro `n` y la métrica `suma`.

**Evidencia sugerida:** captura de las dos UIs y de los dos runs (Prefect y MLflow).

> **Hasta este paso es suficiente para completar la actividad 1.** Lo que sigue (la pipeline de entrenamiento y el tracking del modelo) forma parte del trabajo del grupo a lo largo del curso, pero no es necesario para cerrar esta actividad. Basta con tener el repositorio y el entorno del paso 1 y los servicios validados con `flows/prueba_flow.py`.

### Paso 4 (Opcional). Primera pipeline de entrenamiento en Prefect

El repositorio incluye una pipeline de entrenamiento de ejemplo, `flows/experimento_flow.py`, para que se vea cómo se conectan Prefect y MLflow. No es el trabajo final del grupo: lo esperado es que cada equipo cree su propia pipeline de entrenamiento, adaptada a su caso de uso. La de ejemplo tiene tres tareas:

1. **Cargar datos:** lee el CSV indicado en `configs/config.yaml` y valida sus columnas.
2. **Entrenar:** divide los datos en entrenamiento y prueba, entrena el modelo y calcula las métricas (AUC, recall, etc.). Después registra el run en MLflow (ver paso 5).
3. **Resumen:** crea un artefacto Markdown en Prefect con el modelo, el número de filas, las métricas y el ID del run de MLflow.

Ejecútalo desde `actividades/actividad-1` con las dos variables de entorno definidas en la misma terminal:

```powershell
$env:PREFECT_API_URL = "http://localhost:4200/api"
$env:MLFLOW_TRACKING_URI = "http://localhost:5000"
poetry run python flows/experimento_flow.py
```

En http://localhost:4200/runs, el run `experimento-a1` debe quedar en estado **Completed**. Revisa sus tareas, sus logs y el artefacto **Experimento A1**.

Si tu equipo crea su propia pipeline, puedes usar la de ejemplo como referencia para la estructura de tareas y para el registro en MLflow.


## Criterio de éxito

Otra persona clona el repositorio, instala el entorno y reproduce el experimento.

## Caso de uso

Como propuesta ideal, se espera que el estudiante plantee un desafío propio de su área de desempeño en el que sea viable aplicar técnicas de Machine Learning, ya sea mediante modelos de clasificación, regresión o forecasting. En caso de no contar con una problemática definida, se podrá optar por un caso de estudio simulado utilizando conjuntos de datos públicos de Kaggle. https://www.kaggle.com/datasets

## Entregables

Obligatorios para completar la actividad 1:

- [ ] Repositorio en GitHub, con los integrantes como colaboradores, estructura de carpetas y README.
- [ ] `pyproject.toml` y `poetry.lock` versionados, y `poetry install` funcionando en una clonación limpia de cada integrante.
- [ ] Servicios de MLflow y Prefect validados con `flows/prueba_flow.py`, con capturas del run `prueba` en Prefect y del experimento `prueba-validacion` en MLflow.
- [ ] Memoria 1 completa.

Recomendados (no son necesarios para cerrar la actividad 1):

- [ ] Script de datos (`generate_data.py` o `load_data.py`) con semilla o ruta documentada, y registro del tamaño del dataset en los logs de Prefect y en MLflow (paso 2).
- [ ] Pipeline de entrenamiento propia del grupo en Prefect, con capturas de sus runs, logs y artefactos (paso 4).


## Recursos:
- Libro Guía (Capitulos 1 y 2): https://soclibrary.futa.edu.ng/books/Reliable%20Machine%20Learning%20(Chen,%20CathyMurphy,%20Niall%20RichardParisa%20etc.)%20(Z-Library).pdf

- Documentación especifica:
    - Version control: https://git-scm.com/book/en/v2
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
