# ml/features.py

import pandas as pd

def extract_features(events: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae características numéricas simples a partir de los eventos.
    """
    df = events.copy()

    # Codificación de acción como valor numérico
    df["action_code"] = df["action"].astype("category").cat.codes

    # Timestamp a hora del día (como número de 0 a 1)
    df["hour"] = df["timestamp"].dt.hour / 24.0
    df["minute"] = df["timestamp"].dt.minute / 60.0

    # Cuantificación de frecuencia por IP origen y destino
    df["src_freq"] = df.groupby("src_ip")["src_ip"].transform("count")
    df["dest_freq"] = df.groupby("dest_ip")["dest_ip"].transform("count")

    # Reemplaza NaNs por 0 y selecciona las columnas finales
    features = df[["action_code", "hour", "minute", "src_freq", "dest_freq"]].fillna(0.0)
    return features