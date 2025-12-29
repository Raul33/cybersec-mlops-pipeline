# 📊 Evaluación del modelo de detección de anomalías (Isolation Forest)

## 🎯 Objetivo del módulo

Este módulo implementa la fase de **evaluación del modelo** dentro del pipeline MLOps, permitiendo analizar el comportamiento del modelo **Isolation Forest** entrenado sobre datos transformados (SILVER).

La evaluación proporciona:

- métricas cuantitativas del rendimiento del modelo
- análisis estadístico del score de anomalía
- trazabilidad completa entre modelo, dataset y resultados
- persistencia de resultados y auditoría en PostgreSQL

Este paso completa el ciclo:
**ingesta → transformación → entrenamiento → evaluación**

---

## 🔁 Flujo funcional de evaluación

El flujo de evaluación se implementa mediante **Prefect** y sigue los siguientes pasos:

1️⃣ **Carga del modelo más reciente desde MinIO**  
Se identifica y descarga automáticamente el último modelo disponible en el bucket:

```text
cybersec-ml-models
```


2️⃣ **Carga del dataset SILVER más reciente**
Se selecciona el último dataset transformado disponible en:

```text
data/silver
```

3️⃣ **Generación de predicciones y scores**
El modelo aplica:

- `decision_function()` → score continuo de anomalía

- `predict()` → clasificación binaria (0 = normal, 1 = anómalo)

4️⃣ **Cálculo de métricas de evaluación**
Se calculan métricas agregadas para analizar el comportamiento del modelo.

5️⃣ **Persistencia de resultados de evaluación**
Las métricas se guardan en formato Parquet y se suben a MinIO.

6️⃣ **Registro del evento de evaluación en PostgreSQL**
Se almacena un registro estructurado con trazabilidad completa del proceso.

---

## 🧠 Implementación técnica

El flow completo está definido en:

```text
pipeline/evaluation/model_evaluation_flow.py
```

**Tasks principales**

- load_latest_model
Descarga el modelo más reciente desde MinIO.

- load_latest_silver
Carga el dataset SILVER más reciente para evaluación.

- generate_predictions
Aplica el modelo para generar:

    - `anomaly_score`

    - `prediction` (0 = normal, 1 = anómalo)

- compute_metrics
Calcula métricas agregadas de evaluación.

- save_eval_results
Guarda los resultados de evaluación como Parquet local.

- upload_eval_to_minio
Sube el fichero de evaluación al bucket correspondiente.

- register_eval_event
Registra el evento de evaluación en PostgreSQL.

---

## 📊 Métricas calculadas

Dado que el problema es **no supervisado** y no existe ground truth real, se asume un escenario de normalidad dominante para poder derivar métricas operativas.

Las métricas calculadas son:

- **precision →** proporción de detecciones correctas

- **recall →** capacidad de detección de anomalías

- **f1 →** equilibrio entre precisión y recall

- **anomaly_rate →** proporción de eventos marcados como anómalos

- **score_mean →** media del score de anomalía

- **score_std →** desviación estándar del score

Estas métricas permiten:

- validar estabilidad del modelo

- detectar posibles derivas

- comparar ejecuciones entre sí

---

## 📁 Estructura de artefactos generados

### 📦 Resultados de evaluación (local)

```text
data/eval/eval_<timestamp>.parquet
```

### 📦 Almacenamiento en MinIO

```text
s3://cybersec-ml-eval/eval_<timestamp>.parquet
```

---

## 🗄️ Auditoría en PostgreSQL

Cada ejecución genera un registro en la tabla `evaluation_events`.

**Esquema de la tabla**

```sql
CREATE TABLE evaluation_events (
    id SERIAL PRIMARY KEY,
    timestamp_eval TIMESTAMP NOT NULL,
    modelo_nombre TEXT NOT NULL,
    nombre_dataset TEXT NOT NULL,
    ruta_resultados TEXT NOT NULL,
    metrics JSONB NOT NULL,
    estado TEXT NOT NULL
);
```
**Información registrada**

- modelo evaluado

- dataset utilizado

- ubicación del resultado

- métricas calculadas (JSON)

- estado de la ejecución

---

## 📂 Estructura del módulo

```text
pipeline/
  evaluation/
    model_evaluation_flow.py
    README.md
```

---

## ▶️ Ejecución del flow


```bash
python pipeline/evaluation/model_evaluation_flow.py
```

Ejemplo de salida real:


```text
Evaluación subida correctamente: s3://cybersec-ml-eval/eval_20251224_183029.parquet
Evento de evaluación registrado.
Evaluación completada.
Flow run 'imported-rhino' - Finished in state Completed()
```

---

## 🔗 Integración en el pipeline MLOps completo

Este módulo se ejecuta como **subflow** dentro del pipeline global definido en:

```text
pipeline/full_mlops_flow.py
```

Su ejecución permite:

- validar el modelo entrenado

- generar evidencias cuantitativas

- alimentar decisiones de despliegue o retraining

- cerrar el ciclo de vida MLOps del sistema

---

## 📌 Resultados alcanzados

✔ evaluación automatizada y reproducible
✔ métricas cuantitativas persistidas
✔ trazabilidad modelo–datos–resultados
✔ almacenamiento desacoplado en MinIO
✔ auditoría completa en PostgreSQL
✔ cierre del pipeline MLOps end-to-end