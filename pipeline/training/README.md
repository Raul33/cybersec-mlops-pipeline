# 08 — Entrenamiento ML (Isolation Forest) + auditoría en PostgreSQL

## 🎯 Objetivo
Esta fase incorpora un modelo de detección de anomalías basado en **Isolation Forest**, entrenado diariamente sobre datos transformados (silver). Produce un modelo funcional, almacenable y reutilizable para inferencia.

---

## 📌 Flujo funcional
1️⃣ Cargar datos SILVER materializados en el workspace del Job de Kubernetes
2️⃣ Entrenar Isolation Forest  
3️⃣ Guardar el modelo como pickle  
4️⃣ Subir el modelo a MinIO (gold/models)  
5️⃣ Registrar el evento en PostgreSQL  

---

## 🧠 Nota sobre ejecución en Kubernetes

Aunque el pipeline se ejecuta completamente en Kubernetes, cada Job dispone de un sistema de archivos efímero donde se materializan los resultados intermedios de cada subflow.

El módulo de entrenamiento consume directamente los datos SILVER generados previamente dentro del mismo Job, evitando descargas redundantes desde MinIO y manteniendo el pipeline como una unidad atómica de ejecución.
---

## 📁 Estructura de archivos generados

### 📦 Modelo entrenado
Se almacena dentro de MinIO:

```bash
s3://cybersec-ml-models/model_isoforest_<timestamp>.pkl
```
Ejemplo real:

```bash
s3://cybersec-ml-models/model_isoforest_20251220_183501.pkl
```

---

## 📌 Variables de entorno requeridas

### para MinIO
```bash
export MINIO_ENDPOINT="localhost:9000"
export MINIO_ACCESS_KEY="<YOUR_USER>"
export MINIO_SECRET_KEY="<YOUR_PASSWORD>"
```

### para PostgreSQL

```bash
export PG_HOST="localhost"
export PG_PORT="5555"
export PG_USER="postgres"
export PG_PASSWORD="<YOUR_PASSWORD>"
export PG_DATABASE="mlops_db"
```
## 🗄️ Tabla PostgreSQL utilizada (training audit)


```sql
CREATE TABLE IF NOT EXISTS training_events (
    id SERIAL PRIMARY KEY,
    timestamp_entrenamiento TIMESTAMP NOT NULL,
    ruta_modelo TEXT NOT NULL,
    num_registros INTEGER NOT NULL,
    parametros TEXT NOT NULL,
    estado TEXT NOT NULL
);
```

Campos:

- timestamp_entrenamiento: fecha real de ejecución

- ruta_modelo: ubicación exacta del pickle en MinIO

- num_registros: nº efectivo de filas usadas en el entrenamiento

- parametros: hiperparámetros del modelo

- estado: SUCCESS / FAILED

## 📌 Hiperparámetros usados (simple y estable)

```python
IsolationForest(
    contamination="auto",
    random_state=42,
    n_estimators=100
)
```
Justificación:

- n_estimators=100 → buen equilibrio entre precisión y coste

- random_state=42 → reproducibilidad

- contamination='auto' → robusto sin tunning

## 🧠 Posibles métricas derivables del score (trabajo futuro)

Tras el entrenamiento, el modelo produce un score medio y desviación estándar:

- score_mean: = media(score_anomalía)

- score_std: = varianza(score_anomalía)

Estas métricas permiten validar estabilidad sin complicar el diseño.

> Actualmente estas métricas no se calculan ni se persisten en el pipeline.
> Su inclusión se plantea como una extensión natural en futuras iteraciones, por ejemplo mediante integración con MLflow.


---

## 📊 Ejemplo de registro real en PostgreSQL

```text
 id |   timestamp_entrenamiento    |                   ruta_modelo                  | num_registros |                parametros                 | estado  
----+------------------------------+------------------------------------------------+---------------+-------------------------------------------+---------
  1 | 2025-12-20 18:35:01.403920   | s3://cybersec-ml-models/model_isoforest_2025… |           457 | {'n_estimators':100,'contamination':'auto'} | SUCCESS

```
---

## 📌 Gestión de features

El entrenamiento utiliza exclusivamente las columnas definidas en:

pipeline/config/features.py

Esto garantiza coherencia total entre entrenamiento e inferencia, evita divergencias de esquema y facilita el mantenimiento del sistema.

