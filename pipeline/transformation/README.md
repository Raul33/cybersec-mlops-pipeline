# Transformación de datos RAW → SILVER con auditoría

## 📌 Objetivo del módulo

Este módulo implementa la fase de **transformación de datos** dentro del pipeline MLOps, convirtiendo eventos de red en formato RAW almacenados en MinIO en una versión **SILVER** enriquecida, estructurada y lista para análisis o entrenamiento de modelos de machine learning.

La transformación garantiza:
- calidad de datos
- trazabilidad completa
- separación clara de capas (RAW / SILVER)
- auditoría por ejecución

---

## 🔁 Flujo funcional de transformación

El flujo de transformación se implementa mediante **Prefect** y sigue los siguientes pasos:

1️⃣ **Selección del dataset RAW más reciente**  
Se identifica automáticamente el archivo Parquet más reciente disponible en el bucket RAW de MinIO (`cybersec-ml-raw`).

2️⃣ **Descarga local temporal**  
El archivo seleccionado se descarga a una ubicación temporal (`data/tmp`) para su procesamiento.

3️⃣ **Transformación del dataset**  
Se aplican transformaciones deterministas para enriquecer los datos:

- Cálculo de `bytes_per_second`
- Extracción de la hora del evento (`timestamp_hour`)
- Clasificación del tamaño del flujo (`flow_size_category`)

Estas transformaciones generan nuevas features útiles para análisis y entrenamiento ML.

4️⃣ **Persistencia en formato SILVER**  
El dataset transformado se guarda localmente en formato Parquet, versionado mediante timestamp:

```text
data/silver/network_events_silver_<timestamp>.parquet
```

5️⃣ **Subida a MinIO (SILVER layer)**
El archivo generado se sube al bucket `cybersec-ml-silver`, desacoplando el almacenamiento del sistema de archivos local.

6️⃣ **Registro de auditoría en PostgreSQL**
Cada ejecución del flow registra un evento en PostgreSQL con:

- timestamp de transformación

- nombre del archivo generado

- ruta del objeto en MinIO

- número de registros procesados

- estado final de la ejecución

---

## 🧠 Implementación técnica

El flow completo está definido en:


```text
pipeline/transformation/data_transformation_flow.py
```

**Tasks principales**

- find_latest_raw: detecta el parquet RAW más reciente

- download_from_minio: descarga el archivo para procesamiento local

- transform_parquet: aplica enriquecimiento y feature engineering

- save_silver: guarda el dataset transformado

- upload_to_minio: sube el resultado a MinIO (SILVER)

- register_transformation_event: registra auditoría en PostgreSQL

---

## 📂 Estructura del módulo

```text
pipeline/
  transformation/
    data_transformation_flow.py
    README.md
```

---

## 📦 Requisitos previos

**Buckets MinIO**

```text
cybersec-ml-raw
cybersec-ml-silver
```
**Tabla PostgreSQL**

```text
CREATE TABLE transformation_events (
    id SERIAL PRIMARY KEY,
    timestamp_transformacion TIMESTAMP NOT NULL,
    nombre_archivo TEXT NOT NULL,
    ruta_minio TEXT NOT NULL,
    num_registros INTEGER NOT NULL,
    estado TEXT NOT NULL
);
```

---


## 🔗 Integración en el pipeline completo

Este módulo se ejecuta como subflow dentro del pipeline MLOps global definido en:

```text
pipeline/full_mlops_flow.py
```

Su correcta ejecución es un prerrequisito para:

- entrenamiento del modelo

- evaluación del rendimiento

- registro de artefactos

---

## 📌 Variables de entorno (ejemplo ilustrativo)

```text
export MINIO_ENDPOINT="localhost:9000"
export MINIO_ACCESS_KEY="<YOUR_USER>"
export MINIO_SECRET_KEY="<YOUR_PASSWORD>"

export PG_HOST="localhost"
export PG_PORT="5555"
export PG_USER="postgres"
export PG_PASSWORD="<YOUR_PASSWORD>"
export PG_DATABASE="mlops_db"
```

> Las siguientes variables de entorno se muestran a modo ilustrativo para ejecución local.
En entornos Kubernetes, estas variables se inyectan mediante Secrets y ConfigMaps.

---

## ▶️ Ejecución del pipeline

```bash
python pipeline/transformation/data_transformation_flow.py
```
📌 Ejemplo de salida real:

```bash
Evento de transformación registrado.
Transformación completada.
Flow run 'gregarious-beagle' - Finished in state Completed()
```
## 🧾 Verificación PostgreSQL

```bash
kubectl exec -it mlops-postgresql-0 -n mlops -- \
  psql -U postgres mlops_db \
  -c "SELECT * FROM transformation_events ORDER BY id DESC LIMIT 5;"
```
📌 Ejemplo real:

```text
 id |  timestamp_transformacion  |                nombre_archivo                 |                              ruta_minio                               | num_registros | estado  
----+----------------------------+-----------------------------------------------+-----------------------------------------------------------------------+---------------+---------
  1 | 2025-12-20 15:11:06.847591 | network_events_silver_20251220_161106.parquet | s3://cybersec-ml-silver/network_events_silver_20251220_161106.parquet |            10 | SUCCESS

```

## 📌 Resultados alcanzados

🔄 pipeline RAW → SILVER operativo

📁 parquet transformado almacenado en MinIO

🧾 tracking transaccional en PostgreSQL

🔐 auditoría total por ejecución

🧠 dataset limpio, enriquecido y estandarizado

⚙️ ejecución reproducible y automatizable con Prefect


