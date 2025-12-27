# 🧩 Pipeline MLOps – Visión global

Este directorio contiene la implementación completa de un **pipeline MLOps end-to-end** para un sistema de detección de anomalías en eventos de red, diseñado para ejecutarse de forma **reproducible, trazable y desacoplada** sobre Kubernetes.

El pipeline automatiza todo el ciclo de vida del modelo, desde la ingesta de datos hasta la evaluación final, siguiendo principios de **ingeniería MLOps moderna**.

---

## 🎯 Objetivo del pipeline

El objetivo principal del pipeline es:

- Automatizar el procesamiento de eventos de red
- Entrenar y evaluar un modelo de detección de anomalías
- Versionar datasets y modelos
- Registrar eventos clave para auditoría y trazabilidad
- Ejecutarse de forma controlada dentro de un clúster Kubernetes

Este pipeline está pensado para **entornos de ciberseguridad**, donde la reproducibilidad y la trazabilidad son críticas.

---

## 🔄 Flujo general del pipeline

El pipeline se compone de cuatro grandes fases, orquestadas de forma secuencial:

1. **Ingesta de datos**
2. **Transformación**
3. **Entrenamiento del modelo**
4. **Evaluación**

Cada fase está implementada como un **flow independiente de Prefect**, lo que permite:

- Reutilización
- Aislamiento de responsabilidades
- Escalabilidad futura
- Observabilidad del proceso completo

---

## 🧠 Arquitectura lógica

A alto nivel, el pipeline sigue la siguiente lógica:

- **Prefect** actúa como orquestador del flujo completo
- **MinIO** se utiliza como data lake y model registry
- **PostgreSQL** almacena metadatos de ejecución
- **Kubernetes** ejecuta el pipeline como un Job desacoplado

Todo el pipeline puede ejecutarse sin dependencias locales, utilizando únicamente servicios internos del clúster.

---

## 📦 Componentes principales

El pipeline está organizado en los siguientes módulos:

```text
pipeline/
├── full_mlops_flow.py        # Orquestador principal del pipeline
├── ingestion/                # Ingesta de datos (RAW)
├── transformation/           # Transformación y feature engineering (SILVER)
├── training/                 # Entrenamiento del modelo
├── evaluation/               # Evaluación del modelo
└── config/                   # Configuración compartida (features, esquemas, etc.)
```

---

## 📊 Gestión de datos y modelos

El pipeline implementa una separación clara de capas:

- RAW: datos ingeridos sin procesar

- SILVER: datos transformados y listos para modelado

- MODELS: artefactos entrenados y versionados

- EVAL: resultados de evaluación

Todos los artefactos se almacenan en MinIO, con nombres versionados basados en timestamps para garantizar reproducibilidad.

---

## 🧾 Trazabilidad y auditoría

Cada ejecución del pipeline registra eventos clave en PostgreSQL, incluyendo:

- Ingestas realizadas

- Transformaciones aplicadas

- Entrenamientos ejecutados

- Evaluaciones completadas

Esto permite responder a preguntas como:

- ¿Qué datos se usaron para entrenar este modelo?

- ¿Cuándo se generó?

- ¿Con qué parámetros?

- ¿Qué métricas obtuvo?

---

## ⚠️ Alcance y decisiones de diseño

Este pipeline no incluye todavía:

- Tracking avanzado con MLflow

- Serving online del modelo

- Monitorización en tiempo real

Estas funcionalidades se consideran trabajo futuro, y se han excluido deliberadamente para mantener el foco en la robustez del pipeline batch, que es la base de cualquier sistema MLOps sólido.