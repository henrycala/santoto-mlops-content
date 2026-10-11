# Actividad 4: Presentación del sistema MLOps end-to-end

**Módulo:** Integración de los módulos 1 a 3
**Entregable:** repositorio integrado + presentación de slides (15 a 18 diapositivas, 20 minutos de exposición + preguntas)

## Objetivo

Presentar el sistema construido en las actividades 1 a 3 como una solución de negocio: qué problema resuelve, cómo se ejecutó, cómo se opera, qué KPIs se observaron y qué impacto tendría. Cada slide debe apoyarse en una evidencia producida en las actividades anteriores.

## Relación con las actividades anteriores

| Actividad | Aporte a la presentación |
|-----------|--------------------------|
| 1 | Estructura del repositorio, datos reproducibles y tracking de experimentos (MLflow) |
| 2 | Pipeline automatizado (Metaflow), registro de modelos y servicio de inferencia |
| 3 | Monitoreo de drift, reentrenamiento, CI con quality gate y análisis de equidad |

## Tareas

1. **Integrar el repositorio.** Unificar las partes de las actividades 1 a 3 en un solo proyecto con un README de ejecución.
2. **Ejecutar el flujo completo** y guardar evidencias: dato nuevo → predicción → monitoreo → reentrenamiento → nuevo despliegue.
3. **Medir los KPIs** técnicos y de negocio definidos en la sección de KPIs.
4. **Construir la presentación** con la estructura de abajo.

## Estructura de la presentación

La presentación se organiza en cinco bloques, en este orden. Cada bloque responde una pregunta.

### Bloque A. Caso de negocio (3 slides)

| Slide | Mensaje principal | Contenido | Evidencia |
|-------|-------------------|-----------|-----------|
| 2 | Perder clientes tiene un costo medible | Problema de churn, tasa de abandono base y costo por cliente perdido (cifras supuestas y declaradas) | Supuestos documentados en el repositorio |
| 3 | Qué significa éxito para el negocio | Objetivo de negocio y KPI principal, por ejemplo, reducir el churn en un porcentaje definido | Definición del KPI en el README |
| 4 | Predecir a tiempo permite actuar | Propuesta de solución en una sola idea: identificar clientes en riesgo para intervenir antes de que se vayan | Diagrama simple del flujo de decisión |

### Bloque B. Ejecución del proyecto (4 slides)

| Slide | Mensaje principal | Contenido | Evidencia |
|-------|-------------------|-----------|-----------|
| 5 | El sistema es un flujo, no un modelo | Arquitectura end-to-end: datos, Metaflow, MLflow, servicio, monitoreo y CI | Diagrama de arquitectura |
| 6 | Los datos son reproducibles y controlables | Generador con semilla, esquema y drift inyectado de forma controlada | Parámetros del generador y ejemplo de lote |
| 7 | El pipeline se ejecuta y valida solo | Pasos del flow de Metaflow y validación de datos con fallo controlado | Captura de Metaflow Card o salida de terminal |
| 8 | El modelo campeón se eligió con evidencia | Comparación de runs en MLflow y justificación del modelo elegido | Captura de la comparación de runs |
| 9 | Un solo alias controla qué modelo sirve | Registro en el Model Registry, alias `champion` y servicio de inferencia | Captura del registro y una predicción de ejemplo |

### Bloque C. Operaciones MLOps (3 slides)

| Slide | Mensaje principal | Contenido | Evidencia |
|-------|-------------------|-----------|-----------|
| 10 | El drift se detecta antes de que duela | Reporte de Evidently por lote y variables que cambian | Reporte de Evidently |
| 11 | Ningún cambio degrada el modelo sin bloquearse | Flujo de reentrenamiento y quality gate en CI, con un despliegue bloqueado | Ejecución de CI (bloqueada y aprobada) |
| 12 | El modelo se audita, no solo se entrena | Análisis de equidad por subgrupos y nota de gobernanza | Tabla de métricas por subgrupo |

### Bloque D. KPIs observados (2 slides)

| Slide | Mensaje principal | Contenido | Evidencia |
|-------|-------------------|-----------|-----------|
| 13 | Qué tan bien funciona el sistema | KPIs técnicos: AUC, latencia de inferencia (p95), score de drift, tiempo de reentrenamiento y tasa de despliegues bloqueados | Tabla con valores medidos |
| 14 | Cómo se comporta el modelo con el tiempo | AUC frente al nivel de drift por lote y decisión tomada en cada caso | Gráfico con los lotes de la actividad 3 |

### Bloque E. Impacto de negocio (3 slides)

| Slide | Mensaje principal | Contenido | Evidencia |
|-------|-------------------|-----------|-----------|
| 15 | Cuánto valor puede generar la solución | Impacto estimado con una fórmula explícita (ver abajo) y escenarios optimista, base y pesimista | Hoja de cálculo o script con los supuestos |
| 16 | Qué aprendimos y qué limita el resultado | Lecciones aprendidas y limitaciones, incluyendo que los datos son sintéticos | Sección de problemas de la memoria |
| 17 | Qué haría el equipo a continuación | Próximos pasos priorizados para llevar el sistema a producción real | Lista priorizada |

### Anexo (1 slide, no cuenta en los 18)

| Slide | Contenido |
|-------|-----------|
| 18 | Enlaces a evidencias por actividad y declaración de uso de herramientas de IA (sección 8 de la [plantilla](./plantilla-memoria.md)) |

## Impacto de negocio: fórmula sugerida

Como los datos son sintéticos, el impacto es una **simulación**. Debe presentarse como tal, con los supuestos a la vista:

```
Impacto neto = (clientes en riesgo detectados × tasa de retención con intervención × valor del cliente)
               − costo de la campaña de intervención
```

Los estudiantes deben declarar cada valor (tasa de churn base, valor del cliente, costo por intervención) y presentar tres escenarios.

## Criterios de evaluación

- **Caso de negocio:** el problema y el KPI de negocio están claramente definidos.
- **Ejecución:** la presentación muestra evidencias reales del flujo, no solo diagramas.
- **Operaciones:** se evidencian el monitoreo, el reentrenamiento y al menos un bloqueo por quality gate.
- **KPIs:** los valores están medidos y se interpretan, incluyendo los que salieron mal.
- **Impacto:** los supuestos están declarados y el resultado se presenta como simulación.
- **Diseño:** una idea por slide, texto breve y diagramas legibles.

## Entregables

- [ ] Repositorio integrado con README de ejecución.
- [ ] Presentación de 15 a 18 slides siguiendo la estructura de bloques.
- [ ] Hoja o script con los supuestos del impacto de negocio y sus tres escenarios.
- [ ] Anexo con enlaces a evidencias de las actividades 1 a 3 y declaración de uso de IA.
