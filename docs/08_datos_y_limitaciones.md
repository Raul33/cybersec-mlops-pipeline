# 08 — Datos utilizados y limitaciones del sistema

## 📌 Introducción

Este capítulo describe los **datos utilizados** en el proyecto y analiza de forma crítica las **limitaciones técnicas y metodológicas** del sistema desarrollado.

El objetivo no es únicamente enumerar restricciones, sino **justificar conscientemente las decisiones tomadas**, alineándolas con el alcance académico y los objetivos del Trabajo Fin de Máster.

---

## 📊 Datos utilizados en el proyecto

### 🧪 Naturaleza de los datos

El sistema utiliza **datos sintéticos de eventos de red**, generados de forma programática durante la fase de ingesta del pipeline MLOps.

Cada dataset simula tráfico de red básico, incluyendo campos como:

- timestamp
- dirección IP origen
- dirección IP destino
- volumen de bytes
- duración de la comunicación
- protocolo de red

Estos datos se generan en cada ejecución del pipeline, permitiendo un entorno **controlado, reproducible y sin dependencias externas**.

---

### 🎯 Justificación del uso de datos sintéticos

El uso de datos sintéticos se justifica por varios motivos clave:

- Evitar el uso de datos sensibles o confidenciales
- Cumplir principios éticos y legales
- Garantizar reproducibilidad del sistema
- Facilitar la validación académica del pipeline
- Focalizar el trabajo en la arquitectura MLOps y no en el dataset

📌 En entornos reales de ciberseguridad, los datasets suelen estar protegidos por acuerdos de confidencialidad, lo que hace habitual el uso de datos simulados en contextos académicos.

---

### 🧱 Rol de los datos dentro del pipeline

Los datos sintéticos cumplen un rol fundamental:

- activan todas las fases del pipeline MLOps
- permiten validar la trazabilidad end-to-end
- habilitan el entrenamiento y evaluación del modelo
- permiten generar artefactos reales (parquets, modelos, métricas)

El objetivo del proyecto no es maximizar el rendimiento predictivo, sino **demostrar la viabilidad y solidez del sistema MLOps completo**.

---

## ⚠️ Limitaciones del sistema

### 📉 Ausencia de datos reales

La principal limitación del sistema es la **ausencia de datos reales de producción**.

Esto implica que:

- los resultados del modelo no son directamente extrapolables a un SOC real
- no se evalúan ataques avanzados o comportamientos complejos
- no se representan escenarios de alta variabilidad temporal

No obstante, esta limitación es aceptable y habitual en un contexto académico.

---

### 🧠 Aprendizaje no supervisado

El sistema utiliza **aprendizaje no supervisado**, lo que conlleva ciertas restricciones:

- ausencia de ground truth explícito
- evaluación basada en métricas indirectas
- dificultad para medir precisión real

Sin embargo, este enfoque refleja fielmente la realidad de muchos sistemas de detección de anomalías en ciberseguridad, donde las etiquetas no están disponibles.

---

### 🧪 Simplificación del dominio

El dominio del problema se ha simplificado deliberadamente:

- número reducido de features
- tráfico de red básico
- ausencia de correlación temporal compleja
- ausencia de múltiples fuentes de datos

Esta simplificación permite centrarse en la **arquitectura MLOps**, evitando que la complejidad del dominio opaque los objetivos del trabajo.

---

### ⚙️ Alcance del sistema

El sistema desarrollado:

- no incluye detección en tiempo real
- no implementa modelos supervisados
- no despliega el modelo como servicio online
- no incluye monitorización continua de deriva
- no integra MLflow como eje central

Estas decisiones responden a una **delimitación clara del alcance**, necesaria para mantener el proyecto viable y coherente.

---

## 🧠 Valor académico del enfoque adoptado

A pesar de las limitaciones descritas, el proyecto aporta valor académico al:

- diseñar un pipeline MLOps completo y funcional
- integrar múltiples tecnologías reales (Kubernetes, Prefect, MinIO, PostgreSQL)
- aplicar principios de ingeniería de datos y MLOps
- demostrar trazabilidad y reproducibilidad end-to-end
- reflejar buenas prácticas industriales en un entorno controlado

El enfoque prioriza la **calidad del diseño** frente a la complejidad innecesaria.

---

## 📌 Conclusión

Las limitaciones del sistema son conocidas, explícitas y justificadas.

El uso de datos sintéticos y aprendizaje no supervisado no supone una debilidad, sino una **decisión consciente alineada con el contexto académico y los objetivos del proyecto**.

El sistema desarrollado sienta una base sólida sobre la que podrían incorporarse, en un entorno futuro, datos reales, modelos más complejos y capacidades avanzadas sin modificar la arquitectura fundamental.
