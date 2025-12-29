# 🛡️ SOC Copilot – Aplicación de Visualización de Anomalías

Esta aplicación web, desarrollada con **Streamlit**, actúa como **interfaz de visualización y apoyo al analista de seguridad (SOC)** dentro del proyecto `cybersec-mlops-pipeline`.

Su función principal es **mostrar y explorar los resultados generados por el pipeline MLOps**, permitiendo interpretar de forma clara las anomalías detectadas por modelos de machine learning.

> ⚠️ Esta aplicación **no entrena modelos ni ejecuta detección en tiempo real**.  
> Consume artefactos previamente generados por el pipeline batch ejecutado en Kubernetes.

---

## 🎯 Objetivo de la aplicación

El objetivo de SOC Copilot es:

- Facilitar la **interpretación humana** de los resultados de detección de anomalías
- Visualizar scores y distribuciones generadas por modelos ML
- Permitir al analista ajustar umbrales de alerta
- Servir como **prueba de concepto (PoC)** de integración ML + ciberseguridad

La aplicación se centra en la **explicabilidad y exploración**, no en la automatización completa de decisiones.

---

## 🧠 Rol dentro de la arquitectura MLOps

Dentro del sistema completo, la aplicación ocupa la siguiente posición:

- El **pipeline MLOps**:
  - ingesta datos
  - los transforma
  - entrena modelos
  - evalúa resultados
  - almacena artefactos en MinIO

- La **aplicación Streamlit**:
  - consume esos artefactos
  - los presenta de forma visual
  - permite análisis manual

De este modo, se mantiene una separación clara entre:
- **procesamiento automático (pipeline)**
- **análisis asistido por humanos (app)**

---

## 🔌 Fuentes de datos utilizadas

La aplicación se conecta directamente a **MinIO** (object storage) y consume:

### 📦 Modelos entrenados
- Bucket: `cybersec-ml-models`
- Se selecciona automáticamente el **modelo más reciente**
- El modelo se descarga temporalmente en el contenedor

### 📊 Resultados de evaluación
- Bucket: `cybersec-ml-eval`
- Se cargan los resultados más recientes generados por el pipeline
- Los datos se leen en formato **Parquet**

---

## ⚙️ Funcionalidades principales

La aplicación ofrece las siguientes capacidades:

- 📌 Identificación del **último modelo disponible**
- 🔍 Visualización tabular de eventos evaluados
- 🎚️ Ajuste dinámico de un **umbral de alerta ML**
- 📊 Histogramas de distribución de scores
- 📈 Métricas visuales para apoyo a la decisión

El analista puede explorar cómo varían las alertas al modificar el umbral, lo que simula un entorno real de SOC.

---

## 🧪 Alcance y limitaciones

✔️ Incluido:
- Visualización batch
- Exploración de resultados ML
- Análisis manual asistido

❌ No incluido (deliberadamente):
- Entrenamiento de modelos
- Detección en tiempo real
- Streaming de eventos
- Automatización de respuesta

Estas decisiones se tomaron para **mantener el foco en el pipeline MLOps**, que es el núcleo del proyecto.

---

## 🏗️ Arquitectura de ejecución

La aplicación está pensada para ejecutarse:

- Dentro de **Kubernetes**
- Como un **Deployment independiente**
- Utilizando variables de entorno para credenciales
- Sin dependencias de archivos locales persistentes

Todo el estado persistente reside en MinIO.

---

## 🚀 Ejecución

La aplicación puede desplegarse como contenedor Docker o mediante Kubernetes.

El acceso habitual es a través de:

```text
http://<NODE_IP>:8501
```