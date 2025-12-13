# scripts/run_pipeline.py

import subprocess
import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MODEL_PATH = BASE_DIR / "models" / "iforest.joblib"
PARQUET_PATH = DATA_DIR / "normalized" / "zeek.parquet"
ALERTS_PATH = DATA_DIR / "alerts_ml.csv"

def run_script(script_name, *args):
    script_path = BASE_DIR / "scripts" / script_name
    cmd = ["python3", str(script_path)] + list(args)
    print(f"\n➡️ Ejecutando: {script_name}")
    subprocess.run(cmd, check=True)

def main():
    # 1. Generar dataset sintético (si no existe)
    if not PARQUET_PATH.exists():
        run_script("generate_test_parquet.py")

    # 2. Entrenar modelo Isolation Forest
    run_script("train_iforest.py")

    # 3. Puntuar eventos (no genera output)
    run_script("score_events.py")

    # 4. Generar alertas según score
    run_script("run_iforest.py", "--input", str(PARQUET_PATH), "--output", str(ALERTS_PATH))

    print("\n✅ Pipeline completado exitosamente.")
    print(f"📁 Alertas generadas en: {ALERTS_PATH}")

if __name__ == "__main__":
    main()
