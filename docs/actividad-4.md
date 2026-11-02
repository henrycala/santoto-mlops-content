# Actividad 4: Reflexión sobre el sistema MLOps (actividades 1 a 3)

**Módulo:** Integración de los módulos 1 a 3
**Extensión:** máximo 2 páginas

## 1. Qué implementamos en las actividades 1 a 3

**Actividad 1: fundamentos, versionamiento y tracking.** Estructura del repositorio con Poetry y versiones fijadas de las dependencias, para que cualquiera reproduzca el entorno. Caso de uso de churn (abandono de clientes) sobre el dataset `Customer-Churn-Records.csv`, con carga reproducible de los datos. Servicios levantados con Docker Compose (MLflow en `localhost:5000`) y Prefect para orquestar la primera pipeline de entrenamiento.

**Actividad 2: pipeline y empaquetado.** Pipeline de entrenamiento en Prefect que compara tres modelos (regresión logística con dos valores de C y gradient boosting) con dos conjuntos de variables (todas y un subconjunto). Cada combinación se registra como un run en MLflow. Solo el de mayor AUC se evalúa para ser champion: debe superar un AUC mínimo y al champion actual. Pipeline de inferencia que carga el champion desde el Model Registry, y una API con FastAPI (`/health` y `/predict`), más el despliegue del flow en Prefect.

**Actividad 3: monitoreo, drift y CI.** Flow de inferencia que puntúa un lote con drift emulado (fracción configurable de variables desplazadas y subida de la tasa de churn). Dos flows de monitoreo sobre ese lote: drift de features con Evidently (reporte HTML y alerta si la fracción de variables con drift supera un umbral) y drift del target con un test chi-cuadrado sobre la tasa de `Exited`. Tests unitarios de la lógica de drift y de la API, ejecutados en GitHub Actions en cada PR. Al cierre de la actividad, la suite tiene 17 tests y pasa en local.

La lógica de drift vive en `domain/` y no depende de MLflow, Prefect ni Evidently, así que se puede probar sin servicios levantados. Los flows solo orquestan.

## 2. Mayores dificultades

[Completar: los obstáculos reales del grupo, con cómo se resolvieron. Por ejemplo: configuración de servicios, versiones de dependencias, depuración de la API o de los flows, interpretación de los resultados de drift.]

## 3. Temas que más gustaron

[Completar: qué parte del módulo les resultó más útil o interesante, y por qué.]

## 4. Temas que les hubiera gustado profundizar

[Completar: temas que quedaron superficiales, por ejemplo: reentrenamiento automático por umbral, equidad, despliegue en la nube, monitoreo en producción.]
