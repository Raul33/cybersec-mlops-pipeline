# 09 — Conclusiones y trabajo futuro

## 📌 Introducción

En este capítulo se presentan las **conclusiones finales** del Trabajo Fin de Máster y se describen las **posibles líneas de evolución futura** del sistema desarrollado.

El objetivo es cerrar el proyecto de forma coherente, evaluando el grado de cumplimiento de los objetivos planteados y contextualizando el valor del trabajo realizado dentro del ámbito de la ingeniería MLOps aplicada a la ciberseguridad.

---

## ✅ Grado de cumplimiento de los objetivos

El proyecto ha cumplido satisfactoriamente los objetivos definidos al inicio del trabajo.

En concreto, se ha logrado:

- diseñar e implementar un pipeline MLOps completo y funcional
- automatizar todo el ciclo de vida del modelo de forma reproducible
- aplicar técnicas de detección de anomalías no supervisadas
- garantizar trazabilidad y auditoría end-to-end
- ejecutar el sistema íntegramente sobre Kubernetes
- integrar herramientas estándar del ecosistema MLOps

El sistema funciona como una **prueba de concepto sólida** que demuestra la viabilidad técnica del enfoque propuesto.

---

## 🧠 Aportaciones principales del trabajo

Las principales aportaciones del proyecto son las siguientes:

### 🔹 Diseño de una arquitectura MLOps realista

Se ha diseñado una arquitectura inspirada en entornos industriales reales, incorporando:

- separación clara de capas (RAW, SILVER, MODELS, EVAL)
- orquestación de pipelines con Prefect
- almacenamiento de objetos con MinIO
- auditoría estructurada mediante PostgreSQL
- ejecución desacoplada sobre Kubernetes

Esta arquitectura puede escalarse o adaptarse fácilmente a contextos productivos.

---

### 🔹 Integración de MLOps y ciberseguridad

El proyecto demuestra cómo los principios MLOps pueden aplicarse eficazmente a un caso de uso de ciberseguridad, donde:

- los datos son dinámicos
- las etiquetas son escasas o inexistentes
- la trazabilidad es crítica
- la reproducibilidad es obligatoria

Este enfoque es especialmente relevante para SOCs y entornos de detección de amenazas.

---

### 🔹 Enfoque académico riguroso y justificable

Todas las decisiones técnicas tomadas han sido:

- documentadas
- justificadas
- alineadas con el alcance del trabajo

El uso de datos sintéticos y aprendizaje no supervisado responde a una delimitación consciente del problema y no compromete el valor académico del proyecto.

---

## ⚠️ Limitaciones identificadas

A lo largo del desarrollo se han identificado diversas limitaciones, entre las que destacan:

- uso de datos sintéticos en lugar de datos reales
- ausencia de etiquetas reales para evaluación supervisada
- evaluación basada en métricas indirectas
- falta de inferencia en tiempo real
- ausencia de monitorización continua del modelo

Estas limitaciones han sido aceptadas deliberadamente para mantener el proyecto acotado y viable.

---

## 🚀 Líneas de trabajo futuro

El sistema desarrollado permite múltiples extensiones futuras sin necesidad de rediseñar la arquitectura base.

Entre las posibles líneas de evolución destacan:

### 🔹 Integración completa de MLflow

- tracking de experimentos
- versionado avanzado de modelos
- gestión de métricas históricas
- comparación entre ejecuciones

---

### 🔹 Despliegue del modelo como servicio

- creación de una API de inferencia (FastAPI)
- despliegue como microservicio
- integración con herramientas de seguridad existentes

---

### 🔹 Monitorización avanzada en producción

- detección de data drift y concept drift
- alertas automáticas
- métricas operacionales en tiempo real
- integración con Prometheus y Grafana

---

### 🔹 Uso de datos reales y escenarios complejos

- ingestión de logs reales (Zeek, Suricata, Sysmon)
- correlación multi-fuente
- enriquecimiento con fuentes externas
- evaluación con ground truth parcial

---

### 🔹 Automatización avanzada del pipeline

- ejecución programada mediante schedules
- triggering basado en eventos
- estrategias de retraining automático
- políticas de retención de datos y modelos

---

## 🧠 Conclusión final

Este Trabajo Fin de Máster demuestra que es posible construir un sistema MLOps completo, reproducible y alineado con buenas prácticas industriales, incluso en contextos complejos como la ciberseguridad.

El proyecto no pretende ser un sistema productivo final, sino una **base arquitectónica sólida**, extensible y bien fundamentada, sobre la que pueden construirse soluciones reales de mayor complejidad.

Desde un punto de vista académico y técnico, el trabajo cumple con los objetivos planteados y aporta una visión clara de cómo aplicar MLOps de forma rigurosa y práctica en sistemas de detección de anomalías.

---

