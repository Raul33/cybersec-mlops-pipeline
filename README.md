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


## 📂 Estructura del Proyecto

cybersec-mlops-pipeline/
├── data/               # Datos de entrada y salida del sistema
│   └── normalized/     # Dataset de eventos procesado (formato Parquet)
│   └── alerts_ml.csv   # Alertas generadas por el modelo ML
├── docs/               # Documentación técnica y de arquitectura
├── frontend/           # Aplicación de visualización con Streamlit
├── ml/                 # Lógica de entrenamiento y scoring del modelo ML
├── models/             # Modelo entrenado (Isolation Forest .joblib)
├── notebooks/          # Notebook explicativo del sistema
├── scripts/            # Scripts de ejecución y automatización
├── Dockerfile          # Definición de imagen Docker
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación principal del repositorio

