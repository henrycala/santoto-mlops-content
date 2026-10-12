# Calendario del curso: sesiones y entregas

**Periodo:** semana 11 (12 oct 2026) a semana 17 (semana del 23 al 29 nov 2026)
**Sesiones:** 15 horas en total, 8 sesiones
**Hora límite de entregas:** 23:59, hora de Colombia (UTC-5)

## Resumen por módulo

| Módulo | Semanas | Sesiones | Horas | Actividades |
|--------|---------|----------|-------|-------------|
| 1. Fundamentos y gestión del ciclo de vida | 11 – 12 | S1, S2, S3 | 6 h | A1 |
| 2. Pipelines, entrenamiento automatizado y despliegue | 13 – 14 | S4, S5 | 4 h | A2 |
| 3. Operaciones, monitoreo y CI/CD | 15 – 16 | S6, S7 | 4 h | A3, A4 |
| Integración y cierre | 17 | S8 | 1 h | Charlas finales A4 |

## Contenido por sesión

### S1. Miércoles 14 de octubre (2 h) · Semana 11
**Tema:** Introducción a MLOps

- De Data Science a MLOps: por qué un modelo en un notebook no es un sistema.
- Etapas del ciclo de vida: desarrollo, despliegue y operación.
- Retos de reproducibilidad, escalabilidad y mantenimiento.
- Panorama del ecosistema de herramientas. Se presenta Prefect y MLflow como stack del curso.

### S2. Jueves 15 de octubre (2 h) · Semana 11
**Tema:** Versionamiento, entornos y estructura de proyectos

- Control de versiones con Git y GitHub: ramas, commits y pull requests.
- Control de entornos: `requirements.txt`, Poetry y fijación de versiones.
- Estructuración profesional de un proyecto ML (`src/`, `flows/`, `configs/`, `tests/`).


### S3. Jueves 22 de octubre (2 h) · Semana 12
**Tema:** Registro de experimentos y reproducibilidad & Pipelines en Prefect

- Registro de experimentos: métricas, parámetros y artefactos.
- MLflow Tracking: comparación de runs y autolog.
- Introducción a Prefect.

**Hito:** el **domingo 25 de octubre, 23:59**, se entrega **A1**.

### S4. Jueves 29 de octubre (2 h) · Semana 13
**Tema:** Pipelines en Prefect

- Concepto de pipeline y modularidad: steps, artifacts y parámetros.
- Separación entre datos, código y configuración.
- Validación de datos con fallo controlado (`@retry`, `@catch` o `raise`).


### S5. Jueves 5 de noviembre (2 h) · Semana 14
**Tema:** Modelos, empaquetado y servicio

- Serialización: pickle y joblib frente a MLflow Models (signature, pyfunc).
- Model Registry: versiones, alias `champion` y promoción de modelos.
- Servicio de inferencia: `mlflow models serve` y una API mínima con FastAPI.
- Contenerización con Docker (conceptos; el ejercicio es opcional).

**Hito:** el **domingo 8 de noviembre, 23:59**, se entrega **A2**.

### S6. Jueves 12 de noviembre (2 h) · Semana 15
**Tema:** Monitoreo y drift

- Data drift y model drift: qué son y cómo se miden.
- Seguimiento del rendimiento en producción.
- Evidently AI: reportes de drift por lote.
- Reentrenamiento programado frente a reentrenamiento disparado por un umbral.


### S7. Jueves 19 de noviembre (2 h) · Semana 16
**Tema:** CI/CD, calidad, equidad y gobernanza

- Principios de CI/CD.
- Tests de datos, modelos y pipelines. *Quality gate*.
- Sesgos y equidad: análisis por subgrupos.
- Gobierno del modelo: aprobaciones, auditoría y documentación.
- Escalabilidad, resiliencia y costos (conceptual).

**Hito:** el **domingo 22 de noviembre, 23:59**, se entrega **A3**.

### S8. Jueves 26 de noviembre (1 h) · Semana 17
**Tema:** Discusiones finales y cierre

- Cierre: lecciones aprendidas, retroalimentación e Introducción a AIOps.

**Hito:** entrega de **A4** el **sábado 28 de noviembre, 23:59**. Presentaciones: fecha por definir (ver decisiones).

## Entregas

| Actividad | Asignación | Entrega | Días disponibles | Tipo de entrega |
|-----------|-----------|---------|------------------|-----------------|
| A1: Fundamentos y tracking | S2 · jue 15 oct | dom 25 oct, 23:59 | 10 | Repositorio + memoria 1 |
| A2: Pipeline y empaquetado | S4 · jue 29 oct | dom 8 nov, 23:59 | 10 | Repositorio + memoria 2 |
| A3: Monitoreo, CI/CD y gobernanza | S6 · jue 12 nov | dom 22 nov, 23:59 | 10 | Repositorio con CI + memoria 3 |
| A4: Sistema end-to-end | S6 · jue 12 nov | sáb 28 nov, 23:59 | 16 | Repositorio integrado + slides |
