# santoto-mlops-content

Solución de referencia de las actividades 1 a 3 del curso **MLOps con Metaflow y MLflow**.
Cada actividad está en su propia carpeta y es un proyecto completo y ejecutable:

| Actividad | Carpeta | Contenido |
|---|---|---|
| 1. Fundamentos, versionamiento y tracking | [actividades/actividad-1](./actividades/actividad-1) | Estructura del proyecto, carga del dataset de churn, primer flow de Metaflow y tracking en MLflow |
| 2. Pipeline y empaquetado | [actividades/actividad-2](./actividades/actividad-2) | Pipeline completo en Metaflow, validación de datos con fallo controlado, registro `champion` y servicio de inferencia |
| 3. Monitoreo, CI/CD y gobernanza | [actividades/actividad-3](./actividades/actividad-3) | Lotes con drift, reporte de drift, reentrenamiento por umbral, CI con quality gate, análisis de equidad y nota de gobernanza |

Cada carpeta se construye sobre la anterior: la actividad 2 contiene lo de la 1 transformado en pipeline, y la 3 contiene todo lo anterior más el monitoreo.

## Servicios

MLflow y Metaflow se levantan desde [`services/`](./services/README.md):

- **MLflow:** `docker compose up -d` en `services/` (Docker Desktop abierto). Interfaz en http://localhost:5000.
- **Metaflow:** `./metaflow/start.sh` en `services/`, desde WSL2 o Linux (Metaflow no funciona en Windows nativo, porque usa `fcntl`).

Cada actividad documenta cómo ejecutar sus flows en su propio README.

## Supuestos generales

- **Stack núcleo:** Metaflow (orquestación) y MLflow (tracking, registro y servicio).
- **Datos:** dataset real de abandono de clientes (churn) en `actividades/data/Customer-Churn-Records.csv`, con 10 000 filas.
- **Sin modelos preentrenados:** el modelo se entrena desde cero con scikit-learn.

## Configuración

Cada actividad tiene su `configs/config.yaml`. Los datos, el modelo, los umbrales y el tracking se cambian ahí, no en el código. Por ejemplo, para cambiar de modelo se edita la sección `modelo`.

## Memoria de actividad

Cada actividad debe entregarse con una memoria siguiendo la [plantilla](./docs/plantilla-memoria.md) del curso.
