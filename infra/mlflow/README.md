# 📦 MLflow - Tracking de experimentos

MLflow es la herramienta de registro de experimentos, métricas y modelos que utilizaremos en este proyecto. Se despliega en Kubernetes con Helm y utiliza:

- PostgreSQL como backend para persistencia
- MinIO como almacenamiento de artefactos

---

## 🚀 Instalación con Helm

```yaml
helm repo add community-charts https://community-charts.github.io/helm-charts
helm repo update
```

### 📁 Archivo de configuración

Ruta: `infra/mlflow/values-mlflow.yaml`

### 🛠️ Pre-requisito: Crear base de datos mlflow en PostgreSQL

Antes de instalar MLflow, es necesario asegurarse de que exista la base de datos mlflow en el PostgreSQL del clúster.
Esto se puede hacer fácilmente con un cliente temporal:

```yaml
kubectl run -it --rm psql-client \
  --image=bitnami/postgresql \
  --namespace mlops \
  --env="PGPASSWORD=mlops_pass" \
  --command -- psql -h mlops-postgresql -U postgres

```
Una vez dentro del cliente interactivo psql, ejecuta:

```yaml
CREATE DATABASE mlflow;
\l
```

Verifica que la base de datos aparezca listada y luego sal con:

```yaml
\q
```

### 💻 Comando de instalación

```yaml
helm install mlflow community-charts/mlflow \
  --namespace mlops \
  -f infra/mlflow/values-mlflow.yaml \
  --wait
```

### ✅ Verificación

```yaml
kubectl get pods -n mlops

```

### 🌐 Acceso local

```yaml
kubectl port-forward svc/mlflow -n mlops 5000:5000

```
Luego accede en:

```yaml
http://localhost:5000

```