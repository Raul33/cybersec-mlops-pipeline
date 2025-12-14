# 📦 Apache Airflow - Orquestador de Pipelines MLOps

Apache Airflow es la herramienta que utilizaremos para orquestar todo el ciclo de vida del proyecto MLOps: desde la preparación de datos hasta el reentrenamiento de modelos. Se despliega en Kubernetes con Helm y utiliza:

- PostgreSQL como metastore
- Redis como broker (en caso de usar CeleryExecutor)
- MLflow, MinIO y otros servicios del ecosistema como tareas del pipeline

---

## 🚀 Instalación con Helm

```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

### 📁 Archivo de configuración

Ruta: `infra/mlflow/values-airflow.yaml`

Incluye configuraciones como:

- Conexión a PostgreSQL

- Fernet Key

- Webserver y Scheduler settings

- Persistent Volumes para logs y DAGs


### 💻 Comando de instalación

```yaml
helm install airflow apache-airflow/airflow \
  --namespace mlops \
  -f infra/airflow/values-airflow.yaml
```

### ✅ Verificación

```yaml
kubectl get pods -n mlops

```

### 🌐 Acceso local

```yaml
kubectl port-forward svc/airflow-api-server -n mlops 8080:8080

```
Luego accede en:

```yaml
http://localhost:8080

```
Credenciales por defecto (cambiar):

```yaml
Usuario: admin
Contraseña: admin
```
