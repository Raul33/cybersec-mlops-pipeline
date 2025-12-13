# cybersec-mlops-pipeline
📡 MLOps pipeline on-premises para detección de anomalías y correlación de incidentes en ciberseguridad mediante modelos no supervisados y reglas Sigma. 100 % OSS sobre Kubernetes.


## 📓 Notebooks

Esta carpeta contiene los notebooks utilizados para el análisis exploratorio, el diseño del modelo y la validación conceptual del sistema de detección de anomalías.

### `deteccion_anomalias_explicado.ipynb`

Notebook principal del proyecto. Sirve como **base conceptual y técnica** de toda la aplicación posterior.

Incluye:

- Simulación y carga de eventos de red
- Extracción de características (*features*) relevantes
- Entrenamiento de modelos de detección de anomalías:
  - Isolation Forest
  - Local Outlier Factor (LOF)
  - One-Class SVM
- Evaluación comparativa de modelos
- Explicación de métricas (TP, FP, scores)
- Ejemplo de correlación simulada con reglas Sigma
- Justificación del modelo final elegido (Isolation Forest)

Este notebook **no forma parte de la aplicación en producción**, sino que documenta el razonamiento y las decisiones técnicas que justifican la arquitectura del sistema.


## 📁 Estructura del Proyecto

```bash
cybersec-mlops-pipeline/
├── data/                  # Datos de entrada y salida del sistema
│   ├── normalized/        # Dataset de eventos procesado (formato Parquet)
│   └── alerts_ml.csv      # Alertas generadas por el modelo ML
│
├── docs/                  # Documentación técnica y de arquitectura
│   ├── 01_objetivos.md
│   ├── 02_metricas.md
│   └── 03_estructura.md
│
├── frontend/              # Aplicación de visualización con Streamlit
│   └── streamlit_app.py
│
├── ml/                    # Lógica de entrenamiento y scoring del modelo ML
│   ├── anomaly_detector.py
│   └── features.py
│
├── models/                # Modelo entrenado (Isolation Forest .joblib)
│   └── iforest.joblib
│
├── notebooks/             # Notebook explicativo del sistema
│   └── deteccion_anomalias_explicado.ipynb
│
├── scripts/               # Scripts de ejecución y automatización
│   ├── generate_test_parquet.py
│   ├── run_iforest.py
│   ├── score_events.py
│   └── train_iforest.py
│
├── Dockerfile             # Definición de imagen Docker
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación principal del repositorio


## 🧠 Scripts principales

| Script                             | Descripción                                                  |
|------------------------------------|--------------------------------------------------------------|
| `scripts/train_iforest.py`         | Entrena y guarda modelo Isolation Forest                    |
| `scripts/score_events.py`          | Puntúa eventos usando el modelo entrenado                   |
| `scripts/run_iforest.py`           | Filtra eventos anómalos y genera alertas ML                |
| `scripts/run_pipeline.py`          | Automatiza el flujo de entrenamiento, scoring y alertas     |
| `rules/sigma_emulator.py`          | Simula reglas Sigma sobre eventos para detección basada en reglas |


# Streamlit App

## Decisión del Modelo

Se ha optado por mantener **Isolation Forest** como el único modelo desplegado activamente en producción, por las siguientes razones:

- Ofrece un buen rendimiento general.
- Presenta una interpretación sencilla de los resultados.
- Permite mantener el backend y la lógica de alertado más simple.

Los otros dos modelos (`LOF` y `OCSVM`) están disponibles únicamente en la pestaña de evaluación, donde pueden ser comparados con `IForest` en cuanto a distribución de scores y detección de outliers.

Esta decisión está documentada en el código (`frontend/streamlit_app.py`) y en la lógica de backend que alimenta la app.

---

## Visualización en la App

- Pestaña **"Anomalías ML"**: muestra únicamente las alertas generadas por `Isolation Forest` (`alerts_ml.csv`).
- Pestaña **"Evaluación"**: permite seleccionar entre los tres modelos para comparar su comportamiento de forma interactiva.

---

## Archivos Relevantes

- `ml/anomaly_detector.py`: contiene funciones para entrenar y puntuar con `Isolation Forest`.
- `scripts/train_iforest.py`, `score_events.py`, `run_iforest.py`: scripts automatizados del pipeline.
- `frontend/streamlit_app.py`: interfaz web en Streamlit.

---

## Cómo ejecutar

```bash
# Ejecutar el pipeline completo
python3 scripts/run_pipeline.py

# Construir y lanzar la app
docker build -t soc-copilot-app .
docker run -p 8501:8501 -v $(pwd)/data:/app/data soc-copilot-app
```

Una vez lanzada, accede a la app en `http://localhost:8501`.


