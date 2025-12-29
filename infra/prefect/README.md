# Prefect — Orquestación del pipeline MLOps

## 📌 Rol de Prefect en el sistema

**Prefect** es el motor de orquestación del pipeline MLOps del proyecto `cybersec-mlops-pipeline`.

Su función principal es **coordinar, ejecutar y trazar** todas las fases del pipeline de forma:

- reproducible
- observable
- desacoplada
- preparada para Kubernetes

Prefect no ejecuta lógica de negocio, sino que **orquesta flujos de trabajo** compuestos por tareas independientes.

---

## 🎯 Objetivos de usar Prefect

La elección de Prefect responde a los siguientes objetivos técnicos:

- Orquestar pipelines batch de forma declarativa
- Separar lógica de datos y control de ejecución
- Obtener trazabilidad por ejecución (flow runs)
- Facilitar retries, logging y estados
- Integrarse de forma nativa con Kubernetes
- Evitar soluciones ad-hoc (scripts secuenciales)

📌 Prefect permite evolucionar el pipeline sin reescribir la lógica existente.

---

## 🔁 Modelo de ejecución adoptado

El proyecto utiliza **Prefect 2.x en modo orchestration-first**, con las siguientes características:

- Cada fase del pipeline es un **flow independiente**
- El pipeline completo se ejecuta como un **flow compuesto**
- La ejecución se lanza mediante un **Kubernetes Job**
- No existe dependencia del entorno local

Los flows definidos son:

```text
data_ingestion_flow        → Ingesta (RAW)
data_transformation_flow  → Transformación (SILVER)
model_training_flow       → Entrenamiento (MODELS)
model_evaluation_flow     → Evaluación (EVAL)
full_mlops_flow           → Orquestador end-to-end
```

## 🧩 Rol de full_mlops_flow.py

El archivo:

```text
pipeline/full_mlops_flow.py
```

actúa como **orquestador principal** del sistema.

Sus responsabilidades son:

- Encadenar los subflows en orden lógico

- Propagar la ejecución de extremo a extremo

- Centralizar la ejecución batch

- Permitir una única entrada al pipeline completo

📌 `full_mlops_flow` **no contiene lógica de datos**, solo orquestación.

---

## 📦 Gestión de estado y almacenamiento temporal

Durante la ejecución del pipeline:

- Los archivos locales (`/data`, `/tmp`) **existen únicamente dentro del contenedor**

- Se utilizan como **almacenamiento temporal**

- Todos los artefactos persistentes se suben a MinIO

Esto garantiza que:

- el pipeline sea completamente reproducible

- no existan dependencias del entorno local

- el almacenamiento persistente esté desacoplado (MinIO)

El pipeline puede ejecutarse íntegramente dentro del clúster Kubernetes sin acceso al filesystem del host.

---

## 🧾 Observabilidad y trazabilidad

Prefect proporciona observabilidad nativa mediante:

- estados de ejecución (`Completed`, `Failed`, etc.)

- logs por task

- identificación única de cada flow run

Esta información permite:

- depurar errores rápidamente

- auditar ejecuciones históricas

- validar la correcta ejecución del pipeline

📌 En este proyecto, Prefect se utiliza como **fuente de verdad operacional**, complementada por PostgreSQL para auditoría estructurada.

---

## ⚙️ Ejecución en Kubernetes

El pipeline se ejecuta en Kubernetes mediante un **Job**, que lanza el flow principal:

```text
full_mlops_flow
```

Características clave:

- ejecución batch (no long-running)

- contenedores efímeros

- escalable horizontalmente

- desacoplado del entorno local

Este enfoque es representativo de pipelines MLOps reales en entornos productivos.

---

## ⚠️ Alcance actual

En el estado actual del proyecto:

✔️ Prefect orquesta todo el pipeline
✔️ Se ejecuta correctamente en Kubernetes
✔️ No depende de Prefect Cloud (se prioriza ejecución on-premise y control total del entorno)
✔️ No utiliza scheduling automático

No se incluyen todavía:

- Prefect deployments

- Schedules periódicos

- Triggering basado en eventos

Estas funcionalidades se consideran **trabajo futuro**, no necesarias para validar el pipeline MLOps.

---

## 🧠 Justificación académica

El uso de Prefect demuestra:

- diseño modular de pipelines

- separación clara de responsabilidades

- uso de herramientas estándar MLOps

- alineación con buenas prácticas industriales

Prefect se utiliza como **herramienta de orquestación**, no como dependencia crítica de negocio, lo que mantiene el sistema flexible y extensible.

---

## 🚀 Trabajo futuro

Posibles evoluciones relacionadas con Prefect:

- Schedules diarios de ejecución

- Retries configurables por task

- Alertas ante fallos

- Versionado de flows

Estas mejoras pueden añadirse sin modificar la lógica existente del pipeline.


---

## 🚀 Instalación de Prefect (contexto de infraestructura)

> Esta sección describe cómo se despliega Prefect en el clúster Kubernetes.
> No forma parte de la lógica del pipeline ni es necesaria para entender su funcionamiento.


```yaml
helm repo add prefect https://prefecthq.github.io/prefect-helm
helm repo update

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