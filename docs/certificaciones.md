# Roles, certificaciones y ruta de profundización en MLOps

Referencia de los roles de datos, IA y producto del curso, con las certificaciones recomendadas por rol y una ruta para profundizar en MLOps.

> Los nombres de los exámenes y sus códigos cambian con frecuencia. Verifica la vigencia en las páginas oficiales antes de inscribirte. Los exámenes marcados con `*` son los que menos verifiqué.

---

## 1. Roles técnicos de datos e IA

| Rol | Cualidades | Skills clave |
|---|---|---|
| Analytics Engineer | Rigor con las definiciones de negocio | SQL avanzado, dbt, modelado dimensional, testing de datos |
| Data Engineer | Pragmatismo, foco en confiabilidad | Python, Spark, Airflow, lakehouse, calidad de datos |
| Data Scientist | Curiosidad, rigor estadístico, comunicación | Estadística, Python, experimentación, ML clásico |
| ML Engineer | Ingeniería antes que investigación | scikit-learn o PyTorch, feature engineering, evaluación de modelos |
| MLOps Engineer | Automatización, obsesión por la operación | CI/CD, Docker, Kubernetes, MLflow, monitoreo, IaC |
| Software Engineer | Diseño de sistemas, calidad de código | Arquitectura, APIs, testing, bases de datos, cloud |
| AI Engineer | Producto e ingeniería, iteración rápida | LLMs, RAG, agentes, evaluación de LLMs, observabilidad |

## 2. Roles de producto, negocio y diseño

| Rol | Cualidades | Skills clave |
|---|---|---|
| Product Owner | Priorización, visión de valor, capacidad de decidir | Backlog, historias de usuario, Scrum, métricas de producto |
| Project Manager | Organización, gestión de riesgos, liderazgo | Cronogramas, presupuesto, stakeholders, PMP o Agile |
| Business Analyst | Pensamiento analítico, traductor negocio-tecnología | Requisitos, BPMN, KPIs, SQL básico |
| Data Analyst | Curiosidad, foco en preguntas de negocio | SQL, Excel, Power BI o Looker, storytelling |
| Product Designer | Empatía, pensamiento visual, iteración | Investigación de usuarios, UX/UI, Figma, accesibilidad |

**Punto de encuentro:** PO, BA y Data Analyst trabajan con el mismo dato. El Product Designer y el AI Engineer se cruzan en cualquier producto con IA.

---

## 3. Certificaciones por rol técnico

| Rol | AWS | GCP | Databricks |
|---|---|---|---|
| Analytics Engineer | [Cloud Practitioner](https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html) | [Associate Data Practitioner*](https://cloud.google.com/learn/certification/data-practitioner) | [Data Analyst Associate](https://www.databricks.com/en/learn/certification/data-analyst-associate) |
| Data Engineer | [Data Engineer Associate (DEA-C01)](https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/data-engineer-associate-01.html) | [Professional Data Engineer](https://cloud.google.com/learn/certification/data-engineer) | [Data Engineer Associate](https://www.databricks.com/learn/certification/data-engineer-associate) → Professional |
| Data Scientist | [ML Engineer Associate (MLA-C01)](https://aws.amazon.com/certification/) | [Professional ML Engineer](https://cloud.google.com/learn/certification/machine-learning-engineer) | [Machine Learning Associate](https://www.databricks.com/learn/certification/machine-learning-associate) |
| ML Engineer | [ML Engineer Associate (MLA-C01)](https://aws.amazon.com/certification/) | [Professional ML Engineer](https://cloud.google.com/learn/certification/machine-learning-engineer) | [Machine Learning Professional](https://www.databricks.com/en/learn/certification/machine-learning-professional) |
| MLOps Engineer | [DevOps Engineer Professional (DOP-C02)](https://docs.aws.amazon.com/aws-certification/latest/devops-engineer-professional-02/devops-engineer-professional-02.html) | [Professional Cloud DevOps Engineer](https://cloud.google.com/learn/certification/cloud-devops-engineer) | [Machine Learning Professional](https://www.databricks.com/en/learn/certification/machine-learning-professional) |
| Software Engineer | [Developer Associate (DVA-C02)](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-02/developer-associate-02.html) | [Associate Cloud Engineer](https://cloud.google.com/learn/certification/cloud-engineer) | — |
| AI Engineer | [AI Practitioner (AIF-C01)](https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html) | [Generative AI Leader*](https://cloud.google.com/learn/certification/generative-ai-leader) | [Generative AI Engineer Associate](https://www.databricks.com/learn/certification/genai-engineer-associate) |

**Roles de producto y negocio:** como base, [AWS Cloud Practitioner](https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html) o [GCP Cloud Digital Leader](https://cloud.google.com/learn/certification/cloud-digital-leader).

**Orden sugerido:** fundamentos (Cloud Practitioner o Cloud Digital Leader) → certificación asociada de su rol → certificación profesional.

**Notas:**
- AWS retiró la ML Specialty. Su reemplazo actual es la ML Engineer Associate (MLA-C01).
- El link de MLA-C01 apunta a la página general de AWS Certification, porque no encontré la página directa del examen.
- Los links de [Certifications de GCP](https://cloud.google.com/learn/certification) y [AWS Certification](https://aws.amazon.com/certification/) llevan a las páginas generales de cada proveedor.

---

## 4. Ruta para profundizar en MLOps

### Ruta gratuita

- [Made With ML (MLOps)](https://madewithml.com/courses/mlops/), de Goku Mohandas
- [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp), de DataTalksClub
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/course/)

### Cursos y certificaciones

- [Machine Learning in Production](https://www.coursera.org/learn/introduction-to-machine-learning-in-production), DeepLearning.AI en Coursera
- [Especialización MLOps](https://www.coursera.org/specializations/machine-learning-operations-mlops-on-google-cloud), Google Cloud en Coursera
- MLOps Engineering on AWS, en [AWS Skill Builder](https://skillbuilder.aws/). No encontré la página directa del curso.
- [Machine Learning Professional](https://www.databricks.com/en/learn/certification/machine-learning-professional), Databricks
- [Professional ML Engineer](https://cloud.google.com/learn/certification/machine-learning-engineer), Google Cloud

### Lecturas

- [Designing Machine Learning Systems](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/), Chip Huyen
- [Practical MLOps](https://www.oreilly.com/library/view/practical-mlops/9781098103002/), Noah Gift y Alfredo Deza

### Recomendación

Empieza con Made With ML y MLOps Zoomcamp. Este curso usa MLflow, Prefect y GitHub Actions, y esas bases se aplican directo en la especialización de Google Cloud.

Stack para practicar: Git, Docker, Kubernetes básico, MLflow, Airflow, GitHub Actions, Terraform, Prometheus y Grafana.
