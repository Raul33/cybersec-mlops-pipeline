# Deployment Streamlit — SOC Copilot

## 📌 Rol del componente

El componente **SOC Copilot** es una aplicación web desarrollada con **Streamlit**, encargada de visualizar los resultados del pipeline MLOps:

- modelos entrenados
- resultados de evaluación
- scores de anomalía

Este componente **no ejecuta lógica de entrenamiento**, sino que consume artefactos ya generados y almacenados en MinIO.

---

## 🧱 Tipo de recurso Kubernetes

La aplicación se despliega mediante un:

```text
kind: Deployment
```

Esto permite:

- ejecución continua (long-running)

- reinicios automáticos en caso de fallo

- gestión sencilla del ciclo de vida

- escalabilidad futura

A diferencia del pipeline batch (Job), la UI debe estar siempre disponible.

---

## 🖼 Imagen de contenedor

La aplicación se construye como una imagen Docker ligera:

```text
soc-copilot:ui-light
```

Características:

- optimizada para ejecución de UI

- sin dependencias de entrenamiento

- orientada a lectura de datos

El `imagePullPolicy: IfNotPresent` evita descargas innecesarias y estabiliza la ejecución.

---

## 🔐 Gestión de credenciales

El Deployment utiliza **Kubernetes Secrets** para acceder a MinIO:

- `MINIO_ACCESS_KEY`

- `MINIO_SECRET_KEY`

Las credenciales no están embebidas en el código ni en los manifiestos.


---

## 📦 Almacenamiento

La aplicación monta un volumen:

```text
emptyDir: {}
```

Este volumen:

- existe solo durante la vida del pod

- se usa para almacenamiento temporal

- no contiene datos persistentes

📌 Los datos persistentes siempre se leen desde MinIO.
---

## 🌐 Exposición del servicio

La aplicación se expone mediante un **Service NodePort**:

```text
NodePort: 30010
```
Este enfoque es adecuado para:

- entornos on-premise

- laboratorios

- validación académica

En entornos productivos podría sustituirse por un Ingress con TLS.

---

## 🔗 Integración con el pipeline MLOps

SOC Copilot se integra con el resto del sistema de la siguiente forma:

- consume modelos desde `cybersec-ml-models`

- consume evaluaciones desde `cybersec-ml-eval`

- utiliza MinIO como backend común

- no depende del pipeline en tiempo real

Esto garantiza:

- desacoplamiento total

- robustez del sistema

- separación clara de responsabilidades

