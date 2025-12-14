# 📦 MinIO - Almacenamiento de objetos

MinIO actúa como almacenamiento de objetos compatible con S3, utilizado por MLflow, Airflow y otras herramientas MLOps.

---

## 🚀 Despliegue en Kubernetes (Helm)

Este despliegue se realiza con recursos mínimos para laboratorios con recursos limitados (ej: entornos caseros o pruebas).

### 📁 Archivo de configuración

Ruta: `infra/minio/values-minio.yaml`

### ⚙️ Comando de instalación

```yaml
helm install mlops-minio minio/minio \
  --namespace mlops \
  -f infra/minio/values-minio.yaml \
  --set accessKey=minioaccess \
  --set secretKey=miniosecret \
  --wait
```

### 🌐 Acceso a la interfaz web

```yaml
kubectl port-forward pod/mlops-minio-5bb7657bf6-8ngrn -n mlops 9001:9001
```
### 🪣 Crear un bucket

Una vez dentro de la interfaz:

Clic en Buckets > + Create Bucket

Asignar un nombre, por ejemplo: mlflow-artifacts

Configuración por defecto

Este bucket lo usaremos para MLflow y otros servicios que requieran almacenamiento S3.

### 🧰 Configurar el cliente mc (opcional)

Si deseas usar el CLI oficial de MinIO para cargar archivos, listar buckets, etc.:

1. Instala mc:
[anchor](https://min.io/docs/minio/linux/reference/minio-mc.html)

2. Exporta la conexión local:

```yaml
export MC_HOST_mlops-minio-local=http://user:password@localhost:9001
```
3. Prueba con:

```yaml
mc ls mlops-minio-local
```
