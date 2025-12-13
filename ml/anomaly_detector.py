# ml/anomaly_detector.py

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from ml.features import extract_features as build_event_features

DEFAULT_MODEL_PATH = "models/iforest.joblib"

def train_iforest(events: pd.DataFrame, contamination: float = 0.03, random_state: int = 42):
    """
    Entrena IsolationForest sobre features de eventos normalizados.
    Devuelve (modelo entrenado, lista de nombres de columnas utilizadas como features).
    """
    X = build_event_features(events)
    if X.empty:
        raise ValueError("No hay features para entrenar.")
    model = IsolationForest(
        n_estimators=200,
        max_samples="auto",
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1
    )
    model.fit(X)
    return model, list(X.columns)

def score_iforest(events: pd.DataFrame, model, feature_cols):
    """
    Puntúa eventos y devuelve un DataFrame con las columnas más relevantes y el score ML.
    """
    X = build_event_features(events)
    for c in feature_cols:
        if c not in X.columns:
            X[c] = 0.0  # columna faltante → cero
    X = X[feature_cols]

    # IsolationForest: valores positivos → normal, negativos → anómalos
    dec = model.decision_function(X)
    ml_score = (dec.max() - dec) / (dec.max() - dec.min() + 1e-9)
    is_outlier = model.predict(X) == -1

    out = events[["timestamp", "user", "host", "src_ip", "dest_ip", "action"]].copy()
    out["ml_score"] = ml_score
    out["ml_is_outlier"] = is_outlier.astype(int)
    return out

def save_model(model, feature_cols, path: str = DEFAULT_MODEL_PATH):
    joblib.dump({"model": model, "feature_cols": feature_cols}, path)

def load_model(path: str = DEFAULT_MODEL_PATH):
    data = joblib.load(path)
    return data["model"], data["feature_cols"]
