# 03 — Estructura del proyecto

## 📌 Introducción

Este proyecto está organizado siguiendo principios de **ingeniería MLOps**, con una separación clara entre:

- análisis exploratorio
- lógica de negocio
- orquestación del pipeline
- infraestructura
- visualización
- documentación

El objetivo de esta estructura es garantizar:
- claridad
- mantenibilidad
- reproducibilidad
- escalabilidad
- coherencia académica y profesional

---

## 🧱 Visión general del repositorio

La estructura del repositorio refleja el ciclo de vida completo de un sistema de detección de anomalías en ciberseguridad:

```text
cybersec-mlops-pipeline/
├── app/
├── backend/
├── docs/
├── frontend/
├── infra/
├── ml/
├── models/
├── notebooks/
├── pipeline/
├── rules/
├── scripts/
├── tests/
├── Dockerfile*
├── requirements*.txt
└── README.md
```

Cada directorio cumple una responsabilidad concreta, evitando acoplamientos innecesarios.

---

## notebooks/ — Análisis y justificación

Contiene notebooks de exploración y validación conceptual.

```text
notebooks/
└── deteccion_anomalias_explicado.ipynb
```

Características:

- análisis exploratorio

- comparación de modelos

- justificación técnica

- base teórica del proyecto

📌 **No se utilizan en producción,** pero son fundamentales para comprender el diseño del sistema.

---

## 🧠 ml/ — Lógica de machine learning

Agrupa componentes reutilizables relacionados con ML:

```text
ml/
├── anomaly_detector.py
└── features.py
```

Responsabilidades:

- definición de features

- lógica de scoring

- abstracción del modelo

Este módulo puede reutilizarse en:

- pipelines batch

- servicios de inferencia

- aplicaciones interactivas

---

## 🔁 pipeline/ — Orquestación MLOps

Es el núcleo del sistema. Implementa el pipeline MLOps completo mediante **Prefect**.


```text
pipeline/
├── ingestion/
├── transformation/
├── training/
├── evaluation/
├── config/
└── full_mlops_flow.py
```

Cada submódulo representa una fase del ciclo de vida del modelo.


### 1️⃣ ingestion/ — Capa RAW

- generación / ingesta de eventos

- validación básica de datos

- almacenamiento en MinIO (RAW)

- auditoría en PostgreSQL

📌 Punto de entrada del pipeline.

### 2️⃣ transformation/ — Capa SILVER

- enriquecimiento de datos

- feature engineering

- normalización y categorización

- persistencia SILVER en MinIO

- auditoría de transformación

📌 Prepara los datos para ML.

### 3️⃣ training/ — Entrenamiento del modelo

- carga de datos SILVER

- entrenamiento Isolation Forest

- versionado del modelo

- almacenamiento en MinIO (MODELS)

- auditoría de entrenamiento

📌 Produce artefactos reutilizables.

### 4️⃣ evaluation/ — Evaluación del modelo

- carga de modelo + dataset

- generación de scores

- cálculo de métricas

- almacenamiento en MinIO (EVAL)

- registro de resultados

📌 Permite comparar ejecuciones y modelos.

### 5️⃣ config/ — Configuración compartida

Contiene definiciones comunes reutilizadas por todo el pipeline:

```text
pipeline/config/
└── features.py
```

Ejemplos:

- columnas oficiales de entrada

- convenciones compartidas

Esto evita inconsistencias entre fases.

---

## 🚀 full_mlops_flow.py — Orquestación global

Este archivo coordina todas las fases del pipeline:


```text
pipeline/full_mlops_flow.py
```

Responsabilidades:

- ejecución secuencial de los subflows

- control del flujo end-to-end

- punto de entrada para Kubernetes

📌 No contiene lógica de negocio, solo orquestación.

---

## 🖥️ frontend/ — Visualización (Streamlit)

```text
frontend/
└── streamlit_app.py
```

Funcionalidad:

- visualización de resultados ML

- carga dinámica de modelos desde MinIO

- exploración de scores y alertas

Diseñada para:

- analistas SOC

- público no técnico

- demostraciones académicas

---

## 🏗 infra/ — Infraestructura

Agrupa configuraciones de despliegue:

```text
infra/
├── k8s/
├── minio/
├── postgresql/
├── mlflow/
└── prefect/
```

Incluye:

- manifests de Kubernetes

- valores Helm

- documentación de servicios

📌 Permite reproducir el entorno completo on-premise.
---

## 📚 docs/ — Documentación interna


```text
docs/
├── 01_objetivos.md
├── 02_metricas.md
├── 03_estructura.md
├── 04_scripts.md
├── 05_tests.md
└── 06_ingestion_minio.md
```

Su función es:

- documentar decisiones técnicas

- facilitar comprensión académica

- servir como base del TFM
---

## 🧪 tests/ — Validación

Incluye pruebas básicas para asegurar:

- integridad del pipeline

- estabilidad de funciones clave

```text
tests/
└── test_pipeline.py
```
---

## 📌 Principios de diseño adoptados

La estructura del proyecto sigue estos principios:

- separación clara de responsabilidades

- desacoplamiento entre fases

- almacenamiento persistente externo (MinIO)

- trazabilidad completa (PostgreSQL)

- ejecución reproducible en Kubernetes

---

## 🔮 Evolución futura de la estructura

Como trabajo futuro se contempla:

- incorporación de serving online

- CI/CD automatizado

- monitorización avanzada

- separación en microservicios

- control de versiones de datasets

Estas extensiones no se incluyen en el alcance actual para mantener el proyecto controlado y evaluable académicamente.