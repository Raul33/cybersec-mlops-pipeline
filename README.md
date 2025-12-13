# cybersec-mlops-pipeline

🚀 **Pipeline MLOps para detección de anomalías en eventos de red**, basado en modelos no supervisados (Isolation Forest, LOF, OCSVM) y reglas Sigma simuladas. Diseñado para ejecutarse on‑premise y escalar fácilmente en Kubernetes (RKE2 + Helm). 100% Open Source.

---

## 📚 Contenidos

- [📓 Notebooks](#-notebooks)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🧠 Scripts Principales](#-scripts-principales)
- [🖥️ Aplicación Streamlit](#-aplicación-streamlit)
- [🚀 Cómo Ejecutar](#-cómo-ejecutar)
- [🔭 Siguientes Pasos](#-siguientes-pasos)

---

## 📓 Notebooks

Los notebooks permiten explorar, probar y justificar el enfoque antes de desplegarlo como aplicación. Funcionan como guía conceptual.

### `notebooks/deteccion_anomalias_explicado.ipynb`

Contiene:

- Simulación y carga de eventos de red  
- Extracción de características (*features*)  
- Comparación de modelos:
  - Isolation Forest ✅
  - Local Outlier Factor
  - One-Class SVM  
- Métodos de evaluación: TP, FP, score  
- Simulación de correlación con reglas Sigma  
- Justificación del modelo final elegido  

> Este notebook **no se usa en producción**, pero **es clave para entender todo el diseño**.

---

## 📁 Estructura del Proyecto

```bash
cybersec-mlops-pipeline/
├── backend/                  # (Vacío) Backend opcional para FastAPI
├── data/                     # Datos de entrada y salida
│   ├── normalized/          # Dataset procesado en Parquet
│   │   └── zeek.parquet
│   └── alerts_ml.csv        # Alertas generadas por ML
├── docs/                     # Documentación interna del proyecto
│   ├── 01_objetivos.md
│   ├── 02_metricas.md
│   ├── 03_estructura.md
│   ├── 04_scripts.md
│   └── 05_tests.md
├── frontend/                 # Interfaz web en Streamlit
│   └── streamlit_app.py
├── infra/                    # (Vacío) Infraestructura para K8s, Helm, CI/CD
├── ml/                       # Lógica de entrenamiento y scoring
│   ├── anomaly_detector.py
│   └── features.py
├── models/                   # Modelos entrenados
│   └── iforest.joblib
├── notebooks/                # Notebooks de análisis
│   └── deteccion_anomalias_explicado.ipynb
├── rules/                    # Reglas Sigma simuladas
│   └── sigma_emulator.py
├── scripts/                  # Scripts ejecutables del pipeline
│   ├── generate_test_parquet.py
│   ├── run_iforest.py
│   ├── run_pipeline.py
│   ├── score_events.py
│   └── train_iforest.py
├── tests/                    # Tests unitarios
│   └── test_pipeline.py
├── Dockerfile                # Definición de imagen Docker
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

---

## 🧠 Scripts Principales

| Script                        | Descripción                                                         |
|------------------------------|---------------------------------------------------------------------|
| `scripts/train_iforest.py`   | Entrena y guarda el modelo Isolation Forest (`iforest.joblib`)      |
| `scripts/score_events.py`    | Puntúa eventos usando el modelo entrenado (`ml_score`)              |
| `scripts/run_iforest.py`     | Filtra outliers y genera alertas ML (`alerts_ml.csv`)               |
| `scripts/run_pipeline.py`    | Ejecuta toda la cadena (entrena → puntúa → alerta)                  |
| `scripts/generate_test_parquet.py` | Genera datos de prueba simulados en formato Parquet           |
| `rules/sigma_emulator.py`    | Simula reglas Sigma sobre eventos para correlación básica          |

---

## 🖥️ Aplicación Streamlit: Visualización de Anomalías

### 📌 Decisión de modelo desplegado

En producción se utiliza exclusivamente el modelo **Isolation Forest**, por su:

- Rendimiento general equilibrado
- Interpretación sencilla
- Integración directa en la app

Los otros modelos (`LOF` y `OCSVM`) se pueden evaluar en la pestaña “Evaluación” de la app pero **no** se despliegan como modelo productivo.

---

### 📊 Qué muestra la aplicación

- **Anomalías ML** — Alertas generadas por Isolation Forest.
- **Evaluación** — Comparación de distribución de score y comportamiento de distintos modelos.

---

## 🚀 Cómo Ejecutar

### ♻️ Ejecutar el pipeline completo

```bash
python3 scripts/run_pipeline.py
```

- Entrena Isolation Forest
- Puntúa eventos
- Genera alertas si corresponde
- Resultados en `data/alerts_ml.csv`

---

### 🐿️ Lanzar la app con Docker

```bash
docker build -t soc-copilot-app .
docker run -p 8501:8501 -v $(pwd)/data:/app/data soc-copilot-app
```

Accede a la app desde:

```
http://localhost:8501
```

---

## 🔭 Siguientes Pasos

- [ ] Integrar correlación Sigma + ML en la app
- [ ] Backend REST con FastAPI (opcional)
- [ ] Despliegue como microservicio en Kubernetes (infra/)
- [ ] Automatización con Helm y GitHub Actions
- [ ] Dashboards con Prometheus + Grafana
- [ ] Documentación académica (APA)

---
