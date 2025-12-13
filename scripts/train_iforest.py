# scripts/train_iforest.py

import pathlib
import sys
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from ml.anomaly_detector import train_iforest, save_model

def main():
    input_path = "data/normalized/zeek.parquet"
    output_path = "models/iforest.joblib"

    df = pd.read_parquet(input_path)
    model, feature_cols = train_iforest(df, contamination=0.05, random_state=42)
    save_model(model, feature_cols, output_path)
    print(f"✅ Modelo Isolation Forest guardado en: {output_path}")

if __name__ == "__main__":
    main()
