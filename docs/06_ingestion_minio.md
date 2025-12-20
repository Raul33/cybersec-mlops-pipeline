# 06 — Ingesta de datos + almacenamiento en MinIO (on-premises)

## 📌 Objetivo
En esta fase se implementa la ingesta de datos en modo batch diario, la validación básica, el guardado local en formato parquet y la subida automática a almacenamiento distribuido S3-compatible usando MinIO desplegado sobre Kubernetes.

Esta fase consolida el primer tramo del pipeline MLOps real.

---

## 📌 Tecnologías usadas
- Prefect 2.14.10 → orquestación
- MinIO 2025.x → almacenamiento S3 on-premises
- Python 3.11 → ejecución
- Parquet + PyArrow → formato columna eficiente
- Kubernetes + port-forward → acceso local

---

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

