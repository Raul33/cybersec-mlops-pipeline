# 📜 Documentación de Scripts del Proyecto

Este documento describe la funcionalidad de cada uno de los scripts contenidos en la carpeta `scripts/`. Cada uno cumple un rol dentro del flujo de detección de anomalías mediante aprendizaje automático.

---

## `generate_test_parquet.py`

🔧 **Función**: Genera un archivo Parquet con datos de ejemplo simulados para pruebas.

📥 **Input**: No requiere entradas externas.

📤 **Output**: Crea `data/normalized/zeek.parquet`.

🧠 **Uso principal**: Proporciona una base mínima de datos para entrenar y probar los modelos.

---

## `train_iforest.py`

🤖 **Función**: Entrena el modelo Isolation Forest usando los datos de entrada.

📥 **Input**: `data/normalized/zeek.parquet`

📤 **Output**: Modelo guardado en `models/iforest.joblib`

🧠 **Uso principal**: Crear un modelo capaz de detectar anomalías basado en los eventos de red.

---

## `score_events.py`

📊 **Función**: Usa el modelo entrenado para puntuar nuevos eventos con un `ml_score`.

📥 **Input**: 
- Modelo desde `models/iforest.joblib`
- Datos desde `data/normalized/zeek.parquet`

📤 **Output**: Archivo con resultados en `data/scored.csv`

🧠 **Uso principal**: Evaluar eventos y asignarles una probabilidad de anómalo.

---

## `run_iforest.py`

🚨 **Función**: Detecta alertas en base al `ml_score` y genera un archivo con las más relevantes.

📥 **Input**:
- Modelo: `models/iforest.joblib`
- Eventos: `data/normalized/zeek.parquet`

📤 **Output**: Alertas guardadas en `data/alerts_ml.csv`

🧠 **Uso principal**: Simula un sistema de detección de intrusiones que reporta las anomalías más críticas.

---

## `run_pipeline.py`

⚙️ **Función**: Ejecuta los scripts anteriores en orden para automatizar todo el flujo de trabajo.

🔗 **Incluye**:
1. Entrenamiento del modelo (`train_iforest.py`)
2. Puntuación de eventos (`score_events.py`)
3. Generación de alertas (`run_iforest.py`)

🧠 **Uso principal**: Automatizar el flujo de entrenamiento, evaluación y generación de alertas con un solo comando.

```bash
python3 scripts/run_pipeline.py
