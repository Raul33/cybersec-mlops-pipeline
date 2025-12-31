# Kubernetes Job — Ejecución del pipeline MLOps

## 📌 Rol del Job en el sistema

El pipeline MLOps del proyecto `cybersec-mlops-pipeline` se ejecuta en Kubernetes mediante un **Job**, lo que permite lanzar procesos batch reproducibles y desacoplados del entorno local.

Este Job es el encargado de ejecutar el pipeline completo end-to-end, desde la ingesta de datos hasta la evaluación del modelo.

---

## ⚙️ Tipo de recurso elegido

Se utiliza un recurso de tipo:

```text
kind: Job
```

Esta elección es intencionada, ya que el pipeline:

- es finito (tiene inicio y fin)

- no es un servicio persistente

- no requiere estado en memoria entre ejecuciones

- debe reflejar claramente éxito o fallo

📌 En MLOps, los pipelines de entrenamiento y evaluación se ejecutan habitualmente como Jobs batch.

---

## 🚀 Ejecución del pipeline

El Job lanza un contenedor que ejecuta directamente el flow principal de Prefect:

```text
python pipeline/full_mlops_flow.py
```

Este flow actúa como orquestador end-to-end, encadenando las siguientes fases:

1. Ingesta de datos (RAW)

2. Transformación (SILVER)

3. Entrenamiento del modelo (MODELS)

4. Evaluación del modelo (EVAL)

Toda la lógica de ejecución está contenida en el pipeline, no en el Job.

---

## 🔐 Gestión de credenciales

El Job utiliza Kubernetes Secrets para inyectar credenciales de forma segura:

- MinIO (API S3)

- PostgreSQL (auditoría)

- Docker registry (pull de imagen)

En ningún caso se incluyen credenciales en el código o en el YAML.

---

## 🧱 Variables de entorno utilizadas

El Job define las variables necesarias para conectarse a los servicios internos del clúster:

MinIO

- `MINIO_ENDPOINT`

- `MINIO_ACCESS_KEY`

- `MINIO_SECRET_KEY`

PostgreSQL

- `PG_HOST`

- `PG_PORT`

- `PG_USER`

- `PG_PASSWORD`

- `PG_DATABASE`

MLflow (preparado para futuras fases)

- `MLFLOW_TRACKING_URI`

---

## 📦 Almacenamiento y estado

Durante la ejecución:

- los archivos locales existen únicamente dentro del contenedor

- se utilizan como almacenamiento temporal

- todos los artefactos persistentes se suben a MinIO

Esto garantiza que:

- el pipeline sea completamente reproducible

- no existan dependencias del entorno local

- el almacenamiento persistente esté desacoplado

El pipeline puede ejecutarse íntegramente dentro del clúster Kubernetes sin acceso al filesystem del host.
