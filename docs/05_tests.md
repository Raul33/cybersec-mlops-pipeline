# 05 — Tests y validación del sistema

## 📌 Introducción

Este documento describe el enfoque seguido para la **validación y pruebas** del proyecto `cybersec-mlops-pipeline`.

Dado el carácter **exploratorio, no supervisado y orientado a pipeline MLOps** del sistema, la estrategia de testing se centra en:

- validación funcional de los flujos
- comprobación de integraciones entre componentes
- verificación de la correcta ejecución end-to-end

más que en tests unitarios exhaustivos de bajo nivel.

---

## 🎯 Objetivo de la estrategia de testing

Los objetivos principales de las pruebas en este proyecto son:

- asegurar que el pipeline completo se ejecuta sin errores
- verificar que cada fase produce los artefactos esperados
- validar la correcta comunicación entre servicios (Prefect, MinIO, PostgreSQL)
- garantizar la reproducibilidad del flujo

📌 En proyectos MLOps reales, el **testing de pipelines** tiene un enfoque diferente al testing clásico de software.

---

## 🧠 Enfoque adoptado

La estrategia de validación se basa en tres pilares:

### 1️⃣ Validación funcional de flows Prefect

Cada módulo del pipeline (`ingestion`, `transformation`, `training`, `evaluation`) se ha probado de forma independiente verificando que:

- el flow se ejecuta correctamente
- no se producen errores de dependencia
- los artefactos se generan y almacenan correctamente

Esto se ha realizado mediante:
- ejecución manual de cada flow
- inspección de logs
- verificación de resultados en MinIO y PostgreSQL

---

### 2️⃣ Validación end-to-end del pipeline completo

El archivo:

```text
pipeline/full_mlops_flow.py
```

actúa como **test de integración principal**, ya que ejecuta el pipeline completo en orden:

1. ingesta

2. transformación

3. entrenamiento

4. evaluación

Si este flow finaliza correctamente, se considera que el sistema es funcional.

### 3️⃣ Tests automatizados mínimos

El proyecto incluye un test automatizado básico en:

```text
tests/test_pipeline.py
```

Este test verifica:

- que los módulos del pipeline pueden importarse correctamente

- que la estructura general del proyecto es válida

- que no existen errores sintácticos o dependencias rotas

📌 Este tipo de test es habitual en proyectos MLOps como smoke test inicial.


El archivo `tests/test_pipeline.py` valida el funcionamiento de las funciones principales del pipeline: extracción de características, entrenamiento del modelo y puntuación de eventos.

### 📄 `tests/test_pipeline.py`

```python
import pandas as pd
import pytest
from pathlib import Path

from ml.features import extract_features
from ml.anomaly_detector import train_iforest, score_iforest

# Ruta de test del parquet generado previamente
data_path = Path("data/normalized/zeek.parquet")

@pytest.mark.parametrize("path", [data_path])
def test_extract_features(path):
    df = pd.read_parquet(path)
    features = extract_features(df)
    assert not features.empty, "Las features no deberían estar vacías"
    assert isinstance(features, pd.DataFrame), "Debe retornar un DataFrame"

def test_train_and_score():
    df = pd.read_parquet(data_path)
    model, feature_cols = train_iforest(df, contamination=0.05)
    result = score_iforest(df, model, feature_cols)

    assert "ml_score" in result.columns, "Debe contener la columna 'ml_score'"
    assert "ml_is_outlier" in result.columns, "Debe contener la columna 'ml_is_outlier'"
    assert set(result["ml_is_outlier"].unique()).issubset({0, 1}), "Valores válidos: 0 o 1"
    assert result["ml_score"].between(0, 1).all(), "Todos los scores deben estar entre 0 y 1"

```

----

## ⚠️ Por qué no hay tests unitarios exhaustivos

No se han incluido tests unitarios detallados para cada función por las siguientes razones:

- el sistema trabaja con datos no supervisados

- no existe un ground truth real para validar salidas

- gran parte de la lógica depende de servicios externos (MinIO, PostgreSQL)

- el valor principal está en el flujo completo, no en funciones aisladas

En este contexto, los tests unitarios clásicos aportarían poco valor práctico.

---

## 🧪 Validaciones manuales realizadas

Durante el desarrollo se han realizado validaciones manuales como:

- comprobación de buckets MinIO y artefactos generados

- inspección de tablas de auditoría en PostgreSQL

- revisión de logs de Prefect

- verificación visual de resultados en la aplicación Streamlit

Estas validaciones forman parte del **proceso real de desarrollo MLOps**.

---

## 🚀 Trabajo futuro en testing

Como posibles extensiones del sistema se plantean:

- tests de calidad de datos (data validation)

- tests de drift del modelo

- validación automática de esquemas

- tests de rendimiento del pipeline

- integración con herramientas como Great Expectations

Estas mejoras se consideran fuera del alcance actual del proyecto.

---

## 🧠 Conclusión

La estrategia de testing adoptada es coherente con:

- la naturaleza del problema (detección de anomalías)

- el enfoque MLOps del proyecto

- el uso de Kubernetes y pipelines batch

El sistema prioriza la robustez del flujo completo frente a pruebas unitarias tradicionales, alineándose con prácticas reales de MLOps en entornos productivos.
