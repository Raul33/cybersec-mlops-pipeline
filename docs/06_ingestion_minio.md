# 06 — Ingesta y almacenamiento en MinIO (RAW layer)

## 📌 Introducción

Este documento describe el uso de **MinIO** como sistema de almacenamiento de objetos dentro del proyecto `cybersec-mlops-pipeline`.

MinIO actúa como **data lake on-premise**, permitiendo almacenar datasets y artefactos de machine learning de forma:

- desacoplada
- versionada
- reproducible
- compatible con Kubernetes

En el pipeline MLOps, MinIO es el **punto central de persistencia de datos**.

---

## 🎯 Objetivo de MinIO en el proyecto

MinIO se utiliza para cumplir los siguientes objetivos:

- almacenar datasets en distintas capas (RAW, SILVER, MODELS, EVAL)
- desacoplar el pipeline del sistema de archivos local
- permitir ejecución 100% dentro del clúster Kubernetes
- facilitar trazabilidad y versionado de artefactos
- simular un data lake real en entornos on-premise

📌 MinIO es completamente compatible con la API S3, lo que lo hace estándar en proyectos MLOps modernos.

---

## 🧱 Capas de almacenamiento definidas

El proyecto implementa una separación clara por buckets:

```text
cybersec-ml-raw       → datos ingeridos sin procesar
cybersec-ml-silver    → datos transformados
cybersec-ml-models    → modelos entrenados
cybersec-ml-eval      → resultados de evaluación
```

Esta separación facilita:

- control del ciclo de vida de los datos

- auditoría

- rollback

- reutilización de artefactos

## 🔁 Flujo de ingesta hacia MinIO

Durante la fase de ingesta:

1. Se generan eventos de red sintéticos

2. Se validan los datos

3. Se serializan en formato Parquet

4. Se suben al bucket RAW (`cybersec-ml-raw`)

El archivo queda almacenado con un nombre versionado basado en timestamp:

```text
network_events_<YYYYMMDD_HHMMSS>.parquet
```

---

## 🧠 Implementación técnica

La lógica de ingesta en MinIO se implementa en el task:

```text
upload_to_minio()
```

upload_to_minio()

```text
pipeline/ingestion/data_ingestion_flow.py
```

Este task:

- inicializa un cliente MinIO usando variables de entorno

- sube el archivo Parquet al bucket RAW

- devuelve la URI completa del objeto (`s3://bucket/archivo`)

---

## 📦 Formato de datos: Parquet

Se utiliza el formato **Parquet** por los siguientes motivos:

- almacenamiento columnar eficiente

- compresión automática

- lectura rápida

- integración natural con pandas, Spark y ML

estándar en pipelines de datos modernos

📌 Esto facilita una transición futura a sistemas de big data si fuese necesario.

---

## 🧾 Trazabilidad y auditoría

Cada ingesta registrada en MinIO genera un evento de auditoría en PostgreSQL que incluye:

- timestamp de ingesta

- nombre del archivo

- ruta exacta en MinIO

- número de registros

- estado de la ejecución

Esto permite responder preguntas como:

- ¿qué dataset se usó?

- ¿cuándo se generó?

- ¿dónde está almacenado?

- ¿cuántos registros contiene?

---

## ⚙️ Ejecución en Kubernetes

Cuando el pipeline se ejecuta en Kubernetes:

- los archivos locales existen solo dentro del contenedor

- MinIO actúa como almacenamiento persistente

- no se depende del filesystem del host

- la ejecución es completamente reproducible

📌 Este diseño es clave para entornos productivos.

---

## 🧪 Validación manual

Durante el desarrollo se validó la ingesta en MinIO mediante:

- inspección de buckets desde la UI de MinIO

- verificación de nombres y timestamps

- descarga manual de Parquets

- comparación con registros de PostgreSQL

---

## 🚀 Trabajo futuro

Posibles mejoras relacionadas con MinIO:

- políticas de retención por bucket

- versionado automático de objetos

- cifrado en reposo

- integración con MLflow

- lifecycle management

Estas mejoras se consideran fuera del alcance actual del proyecto.

---


###############################

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

---

## 🧠 Conclusión

MinIO cumple un papel central en el pipeline MLOps, proporcionando un **data lake ligero, reproducible y alineado con buenas prácticas**.

Su uso permite desacoplar completamente el procesamiento del almacenamiento, facilitando escalabilidad, auditoría y mantenimiento del sistema.




