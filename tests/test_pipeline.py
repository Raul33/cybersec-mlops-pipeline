# tests/test_pipeline.py
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
