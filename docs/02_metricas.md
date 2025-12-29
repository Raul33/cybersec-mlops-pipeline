# 02 — Métricas de evaluación del sistema

## 📌 Introducción

La evaluación de sistemas de detección de anomalías en ciberseguridad presenta particularidades importantes, especialmente cuando se emplean **modelos de aprendizaje no supervisado**, donde no existe una etiqueta real (*ground truth*) completa y fiable.

En este proyecto se utilizan métricas adaptadas a este contexto, priorizando:
- la estabilidad del modelo
- la tasa de alertas generadas
- la coherencia del score de anomalía
- la trazabilidad de resultados

El objetivo no es maximizar una métrica clásica aislada, sino **evaluar el comportamiento global del sistema** dentro de un pipeline MLOps reproducible.

---

## ⚠️ Consideraciones clave en detección de anomalías

A diferencia de problemas de clasificación supervisada:

- no se dispone de etiquetas reales para todos los eventos
- las anomalías son raras y cambiantes
- un exceso de alertas es tan problemático como no detectar ninguna

Por este motivo, métricas como *accuracy* o *ROC-AUC* **no son adecuadas** en este contexto y no se utilizan en el sistema.

---

## 🧠 Tipología de métricas empleadas

Las métricas del proyecto se dividen en cuatro grandes bloques:

1. Métricas basadas en el *score* del modelo  
2. Métricas de tasa de anomalías  
3. Métricas simuladas de clasificación  
4. Métricas operativas del pipeline  

---

## 📊 1️⃣ Métricas basadas en el score de anomalía

El modelo principal (Isolation Forest) genera un **score continuo de anomalía** para cada evento.

### 🔹 Score de anomalía (`anomaly_score`)

- Valor continuo generado por el modelo
- Cuanto más bajo, más anómalo es el evento
- Permite ordenar y priorizar alertas

Este score se utiliza como base para:
- generación de alertas
- visualización en la aplicación Streamlit
- análisis de estabilidad del modelo

---

### 🔹 Media del score (`score_mean`)

Representa el valor medio del score de anomalía en un dataset completo.

**Utilidad:**
- detectar desviaciones globales del modelo
- identificar cambios bruscos en el comportamiento de los datos
- comprobar estabilidad entre ejecuciones

---

### 🔹 Desviación estándar del score (`score_std`)

Mide la dispersión del score de anomalía.

**Utilidad:**
- detectar modelos inestables
- identificar datasets con comportamiento anómalo generalizado
- comparar ejecuciones históricas

---

## 📈 2️⃣ Métrica de tasa de anomalías

### 🔹 Anomaly Rate

Se define como el porcentaje de eventos clasificados como anómalos respecto al total:

```bash
anomaly_rate = nº anomalías / nº total de eventos
```


**Utilidad:**
- controlar el volumen de alertas
- evitar *alert fatigue*
- comparar ejecuciones batch

Esta métrica es especialmente relevante en entornos SOC, donde un exceso de alertas reduce la efectividad operativa.

---

## 🧪 3️⃣ Métricas simuladas de clasificación

Dado que no existe ground truth real, se utiliza una **aproximación simulada**, asumiendo que la mayoría de eventos son normales.

Sobre esta base se calculan:

- Precision
- Recall
- F1-score

Estas métricas:
- **no se interpretan como valores absolutos**
- se usan únicamente para comparar ejecuciones
- ayudan a detectar regresiones del modelo

---

## ⚙️ 4️⃣ Métricas operativas del pipeline

Además de métricas puramente de ML, el sistema registra métricas operativas:

- número de registros procesados
- timestamps de ejecución
- estado de cada fase (SUCCESS / FAILED)
- artefactos generados (datasets, modelos, evaluaciones)

Estas métricas permiten:
- auditoría completa
- reproducibilidad
- análisis forense del pipeline

---

## 🧩 Relación con el pipeline MLOps

Las métricas se calculan y almacenan dentro del pipeline de forma automatizada:

- el módulo de **evaluación** calcula métricas de score y tasa de anomalías
- los resultados se almacenan en MinIO (EVAL layer)
- los metadatos se registran en PostgreSQL

Esto garantiza que cada modelo entrenado esté asociado a:
- un dataset concreto
- unas métricas concretas
- un contexto temporal reproducible

---

## 📌 Justificación del enfoque adoptado

El conjunto de métricas seleccionadas permite:

- evaluar modelos no supervisados de forma realista
- mantener simplicidad conceptual
- evitar métricas engañosas
- facilitar la explicación a público no técnico
- escalar el sistema en el futuro

Este enfoque es coherente con sistemas reales de detección de anomalías utilizados en ciberseguridad.

---

## 🔮 Trabajo futuro en métricas

Como líneas de mejora futuras se consideran:

- incorporación de etiquetas parciales procedentes de analistas
- métricas basadas en feedback humano
- integración con MLflow para tracking avanzado
- análisis temporal de deriva del modelo (*concept drift*)

Estas extensiones no se incluyen en el alcance actual del proyecto para mantener la robustez y claridad del diseño base.