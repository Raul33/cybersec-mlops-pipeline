# 07 — Transformación de datos RAW → SILVER + auditoría PostgreSQL

## 📌 Objetivo
En esta fase del pipeline MLOps convertimos los datos RAW almacenados en MinIO en una versión SILVER más limpia, enriquecida y lista para análisis o entrenamiento ML.

Este paso añade trazabilidad total entre:
- datos crudos (raw)
- datos procesados (silver)
- metadatos operacionales en PostgreSQL

---

## 📌 Flujo funcional de transformación

1️⃣ **Carga desde MinIO (RAW)**
- El flow detecta el archivo parquet más reciente del bucket `cybersec-ml-raw`.

2️⃣ **Transformación del dataset**
- Normalización de columnas  
- Conversión de tipos  
- Cálculo de métricas adicionales (`bytes_per_sec`)  
- Clasificación de tráfico (`traffic_class`: HIGH | MEDIUM | LOW)

3️⃣ **Persistencia local SILVER**
Los datos procesados se guardan automáticamente como:


```text
data/transformed/network_events_silver_<timestamp>.parquet
```
ejemplo real:

```text
cybersec-ml-silver
```


4️⃣ **Subida a MinIO (SILVER)**
El parquet transformado se envía al bucket:

```text
cybersec-ml-silver
```


5️⃣ **Registro de auditoría en PostgreSQL**
Cada ejecución genera un evento estructurado:

- timestamp de transformación
- archivo procesado
- ubicación en MinIO
- volumen de registros
- estado final (SUCCESS | FAILED)

---

## 📂 Requisitos previos

📌 Buckets MinIO existentes:

```text
cybersec-ml-raw
cybersec-ml-silver
```


## 📌 Tabla PostgreSQL creada:

```sql
CREATE TABLE transformation_events (
    id SERIAL PRIMARY KEY,
    timestamp_transformacion TIMESTAMP NOT NULL,
    nombre_archivo TEXT NOT NULL,
    ruta_minio TEXT NOT NULL,
    num_registros INTEGER NOT NULL,
    estado TEXT NOT NULL
);
```

## 📌 Variables de entorno requeridas:

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


