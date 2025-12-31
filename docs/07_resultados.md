# 07 — Resultados del sistema MLOps de detección de anomalías

## 📌 Introducción

Este capítulo presenta los **resultados obtenidos** tras la implementación y ejecución del sistema MLOps desarrollado para la detección de anomalías en eventos de red.

Los resultados se analizan desde una doble perspectiva:

- **Resultados del modelo de machine learning**
- **Resultados del pipeline MLOps end-to-end**

El objetivo no es únicamente evaluar el rendimiento del modelo, sino demostrar la **validez, reproducibilidad y trazabilidad del sistema completo**, que constituye el núcleo del proyecto.

---

## 🧠 Resultados del modelo de detección de anomalías

### 📊 Modelo utilizado

El modelo finalmente integrado en el pipeline es **Isolation Forest**, seleccionado tras un análisis comparativo realizado en el notebook exploratorio del proyecto.

Las razones principales de su elección fueron:

- Buen equilibrio entre detección de anomalías y falsos positivos
- Robustez frente a ruido
- Baja necesidad de ajuste de hiperparámetros
- Adecuación a contextos sin etiquetas (aprendizaje no supervisado)

---

### ⚙️ Configuración del modelo

El entrenamiento se realiza automáticamente sobre los datos transformados (capa SILVER), utilizando las mismas columnas de entrada de forma consistente.

Configuración principal:

- `n_estimators = 100`
- `contamination = auto`
- `random_state = 42`

Esta configuración prioriza **estabilidad y reproducibilidad** frente a optimización agresiva.

---

### 📈 Resultados de evaluación

Dado que el sistema trabaja con **datos no etiquetados**, la evaluación se basa en métricas indirectas y de comportamiento:

- **Tasa de anomalías detectadas**
- **Distribución del score de anomalía**
- **Estabilidad estadística del score**
- **Consistencia entre ejecuciones**

Estas métricas permiten validar el comportamiento del modelo sin necesidad de ground truth explícito, lo cual es habitual en escenarios reales de ciberseguridad.

---

### 📊 Métricas registradas

En cada ejecución de la fase de evaluación se registran, entre otras, las siguientes métricas:

- `anomaly_rate`: proporción de eventos marcados como anómalos
- `score_mean`: media del score de anomalía
- `score_std`: desviación estándar del score

Estas métricas permiten detectar:

- cambios bruscos en el comportamiento del modelo
- posibles problemas de deriva de datos
- ejecuciones anómalas del pipeline

Los resultados de evaluación se almacenan de forma versionada en MinIO (bucket `cybersec-ml-eval`) y quedan auditados en PostgreSQL.

---

## 🔁 Resultados del pipeline MLOps

### 🧩 Ejecución end-to-end

El pipeline MLOps completo se ejecuta como un **Job de Kubernetes**, lanzando el flow principal `full_mlops_flow`.

Cada ejecución completa incluye:

1. Ingesta de datos (RAW)
2. Transformación y feature engineering (SILVER)
3. Entrenamiento del modelo
4. Evaluación del modelo
5. Registro de metadatos y auditoría

El pipeline se ejecuta correctamente sin dependencia del entorno local, utilizando únicamente servicios internos del clúster.

---

### 📦 Resultados de persistencia y versionado

Durante una ejecución completa del pipeline se generan y almacenan los siguientes artefactos:

- Dataset RAW en MinIO (`cybersec-ml-raw`)
- Dataset transformado SILVER (`cybersec-ml-silver`)
- Modelo entrenado (`cybersec-ml-models`)
- Resultados de evaluación (`cybersec-ml-eval`)

Todos los artefactos:

- están versionados mediante timestamp
- son inmutables una vez generados
- pueden ser reproducidos a partir de los metadatos registrados

---

### 🧾 Resultados de trazabilidad y auditoría

Cada fase del pipeline genera un evento estructurado en PostgreSQL:

- `ingestion_events`
- `transformation_events`
- `training_events`
- `evaluation_events`

Esto permite reconstruir completamente una ejecución y responder a preguntas clave como:

- qué datos se utilizaron
- qué modelo se entrenó
- cuándo se ejecutó cada fase
- qué métricas se obtuvieron

La combinación de Prefect + PostgreSQL proporciona una **trazabilidad completa del ciclo de vida del modelo**.

---

## 🖥️ Resultados de la aplicación de visualización

La aplicación web desarrollada con **Streamlit (SOC Copilot)** permite visualizar de forma intuitiva los resultados del pipeline:

- modelos disponibles en MinIO
- resultados de evaluación más recientes
- distribución de scores de anomalía
- exploración interactiva de eventos

La aplicación consume directamente los artefactos generados por el pipeline, validando la **integración entre backend MLOps y frontend de visualización**.

---

## ✅ Evaluación global de resultados

A partir de los resultados obtenidos, se concluye que:

- el pipeline MLOps es funcional y estable
- el modelo de detección de anomalías se comporta de forma coherente
- la arquitectura es reproducible y desacoplada
- la trazabilidad está garantizada en todas las fases
- el sistema es representativo de un entorno real de MLOps en ciberseguridad

El proyecto cumple así los objetivos planteados y valida la viabilidad de una arquitectura MLOps on-premise basada en Kubernetes.

---

## 📌 Resumen de resultados clave

- ✔ Pipeline end-to-end operativo en Kubernetes
- ✔ Modelo no supervisado entrenado automáticamente
- ✔ Versionado completo de datos, modelos y métricas
- ✔ Auditoría estructurada por ejecución
- ✔ Visualización funcional de resultados
- ✔ Diseño alineado con buenas prácticas MLOps

Estos resultados constituyen la base para las conclusiones finales del trabajo.
