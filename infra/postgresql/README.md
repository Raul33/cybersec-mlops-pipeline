# 🐘 PostgreSQL — Base de datos de auditoría y trazabilidad MLOps

PostgreSQL se utiliza en el proyecto `cybersec-mlops-pipeline` como **base de datos central de auditoría y metadatos operacionales** del pipeline MLOps.

Su función principal es **registrar, persistir y consultar información estructurada** sobre cada ejecución del pipeline, incluyendo:

- ingestas de datos
- transformaciones aplicadas
- entrenamientos de modelos
- evaluaciones realizadas

PostgreSQL actúa como **fuente de verdad histórica** del sistema, complementando a Prefect (observabilidad) y MinIO (persistencia de artefactos).


---

## 🎯 Rol de PostgreSQL en el pipeline MLOps

PostgreSQL se utiliza como **capa de auditoría transversal** a todo el pipeline MLOps.

A diferencia de MinIO (almacenamiento de artefactos) y Prefect (orquestación), PostgreSQL permite:

- registrar eventos estructurados por ejecución
- consultar histórico de ejecuciones
- auditar qué datos y modelos se usaron
- responder a preguntas operativas y académicas

Ejemplos de preguntas que PostgreSQL permite responder:

- ¿Cuándo se ejecutó por última vez el pipeline?
- ¿Qué dataset se utilizó para entrenar un modelo concreto?
- ¿Cuántos registros procesó cada fase?
- ¿Qué ejecuciones fallaron o tuvieron resultados anómalos?

📌 Esta base de datos **no se utiliza para datos de negocio**, sino exclusivamente para **metadatos MLOps**.

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

Contraseña: ****

Base de datos: mlops_db

### 🧪 Probar conexión desde dentro del clúster (opcional)

```yaml
kubectl run -it --rm psql-client --image=bitnami/postgresql --namespace mlops \
  --env="PGPASSWORD=****" --command -- psql -h mlops-postgresql -U postgres -d mlops_db

```

---

## 🗄️ Esquema de auditoría utilizado

El pipeline MLOps utiliza varias tablas para registrar eventos operacionales. Cada fase del pipeline inserta un registro por ejecución.

### 📥 Tabla `ingestion_events`

Registra cada ingesta de datos en la capa RAW.

Campos principales:
- timestamp_ingesta
- nombre_archivo
- ruta_minio
- num_registros
- estado

---

### 🔄 Tabla `transformation_events`

Registra cada transformación RAW → SILVER.

Campos principales:
- timestamp_transformacion
- nombre_archivo
- ruta_minio
- num_registros
- estado

---

### 🧠 Tabla `training_events`

Registra cada entrenamiento de modelo.

Campos principales:
- timestamp_entrenamiento
- ruta_modelo
- num_registros
- parametros
- estado

---

### 📊 Tabla `evaluation_events`

Registra cada evaluación del modelo entrenado.

Campos principales:
- timestamp_eval
- modelo_nombre
- nombre_dataset
- ruta_resultados
- metrics
- estado



