# 06 — Ingesta de datos + almacenamiento en MinIO + auditoría PostgreSQL (on-premises)

## 📌 Objetivo
En esta fase se implementa la ingesta de datos en modo batch diario, con:

- Generación sintética de tráfico de red  
- Validación básica del dataset  
- Persistencia en formato parquet  
- Subida a MinIO (S3 on-premises)  
- Registro operacional en PostgreSQL  

Esta fase consolida el primer tramo real del pipeline MLOps orientado a detección de anomalías en red.

---

## 📌 Tecnologías usadas
- Prefect 2.14.10 → orquestación  
- MinIO → almacenamiento raw tipo S3 en Kubernetes  
- PostgreSQL → metadata y auditoría de ingestas  
- Python 3.11 → ejecución del pipeline  
- Parquet + PyArrow → formato columna eficiente  
- Kubernetes → entorno on-premises reproducible  

---

## 📁 Estructura de archivos generados
Los datos quedan almacenados bajo:

```text
data/ingested/network_events_<timestamp>.parquet
```
ejemplo real:

```text
data/ingested/network_events_20251220_121209.parquet
```

## 📦 Flujo funcional

1️⃣ Generación de dataset sintético

- Cada ejecución produce 10 filas simuladas con campos:
timestamp, src_ip, dst_ip, bytes, duration, protocol

2️⃣ Validación estructural

- Tipos correctos

- Sin nulos

- Esquema consistente

3️⃣ Persistencia local

- Guardado automático en parquet

4️⃣ Carga a MinIO (S3)

- Bucket: cybersec-ml-raw

- Cada ingesta genera un objeto nuevo

5️⃣ Registro operacional en PostgreSQL

- Inserción de un registro por ejecución

- Auditoría completa de origen, volumen y estado

## 📌 Variables de entorno requeridas

Antes de ejecutar el pipeline, deben configurarse:

```bash
export MINIO_ENDPOINT="localhost:9000"
export MINIO_ACCESS_KEY="<YOUR_USER>"
export MINIO_SECRET_KEY="<YOUR_PASSWORD>"
```

> NOTA: El puerto 9000 es el API S3.
> El puerto 9001 es la consola web y no acepta operaciones S3.


```bash
kubectl port-forward pod/<NOMBRE_DEL_POD> -n mlops 9000:9000 9001:9001
```
PostgreSQL

```bash
export PG_HOST="localhost"
export PG_PORT="5555"
export PG_USER="postgres"
export PG_PASSWORD="<YOUR_PASSWORD>"
export PG_DATABASE="mlops_db"
```

> ⚠️ PG_PASSWORD es obligatorio — si falta, el pipeline lo bloquea.

Para exponer PostgreSQL desde Kubernetes:

```bash
kubectl port-forward \
  -n mlops \
  svc/mlops-postgresql \
  5555:5432
```

## 🗄️ Tabla PostgreSQL utilizada

```sql
CREATE TABLE ingestion_events (
    id SERIAL PRIMARY KEY,
    timestamp_ingesta TIMESTAMP NOT NULL,
    nombre_archivo TEXT NOT NULL,
    ruta_minio TEXT NOT NULL,
    num_registros INTEGER NOT NULL,
    estado TEXT NOT NULL
);
```

## 📌 Consulta rápida de ingestiones históricas

```bash
kubectl exec -it mlops-postgresql-0 -n mlops -- \
  psql -U postgres mlops_db \
  -c "SELECT * FROM ingestion_events ORDER BY id DESC LIMIT 10;"
```

Ejemplo de salida real:

```bash
 id |     timestamp_ingesta      |             nombre_archivo             |                         ruta_minio                          | num_registros | estado  
----+----------------------------+----------------------------------------+-------------------------------------------------------------+---------------+---------
  1 | 2025-12-20 12:12:09.495903 | network_events_20251220_121209.parquet | s3://cybersec-ml-raw/network_events_20251220_121209.parquet |            10 | SUCCESS
```




