# Git: qué es, cuándo usarlo y cuándo no

Git es un sistema de control de versiones: guarda el historial de los cambios de un proyecto para poder revisarlos, compararlos, deshacerlos y trabajar en paralelo sin pisarse. Este documento explica los conceptos básicos con los ejemplos de este proyecto.

## 1. Qué problema resuelve

Sin control de versiones, un proyecto acaba con carpetas como `final`, `final_v2`, `final_DEFINITIVO`. Con Git:

- Cada cambio queda registrado con autor, fecha y mensaje.
- Se puede volver a cualquier versión anterior.
- Varias personas pueden editar el mismo proyecto y combinar sus cambios.
- Se pueden probar ideas en ramas aisladas sin tocar la versión estable.

En MLOps esto importa porque el código, la configuración (`configs/config.yaml`) y las dependencias (`pyproject.toml`, `poetry.lock`) deben corresponder siempre a un mismo experimento reproducible.

## 2. Conceptos clave

### Las tres áreas de trabajo

```
Directorio de trabajo  --git add-->  Staging (índice)  --git commit-->  Repositorio (.git/)
   (archivos editados)                 (cambios preparados)              (historial)
```

- **Directorio de trabajo:** los archivos tal como están en disco.
- **Staging (índice):** los cambios que has seleccionado para el próximo commit.
- **Repositorio:** la carpeta oculta `.git/` con todo el historial.

### Commit

Una fotografía del proyecto en un momento dado, con un mensaje que explica el cambio. Cada commit tiene un identificador único (hash SHA-1 o SHA-256) que depende de su contenido y de su padre. Por eso el historial no se puede alterar en silencio: cambiar un commit cambia todos los siguientes.

### Rama (branch)

Un puntero móvil a un commit. Crear una rama es barato (un archivo de unos bytes). Sirve para aislar trabajo: `main` contiene lo estable y cada experimento vive en su rama hasta que se fusiona.

### Remoto (remote)

Una copia del repositorio en otro sitio (GitHub, GitLab, un servidor del curso). `origin` es el nombre habitual del remoto principal.

### HEAD

El puntero a la rama o commit en el que estás trabajando ahora.

## 3. Características principales

- **Distribuido:** cada clon tiene el historial completo. Puedes hacer commits, ver el historial y crear ramas sin conexión.
- **Instantáneas, no diferencias:** Git guarda el estado de los archivos en cada commit. Las diferencias se calculan al mostrarlas.
- **Integridad:** cada objeto (archivo, árbol, commit) tiene un hash. Un cambio corrupto o malicioso se detecta.
- **Ramas baratas:** crear, cambiar y fusionar ramas es rápido, así que se usa con normalidad.
- **Historial reescribible (con cuidado):** `rebase`, `commit --amend` y `reset` permiten reorganizar commits locales. No deben usarse sobre commits que otros ya tienen.
- **Ignorar archivos:** `.gitignore` indica qué no versionar (entornos virtuales, `mlflow.db`, `mlruns/`, cachés).

## 4. Comandos principales

### Configuración inicial (una vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"
git config --global init.defaultBranch main
```

### Crear o clonar un repositorio

| Comando | Para qué sirve |
|---|---|
| `git init` | Crea un repositorio nuevo en la carpeta actual. |
| `git clone <url>` | Copia un repositorio remoto completo en tu equipo. |

### Trabajo diario

| Comando | Para qué sirve |
|---|---|
| `git status` | Muestra qué archivos cambiaron y en qué área están. Úsalo antes de cada commit. |
| `git diff` | Muestra los cambios no preparados. |
| `git diff --staged` | Muestra los cambios preparados para el próximo commit. |
| `git add <archivo>` | Prepara un archivo para el commit. `git add -p` permite elegir trozos concretos. |
| `git commit -m "mensaje"` | Crea un commit con lo preparado. |
| `git log --oneline --graph` | Muestra el historial de forma compacta. |
| `git restore <archivo>` | Descarta cambios no preparados de un archivo. **Borra cambios sin recuperación.** |
| `git restore --staged <archivo>` | Saca un archivo del staging sin perder sus cambios. |

### Ramas

| Comando | Para qué sirve |
|---|---|
| `git branch` | Lista las ramas locales. |
| `git switch -c <rama>` | Crea una rama nueva y cambia a ella. |
| `git switch <rama>` | Cambia a una rama existente. |
| `git merge <rama>` | Incorpora los cambios de otra rama en la actual. |
| `git branch -d <rama>` | Borra una rama ya fusionada. |

### Remotos

| Comando | Para qué sirve |
|---|---|
| `git remote -v` | Muestra las URL de los remotos. |
| `git fetch` | Descarga cambios del remoto sin modificar tu trabajo. |
| `git pull` | `fetch` + `merge` (o `rebase`) de la rama remota. |
| `git push -u origin <rama>` | Sube la rama al remoto la primera vez. Después basta `git push`. |

### Deshacer cosas

| Comando | Para qué sirve | Cuidado |
|---|---|---|
| `git stash` | Guarda cambios sin commitear para volver después. | Bajo. |
| `git revert <commit>` | Crea un commit que deshace otro. | Seguro: no reescribe historial. |
| `git reset --soft HEAD~1` | Deshace el último commit y deja los cambios preparados. | Medio: solo en commits no publicados. |
| `git reset --hard` | Descarta todos los cambios locales y fuerza el estado de un commit. | **Destructivo.** Pierde trabajo no commiteado. |

### Etiquetas

| Comando | Para qué sirve |
|---|---|
| `git tag -a v0.1.0 -m "Actividad 1"` | Marca un commit concreto, por ejemplo una entrega. |

## 5. Ejemplo de flujo de trabajo en este proyecto

```bash
# 1. Crear una rama para el cambio
git switch -c feat/regularizacion-logistica

# 2. Editar configs/config.yaml (por ejemplo C: 0.5) y ejecutar el flow
poetry run python flows/experimento_flow.py run

# 3. Revisar qué cambió antes de confirmar
git status
git diff

# 4. Preparar y confirmar solo lo que corresponde
git add configs/config.yaml
git commit -m "Ajusta C de la regresión logística a 0.5"

# 5. Subir la rama y fusionarla cuando esté lista
git push -u origin feat/regularizacion-logistica
```

Buenas prácticas de los mensajes de commit: primera línea corta (unos 50 caracteres) en imperativo, y en el cuerpo, si hace falta, el porqué del cambio.

## 6. Cuándo usar Git

- **Siempre que haya código o texto que cambie:** scripts, flows, configuraciones YAML, pruebas, documentación, `pyproject.toml`.
- **Para trabajar en equipo:** ramas por tarea, revisión de cambios (pull requests) y fusión controlada.
- **Para reproducir un experimento:** un commit concreto identifica exactamente el código y las dependencias (junto con `poetry.lock`) que produjeron un resultado. MLflow puede registrar ese commit en cada run.
- **Para recuperar versiones anteriores:** saber qué cambió, cuándo y por qué.
- **Para documentar decisiones:** el historial y los mensajes explican por qué el proyecto está como está.

## 7. Cuándo no usar Git (o usarlo con otra herramienta)

- **Datasets grandes o que cambian a menudo.** Git no está pensado para archivos de cientos de MB que se modifican en cada iteración: el repositorio crece sin control y los clones se vuelven lentos. Para datos y modelos binarios se usan **DVC** (versiona los datos fuera de Git y guarda en Git solo un puntero) o **Git LFS** (almacena archivos grandes aparte, sin cambiar el flujo). En este curso el CSV de churn es pequeño y se versiona directamente; un proyecto real con datos de millones de filas usaría DVC.
- **Modelos entrenados y artefactos binarios.** Para ellos sirve más el registro de modelos de MLflow (`mlruns/`, `mlflow.db`) que Git. Por eso esos archivos están en `.gitignore`.
- **Secretos y credenciales.** Contraseñas, tokens o claves de API no deben entrar nunca al repositorio. Aunque se borren en el siguiente commit, siguen en el historial. Se usan variables de entorno o un gestor de secretos. Si ya se subió algo así, hay que revocarlo, no solo borrarlo.
- **Archivos generados o temporales.** Entornos virtuales (`.venv/`), cachés (`__pycache__/`), salidas de ejecución. Se ignoran con `.gitignore`.
- **Notebooks con salidas.** Los `.ipynb` mezclan código, resultados e imágenes en JSON, y los diffs son ilegibles. Si se versionan, conviene limpiar las salidas (`nbstripout`) o versionar la versión `.py` equivalente.
- **Como copia de seguridad única.** Git guarda lo que se commitea. Lo no commiteado no está protegido, y un remoto mal configurado tampoco es un backup completo.
- **Para colaborar en tiempo real sobre el mismo texto.** Git funciona por commits y fusiones, no por edición simultánea. Para eso sirven herramientas de edición colaborativa, aunque Git siga siendo la fuente de verdad del código.
- **Si nadie lo va a usar.** En un fichero suelto o un proyecto de una hora, el coste de aprender y mantener el repositorio puede ser mayor que el beneficio. Aun así, en este curso se usa siempre.

## 8. Errores frecuentes

- **Commitear sin mirar `git status`:** se incluyen archivos que no pertenecían al cambio. Usa `git add` con nombres concretos en lugar de `git add .`.
- **Trabajar directamente en `main`:** crea una rama para cada cambio.
- **`git reset --hard` sin pensar:** borra cambios sin posibilidad de recuperarlos desde Git.
- **Reescribir historial compartido:** `git push --force` sobre una rama que otros usan les obliga a reparar su copia. Evítalo; si hace falta, usa `--force-with-lease`.
- **Mensajes como «cambios» o «fix»:** dentro de seis meses nadie sabrá qué cambió ni por qué.

## 9. Git y GitHub: diferencias

Git y GitHub se confunden a menudo, pero son cosas distintas:

| | Git | GitHub |
|---|---|---|
| Qué es | Programa de control de versiones. | Servicio web que aloja repositorios Git. |
| Dónde corre | En tu equipo (es una herramienta de línea de comandos). | En los servidores de GitHub, accesible desde el navegador. |
| Creado por | Linus Torvalds (2005). Software libre. | Empresa (desde 2018 propiedad de Microsoft). |
| Sin el otro | Funciona sin conexión y sin cuenta en ningún sitio. | Necesita Git: almacena repositorios Git. |
| Qué aporta | Historial, commits, ramas, fusiones. | Copia remota, revisiones de código (pull requests), issues, CI/CD (GitHub Actions), páginas web, permisos de equipo. |

Otros servicios similares que alojan repositorios Git son GitLab y Bitbucket. Todos usan el mismo Git por debajo; cambian las funciones de colaboración que añaden alrededor.

Relación práctica: con Git versionas en tu equipo; con GitHub compartes ese historial (`git push origin`), revisas los cambios de otras personas y automatizas pruebas al subir código. Un proyecto puede usar Git sin GitHub (un repositorio solo local, o en un servidor propio), pero no al revés.

En este curso, Git es lo que se usa para versionar el código; GitHub es el sitio donde se publica el repositorio y se entregan las actividades.

## 10. Resumen

Git registra la historia del proyecto como una secuencia de commits, con ramas para aislar trabajo y remotos para compartirlo. Es imprescindible para código y configuración, y se complementa con DVC, Git LFS o el registro de MLflow para datos y modelos grandes, y con variables de entorno para los secretos.
