# scripts/run_iforest.py

import argparse
import sys
import pathlib
import pandas as pd

# Asegurarse de que se puede importar desde la raíz del proyecto
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from ml.anomaly_detector import load_model, score_iforest

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Parquet normalizado")
    ap.add_argument("--model", default="models/iforest.joblib")
    ap.add_argument("--output", default="data/alerts_ml.csv")
    ap.add_argument("--threshold", type=float, default=0.8, help="umbral de rareza 0..1 para crear alerta")
    args = ap.parse_args()

    # Leer eventos desde Parquet
    df = pd.read_parquet(args.input)

    # Cargar modelo y columnas usadas
    model, cols = load_model(args.model)

    # Puntuar eventos
    scored = score_iforest(df, model, cols)

    # Crear alertas ML: filtrar por umbral
    alerts = scored[(scored["ml_is_outlier"] == 1) | (scored["ml_score"] >= args.threshold)].copy()

    if alerts.empty:
        alerts = alerts.assign(
            title=[],
            rule_id=[],
            severity=[],
            summary=[],
            risk=[]
        )
    else:
        alerts["title"] = "Anomalía de comportamiento (IsolationForest)"
        alerts["rule_id"] = "ML-IFOREST"

        def sev(score):
            if score >= 0.95: return "critical"
            if score >= 0.90: return "high"
            if score >= 0.80: return "medium"
            return "low"

        alerts["severity"] = alerts["ml_score"].apply(sev)
        alerts["summary"] = alerts.apply(lambda r: f"Evento anómalo (score={r['ml_score']:.2f}) action={r['action']}", axis=1)
        alerts["risk"] = alerts["ml_score"].clip(0, 1)

    # Selección final de columnas compatibles con Sigma
    out = alerts[[
        "timestamp", "user", "host", "src_ip", "dest_ip",
        "title", "rule_id", "severity", "summary", "risk"
    ]].copy()

    pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    print(f"OK: {len(out)} alertas ML -> {args.output}")

