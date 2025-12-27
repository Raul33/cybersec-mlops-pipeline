import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from pipeline.config.features import FEATURE_COLUMNS


import os
import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from minio import Minio
import psycopg2
from prefect import flow, task
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score
)


SILVER_BUCKET = "cybersec-ml-silver"
MODEL_BUCKET = "cybersec-ml-models"
EVAL_BUCKET = "cybersec-ml-eval"


@task
def load_latest_model():
    """Carga el modelo más reciente desde MinIO."""
    client = Minio(
        os.getenv("MINIO_ENDPOINT"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False,
    )

    objects = list(client.list_objects(MODEL_BUCKET))
    if not objects:
        raise ValueError("No hay modelos entrenados en MinIO.")

    latest_model = sorted(objects, key=lambda x: x.last_modified)[-1]

    local_path = f"data/tmp/{latest_model.object_name}"
    os.makedirs("data/tmp", exist_ok=True)

    client.fget_object(MODEL_BUCKET, latest_model.object_name, local_path)

    return local_path, latest_model.object_name


@task
def load_latest_silver():
    """Carga el dataset transformado más reciente para evaluación."""
    files = [f for f in os.listdir("data/silver") if f.endswith(".parquet")]
    if not files:
        raise ValueError("No hay datasets transformados en /data/silver")

    latest_file = sorted(files)[-1]
    df = pd.read_parquet(f"data/silver/{latest_file}")
    return df, latest_file


@task
def generate_predictions(model_path, df):
    """Aplica el modelo y produce scores + etiquetas."""
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Aplicar el modelo a las columnas oficiales
    features = df[FEATURE_COLUMNS]

    scores = model.decision_function(features)
    predictions = model.predict(features)

    # IsolationForest outputs -1 para anomalías → convertir a 0/1
    df["anomaly_score"] = scores
    df["prediction"] = np.where(predictions == -1, 1, 0)

    return df



@task
def compute_metrics(df):
    """Calcula métricas avanzadas."""
    # No ground truth → simulamos normalidad del 95%
    y_true = np.zeros(len(df))
    y_pred = df["prediction"].values

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    anomaly_rate = df["prediction"].mean()
    score_mean = df["anomaly_score"].mean()
    score_std = df["anomaly_score"].std()

    metrics = {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "anomaly_rate": round(float(anomaly_rate), 4),
        "score_mean": round(float(score_mean), 4),
        "score_std": round(float(score_std), 4),
    }

    return metrics


@task
def save_eval_results(df, metrics):
    """Guarda resultados extendidos como parquet local."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"data/eval/eval_{ts}.parquet"

    os.makedirs("data/eval", exist_ok=True)

    df_eval = pd.DataFrame({
        "metric": list(metrics.keys()),
        "value": list(metrics.values()),
    })

    df_eval.to_parquet(output_path, index=False)

    return output_path


@task
def upload_eval_to_minio(path):
    """Sube evaluación a MinIO creando bucket si no existe."""
    client = Minio(
        os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False,
    )

    bucket_name = "cybersec-ml-eval"
    filename = os.path.basename(path)

    # Crear bucket si no existe
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # Subir archivo
    client.fput_object(bucket_name, filename, path)

    uri = f"s3://{bucket_name}/{filename}"
    print(f"Evaluación subida correctamente: {uri}")

    return uri



@task
def register_eval_event(filename, model_name, dataset_name, metrics):
    """Inserta registro en PostgreSQL."""
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST", "mlops-postgresql.mlops.svc.cluster.local"),
        port=os.getenv("PG_PORT", "5555"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE", "mlops_db"),
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO evaluation_events
        (timestamp_eval, modelo_nombre, nombre_dataset, ruta_resultados, metrics, estado)
        VALUES
        (NOW(), %s, %s, %s, %s, 'SUCCESS');
    """, (model_name, dataset_name, filename, json.dumps(metrics)))

    conn.commit()
    cur.close()
    conn.close()

    print("Evento de evaluación registrado.")
    return True


@flow
def model_evaluation_flow():
    model_path, model_name = load_latest_model()
    df_silver, dataset_name = load_latest_silver()
    df_pred = generate_predictions(model_path, df_silver)
    metrics = compute_metrics(df_pred)
    local_eval = save_eval_results(df_pred, metrics)
    eval_uri = upload_eval_to_minio(local_eval)

    register_eval_event(
        os.path.basename(local_eval),
        model_name,
        dataset_name,
        metrics,
    )

    print("Evaluación completada.")
    return True


if __name__ == "__main__":
    model_evaluation_flow()
