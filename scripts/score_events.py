# scripts/score_events.py

import pathlib
import sys
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from ml.anomaly_detector import load_model, score_iforest

def main():
    input_path = "data/normalized/zeek.parquet"
    model_path = "models/iforest.joblib"
    output_path = "data/alerts_ml.csv"

    df = pd.read_parquet(input_path)
    model, feature_cols = load_model(model_path)
    scored_df = score_iforest(df, model, feature_cols)
    scored_df.to_csv(output_path, index=False)
    print(f"✅ Puntuación completada. Archivo guardado en: {output_path}")

if __name__ == "__main__":
    main()
