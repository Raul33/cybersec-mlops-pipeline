# 🐘 PostgreSQL - Base de datos para servicios MLOps

PostgreSQL se utiliza como backend para herramientas como **MLflow** o **Airflow**, permitiendo guardar metadatos, ejecuciones, experimentos o DAGs. En este caso, se ha desplegado como base de datos común para los servicios que la necesiten.

---

## 🚀 Despliegue en Kubernetes (Helm)

Este despliegue usa el chart oficial de Bitnami, configurado con un usuario, contraseña y base de datos inicial.

---

### 📁 Archivo de configuración

Ruta: `infra/postgresql/values-postgresql.yaml`

### 💻 Comando de instalación

```yaml
helm install mlops-postgresql bitnami/postgresql \
  --namespace mlops \
  -f infra/postgresql/values-postgresql.yaml
```
### 🔌 Conexión desde un pod

Para conectarte a PostgreSQL desde otro contenedor del clúster, usa los siguientes valores:

Host: mlops-postgresql.mlops.svc.cluster.local

Puerto: 5432

Usuario: postgres

Contraseña: mlops_pass

Base de datos: mlops_db

### 🧪 Probar conexión desde dentro del clúster (opcional)

```yaml
kubectl run -it --rm psql-client --image=bitnami/postgresql --namespace mlops \
  --env="PGPASSWORD=mlops_pass" --command -- psql -h mlops-postgresql -U postgres -d mlops_db

```


