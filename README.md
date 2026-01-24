# cybersec-mlops-pipeline

🚀 **Pipeline MLOps para detección de anomalías en eventos de red**, basado en modelos no supervisados (Isolation Forest, LOF, OCSVM) y reglas Sigma simuladas. Diseñado para ejecutarse on‑premise y escalar fácilmente en Kubernetes (RKE2 + Helm). 100% Open Source.

---

## 📚 Contenidos

- [🧩 Arquitectura MLOps](#-arquitectura-mlops-del-sistema)
- [📓 Notebook de justificación](#-notebooks)
- [⚙️ Pipeline MLOps](#-estructura-del-proyecto)
- [🧠 Scripts y lógica ML](#-scripts-principales)
- [🖥️ Aplicación Streamlit](#-aplicación-streamlit-visualización-de-anomalías)
- [🚀 Ejecución y despliegue](#-cómo-ejecutar)
- [🔭 Trabajo futuro](#-siguientes-pasos)

---

## 🎓 Contexto académico y alcance del proyecto

Este repositorio corresponde al **Trabajo Fin de Máster (TFM)** del autor y documenta la evolución completa del proyecto desde una fase exploratoria hasta una implementación **MLOps end-to-end** ejecutada sobre Kubernetes.

El proyecto se estructura en **tres niveles complementarios**:

1. **Exploración y justificación del modelo** (notebooks)
2. **Aplicación de detección y visualización** (scripts + Streamlit)
3. **Pipeline MLOps batch automatizado** (Prefect + MinIO + PostgreSQL + Kubernetes)

Cada uno de estos niveles se conserva de forma explícita en el repositorio para mostrar tanto el razonamiento académico como la implementación profesional.

---

## 🧩 Arquitectura MLOps del sistema

El proyecto implementa una **arquitectura MLOps batch end-to-end**, diseñada para ejecutarse completamente **dentro de un clúster Kubernetes**, sin dependencias del entorno local.

La arquitectura combina herramientas open-source ampliamente utilizadas en MLOps:

- **Prefect** → orquestación de flujos
- **MinIO** → data lake y model registry
- **PostgreSQL** → auditoría y trazabilidad
- **Kubernetes (RKE2)** → ejecución desacoplada y reproducible

### 🔄 Flujo general

A alto nivel, el sistema sigue el siguiente ciclo:

1. **Ingesta de datos**
   - Generación y validación de eventos de red
   - Persistencia en MinIO (capa RAW)
   - Registro de metadatos en PostgreSQL

2. **Transformación de datos**
   - Enriquecimiento y feature engineering
   - Persistencia en MinIO (capa SILVER)
   - Auditoría de transformación

3. **Entrenamiento del modelo**
   - Entrenamiento batch con Isolation Forest
   - Versionado del modelo en MinIO
   - Registro de parámetros y volumen de datos

4. **Evaluación**
   - Aplicación del modelo sobre datos recientes
   - Cálculo de métricas agregadas
   - Almacenamiento de resultados y auditoría

Todo el flujo se ejecuta de forma automática mediante un **Job de Kubernetes**, utilizando imágenes Docker versionadas.

### 📦 Gestión de artefactos

El sistema separa claramente cada tipo de artefacto:

- **RAW** → datos ingeridos sin procesar
- **SILVER** → datos transformados
- **MODELS** → modelos entrenados
- **EVAL** → resultados de evaluación

Todos los artefactos se almacenan en MinIO, utilizando nombres versionados con timestamps para garantizar **reproducibilidad y trazabilidad**.

### 🔍 Observabilidad y auditoría

Cada fase del pipeline registra eventos estructurados en PostgreSQL, permitiendo responder preguntas clave como:

- ¿Qué datos se usaron para entrenar un modelo?
- ¿Cuándo se ejecutó cada fase?
- ¿Con qué parámetros?
- ¿Qué métricas se obtuvieron?

Esta capa de auditoría es fundamental en entornos de **ciberseguridad**, donde la trazabilidad es un requisito crítico.

---

## 🧩 Arquitectura MLOps del sistema

Este proyecto implementa una **arquitectura MLOps end-to-end** para la detección de anomalías en eventos de red, diseñada bajo principios de:

- reproducibilidad
- desacoplamiento
- trazabilidad
- ejecución en Kubernetes

El sistema cubre **todo el ciclo de vida del modelo**, desde la ingesta de datos hasta la evaluación final, sin dependencias del entorno local.

---

### 🏗 Componentes principales

El sistema se compone de los siguientes bloques:

- **Notebooks**  
  Justificación teórica y experimental del enfoque (no productivos).

- **Pipeline MLOps (Prefect)**  
  Orquesta todo el flujo batch:
  - ingesta
  - transformación
  - entrenamiento
  - evaluación

- **MinIO**  
  Actúa como *data lake* y *model registry*:
  - RAW → datos sin procesar
  - SILVER → datos transformados
  - MODELS → artefactos entrenados
  - EVAL → resultados de evaluación

- **PostgreSQL**  
  Almacena metadatos operacionales:
  - ejecuciones
  - datasets usados
  - parámetros de entrenamiento
  - métricas obtenidas

- **Kubernetes (RKE2)**  
  Ejecuta el pipeline como Jobs desacoplados, permitiendo escalado y aislamiento.

- **Aplicación Streamlit**  
  Permite visualizar anomalías detectadas y evaluar el comportamiento del modelo.

---

### 🔄 Flujo de alto nivel

1. Se generan o ingieren eventos de red
2. Los datos se validan y almacenan en la capa RAW (MinIO)
3. Se transforman y enriquecen (SILVER)
4. Se entrena un modelo Isolation Forest
5. El modelo se evalúa sobre datos recientes
6. Todos los pasos quedan auditados

Este diseño refleja un **pipeline MLOps realista**, alineado con prácticas profesionales en entornos de ciberseguridad.

---


## 📓 Notebooks

Los notebooks permiten explorar, probar y justificar el enfoque antes de desplegarlo como aplicación. Funcionan como guía conceptual.

### `notebooks/deteccion_anomalias_explicado.ipynb`

Contiene:

- Simulación y carga de eventos de red  
- Extracción de características (*features*)  
- Comparación de modelos:
  - Isolation Forest ✅
  - Local Outlier Factor
  - One-Class SVM  
- Métodos de evaluación: TP, FP, score  
- Simulación de correlación con reglas Sigma  
- Justificación del modelo final elegido  

> Este notebook **no se usa en producción**, pero **es clave para entender todo el diseño**.

---

## 📁 Estructura del Proyecto

> ⚠️ **Nota sobre la estructura**
>
> Este repositorio incluye tanto:
>
> - código exploratorio y scripts iniciales (fase de experimentación)
> - como una implementación completa de un pipeline MLOps productivo sobre Kubernetes
>
> Ambas partes se conservan deliberadamente:
> - los **scripts y notebooks** justifican decisiones técnicas
> - el **pipeline Prefect + MinIO + PostgreSQL** representa la solución final


```bash
cybersec-mlops-pipeline/
├── backend/                  # (Vacío) Backend opcional para FastAPI
├── data/                     # Datos de entrada y salida
│   ├── normalized/          # Dataset procesado en Parquet
│   │   └── zeek.parquet
│   └── alerts_ml.csv        # Alertas generadas por ML
├── docs/                     # Documentación interna del proyecto
│   ├── 01_objetivos.md
│   ├── 02_metricas.md
│   ├── 03_estructura.md
│   ├── 04_scripts.md
│   └── 05_tests.md
├── frontend/                 # Interfaz web en Streamlit
│   └── streamlit_app.py
├── infra/                    # (Vacío) Infraestructura para K8s, Helm, CI/CD
├── ml/                       # Lógica de entrenamiento y scoring
│   ├── anomaly_detector.py
│   └── features.py
├── models/                   # Modelos entrenados
│   └── iforest.joblib
├── notebooks/                # Notebooks de análisis
│   └── deteccion_anomalias_explicado.ipynb
├── rules/                    # Reglas Sigma simuladas
│   └── sigma_emulator.py
├── scripts/                  # Scripts ejecutables del pipeline
│   ├── generate_test_parquet.py
│   ├── run_iforest.py
│   ├── run_pipeline.py
│   ├── score_events.py
│   └── train_iforest.py
├── tests/                    # Tests unitarios
│   └── test_pipeline.py
├── Dockerfile                # Definición de imagen Docker
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

### 🧪 Código exploratorio y scripts legacy

Los siguientes directorios corresponden a fases iniciales del proyecto y se conservan como:

- evidencia de experimentación
- apoyo conceptual

Incluyen:

- `scripts/` → ejecución local del pipeline inicial
- `ml/` → lógica base de entrenamiento y scoring
- `rules/` → simulación de reglas Sigma
- `tests/` → pruebas unitarias básicas

Este código **no se ejecuta en producción**, pero es clave para entender la evolución del sistema.

### 🔁 Pipeline MLOps productivo (Kubernetes)

La implementación **productiva y automatizada** del sistema se encuentra en el directorio:

```bash
pipeline/
```

Este módulo representa la **fuente de verdad** del sistema y se ejecuta completamente dentro de Kubernetes mediante Jobs.

```text
pipeline/
├── full_mlops_flow.py        # Orquestador end-to-end
├── ingestion/                # Ingesta batch (RAW)
├── transformation/           # Feature engineering (SILVER)
├── training/                 # Entrenamiento del modelo
├── evaluation/               # Evaluación del rendimiento
└── config/                   # Configuración compartida
```

Cada submódulo incluye su propio README con explicación técnica detallada.

---

## 🧠 Scripts Principales

| Script                        | Descripción                                                         |
|------------------------------|---------------------------------------------------------------------|
| `scripts/train_iforest.py`   | Entrena y guarda el modelo Isolation Forest (`iforest.joblib`)      |
| `scripts/score_events.py`    | Puntúa eventos usando el modelo entrenado (`ml_score`)              |
| `scripts/run_iforest.py`     | Filtra outliers y genera alertas ML (`alerts_ml.csv`)               |
| `scripts/run_pipeline.py`    | Ejecuta toda la cadena (entrena → puntúa → alerta)                  |
| `scripts/generate_test_parquet.py` | Genera datos de prueba simulados en formato Parquet           |
| `rules/sigma_emulator.py`    | Simula reglas Sigma sobre eventos para correlación básica          |

---

## 🖥️ Aplicación Streamlit: Visualización de Anomalías

### 📌 Decisión de modelo desplegado

En producción se utiliza exclusivamente el modelo **Isolation Forest**, por su:

- Rendimiento general equilibrado
- Interpretación sencilla
- Integración directa en la app

Los otros modelos (`LOF` y `OCSVM`) se pueden evaluar en la pestaña “Evaluación” de la app pero **no** se despliegan como modelo productivo.

---

### 📊 Qué muestra la aplicación

- **Anomalías ML** — Alertas generadas por Isolation Forest.
- **Evaluación** — Comparación de distribución de score y comportamiento de distintos modelos.

---

## 🚀 Cómo Ejecutar el Proyecto

### ♻️ Ejecución local (fase exploratoria)

> ⚠️ Esta forma de ejecución corresponde a una fase inicial del proyecto y se conserva con fines demostrativos y de aprendizaje.
>  
> El pipeline productivo se ejecuta exclusivamente en Kubernetes.

```bash
python3 scripts/run_pipeline.py
```

- Entrena Isolation Forest - Puntúa eventos - Genera alertas si corresponde - Resultados en data/alerts_ml.csv


### ☸️ Ejecución MLOps en Kubernetes (recomendada)

La forma **principal y productiva** de ejecutar este proyecto es mediante un **Job de Kubernetes**, que lanza el pipeline completo end-to-end dentro del clúster.

Este enfoque garantiza:

- ejecución reproducible
- aislamiento del entorno
- uso exclusivo de servicios internos (MinIO, PostgreSQL)
- ausencia de dependencias locales

#### ▶️ Ejecutar el pipeline completo

```bash
kubectl apply -f infra/k8s/job-full-mlops.yaml
```
#### ▶️ Ver el estado del Job

```bash
kubectl get jobs -n mlops
kubectl get pods -n mlops
```
#### ▶️ Ver logs del pipeline


```bash
kubectl logs -n mlops job/full-mlops-pipeline
```

El Job ejecuta internamente:

- ingesta de datos

- transformación

- entrenamiento

- evaluación

Todo ello orquestado mediante **Prefect** y persistiendo artefactos en **MinIO**.

---

### 🖥️ Visualización (Streamlit)

La aplicación Streamlit se utiliza únicamente como **capa de visualización**, no como motor del pipeline MLOps.
---

### 🐿️ Lanzar la app con Docker

```bash
docker build -t soc-copilot-app .
docker run -p 8501:8501 -v $(pwd)/data:/app/data soc-copilot-app
```

Accede a la app desde:

```
http://localhost:8501
```

---

## 🔭 Siguientes Pasos

Las siguientes líneas de trabajo representan **extensiones naturales del sistema**, no requisitos para la validez del pipeline actual.

El alcance del proyecto se ha delimitado conscientemente para priorizar:
- robustez del pipeline batch
- trazabilidad
- reproducibilidad
- arquitectura MLOps sobre Kubernetes


### 🧩 Evolución funcional

- [ ] Integrar correlación real entre reglas Sigma y anomalías ML
- [ ] Backend REST con FastAPI para serving offline
- [ ] Mejora de la lógica de scoring y umbrales dinámicos

### ⚙️ Evolución MLOps

- [ ] Integración de tracking de experimentos con MLflow
- [ ] Registro avanzado de métricas y artefactos
- [ ] Monitorización con Prometheus + Grafana
- [ ] Automatización CI/CD con GitHub Actions
- [ ] Despliegue mediante Helm Charts

### 🎓 Extensión académica

- [ ] Evaluación con datasets reales de ciberseguridad
- [ ] Comparativa formal con otros enfoques de detección
- [ ] Validación temporal del modelo (data drift / concept drift)

---

> Este repositorio refleja tanto la evolución del proyecto como su arquitectura final, diferenciando claramente entre fases exploratorias y componentes productivos.
