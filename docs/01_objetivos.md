# 🎯 Objetivos del Proyecto

## 1. Contexto general

El presente proyecto tiene como objetivo el diseño e implementación de un **sistema MLOps completo para la detección de anomalías en eventos de red**, aplicado a un contexto de **ciberseguridad**.

El trabajo se desarrolla como **Trabajo de Fin de Máster (TFM)** y combina aspectos de:

- aprendizaje automático no supervisado
- ingeniería de datos
- arquitectura MLOps
- despliegue y ejecución en entornos orquestados con Kubernetes

El sistema está diseñado para ejecutarse **on-premise**, sin dependencias de servicios cloud propietarios, utilizando únicamente tecnologías **open-source**.

---

## 2. Objetivo principal

El objetivo principal del proyecto es **construir un pipeline MLOps end-to-end**, reproducible y trazable, capaz de:

- ingerir eventos de red
- transformarlos y enriquecerlos
- entrenar modelos de detección de anomalías
- evaluar su comportamiento
- registrar todos los artefactos y metadatos generados

Todo el ciclo de vida del modelo se ejecuta de forma **automatizada dentro de un clúster Kubernetes**, siguiendo principios de ingeniería MLOps moderna.

---

## 3. Objetivos específicos

Para alcanzar el objetivo principal, se definen los siguientes objetivos específicos:

### 3.1 Detección de anomalías en ciberseguridad

- Analizar técnicas de **detección de anomalías no supervisadas** aplicadas a eventos de red.
- Comparar diferentes algoritmos (Isolation Forest, LOF, One-Class SVM) en un entorno controlado.
- Seleccionar un modelo base adecuado para su uso en producción.

### 3.2 Diseño de un pipeline MLOps reproducible

- Diseñar un pipeline batch dividido en fases claramente separadas:
  - ingesta (RAW)
  - transformación (SILVER)
  - entrenamiento (MODELS)
  - evaluación (EVAL)
- Garantizar la reproducibilidad de los resultados mediante versionado de datos y modelos.

### 3.3 Orquestación y automatización

- Utilizar **Prefect** como orquestador de flujos MLOps.
- Ejecutar el pipeline completo como un **Job en Kubernetes**, sin dependencias del entorno local.
- Permitir la ejecución desatendida y repetible del sistema.

### 3.4 Gestión de datos y artefactos

- Utilizar **MinIO** como sistema de almacenamiento de objetos para datasets y modelos.
- Implementar una separación clara de capas (RAW / SILVER / MODELS / EVAL).
- Versionar todos los artefactos generados mediante timestamps.

### 3.5 Trazabilidad y auditoría

- Registrar eventos clave del pipeline en **PostgreSQL**:
  - ingestas realizadas
  - transformaciones aplicadas
  - entrenamientos ejecutados
  - evaluaciones del modelo
- Garantizar la trazabilidad completa del ciclo de vida del modelo.

### 3.6 Visualización y análisis

- Desarrollar una aplicación **Streamlit** para visualizar resultados de detección de anomalías.
- Facilitar la interpretación de los scores generados por el modelo.
- Mostrar información relevante para analistas de seguridad de forma accesible.

---

## 4. Alcance del proyecto

El alcance del proyecto incluye:

- pipeline batch MLOps completo
- detección de anomalías no supervisada
- ejecución en Kubernetes
- almacenamiento desacoplado
- auditoría y trazabilidad

Quedan explícitamente fuera del alcance:

- inferencia en tiempo real
- despliegue como servicio online
- monitorización en producción del modelo
- integración completa con SIEM reales

Estas funcionalidades se consideran **trabajo futuro**.
