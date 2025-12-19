# 📦 Prefect
---

## 🚀 Instalación con Helm

```yaml
helm repo add prefect https://prefecthq.github.io/prefect-helm
helm repo update

```

### 📁 Archivo de configuración


### 🛠️ Pre-requisito: Crear base de datos mlflow en PostgreSQL



```yaml


```


### 💻 Comando de instalación

```yaml
helm upgrade --install prefect prefect/prefect-server \
  -n mlops
```

### ✅ Verificación

```yaml
kubectl get pods -n mlops

```

### 🌐 Acceso local

```yaml
kubectl port-forward -n mlops svc/prefect-server 4200:4200

```
Luego accede en:

```yaml
http://localhost:4200

```