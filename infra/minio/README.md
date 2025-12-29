# MinIO — Almacenamiento de objetos (Data Lake)

## 📌 Rol de MinIO en el sistema

**MinIO** actúa como el sistema de **almacenamiento persistente central** del proyecto `cybersec-mlops-pipeline`.

Su función es proporcionar un **data lake compatible con S3**, desplegado on-premise sobre Kubernetes, que permita:

- almacenar datasets y artefactos ML
- desacoplar completamente el pipeline del filesystem local
- garantizar reproducibilidad y trazabilidad
- simular arquitecturas reales de MLOps en entornos corporativos

MinIO se utiliza como **fuente única de persistencia**, tanto para datos como para modelos y resultados.

---

## 🚀 Despliegue de MinIO en Kubernetes

MinIO se despliega en el clúster Kubernetes mediante **Helm**, utilizando un fichero `values-minio.yaml` personalizado.

Este enfoque permite:

- configuración declarativa
- despliegue reproducible
- fácil adaptación a otros entornos

El despliegue se realiza dentro del namespace `mlops`.

### 📁 Archivo de configuración

Ruta: `infra/minio/values-minio.yaml`

### 💻 Comando de instalación

```yaml
helm upgrade --install mlops-minio minio/minio \
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

> NOTA: 📌 Este bucket se prepara como base para una futura integración con MLflow.

### 🧰 Configurar el cliente mc (opcional)

Si deseas usar el CLI oficial de MinIO para cargar archivos, listar buckets, etc.:

1. Instala mc:
[MinIO client](https://min.io/docs/minio/linux/reference/minio-mc.html)

2. Exporta la conexión local:

```yaml
export MC_HOST_mlops-minio-local=http://user:password@localhost:9001
```
3. Prueba con:

```yaml
mc ls mlops-minio-local
```

### 🔍 Validación y acceso

Durante el desarrollo y validación del sistema se comprobó:

- correcta creación de buckets
- subida de objetos desde el pipeline
- versionado por timestamp
- lectura correcta desde distintos flows

El acceso a la consola web de MinIO se realiza mediante port-forward:

```bash
kubectl port-forward -n mlops svc/minio 9001:9001
```

📌 El puerto 9000 se utiliza exclusivamente para la API S3.

---

## 🧱 Capas de almacenamiento (buckets)

El proyecto implementa una separación clara de responsabilidades mediante distintos buckets:

```text
cybersec-ml-raw       → datos ingeridos sin procesar
cybersec-ml-silver    → datos transformados y enriquecidos
cybersec-ml-models    → modelos entrenados
cybersec-ml-eval      → resultados de evaluación
```
Cada bucket representa una **fase del ciclo de vida del dato o del modelo**, facilitando:

- auditoría

- versionado

- rollback

- reutilización de artefactos

---

## 🔁 Integración con el pipeline MLOps

MinIO se integra con el pipeline MLOps en todas sus fases:

- Ingesta → escritura en `cybersec-ml-raw`
- Transformación → lectura RAW / escritura SILVER
- Entrenamiento → lectura SILVER / escritura MODELS
- Evaluación → lectura MODELS / escritura EVAL

Todos los flows de Prefect utilizan MinIO como backend de persistencia, accediendo mediante la API S3 y variables de entorno.

📌 Ningún artefacto crítico se almacena de forma persistente en el contenedor.

---

## ⚠️ Alcance actual

En el estado actual del proyecto, MinIO se utiliza como:

✔️ data lake on-premise  
✔️ almacenamiento de datasets y modelos  
✔️ backend S3 para pipelines batch  

No se incluyen todavía:

- versionado avanzado de objetos
- políticas de retención
- cifrado en reposo
- integración con MLflow

Estas mejoras se consideran **trabajo futuro**.
