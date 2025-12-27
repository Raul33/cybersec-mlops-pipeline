import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))


import os
import pickle
from datetime import datetime
from pipeline.config.features import FEATURE_COLUMNS


import pandas as pd
from minio import Minio
from sklearn.ensemble import IsolationForest
import psycopg2
from psycopg2.extras import Json

from prefect import flow, task


# ---------------------------
# 🧠 TASK: cargar parquet local
# ---------------------------
@task
def load_transformed_data():
    folder = "data/silver"
    files = os.listdir(folder)
    if not files:
        raise FileNotFoundError("No hay archivos transformados disponibles.")

    # Selecciona el parquet más reciente por timestamp del nombre
    files = sorted(files, reverse=True)
    filepath = os.path.join(folder, files[0])

    print(f"Archivo cargado para entrenamiento: {filepath}")
    df = pd.read_parquet(filepath)

    return df, filepath


# ---------------------------
# 🧠 TASK: entrenar Isolation Forest
# ---------------------------
@task
def train_isolation_forest(df):
    """
    Entrena un IsolationForest usando siempre las mismas features
    definidas en pipeline.config.features.FEATURE_COLUMNS.
    """
    from sklearn.ensemble import IsolationForest

    # Usamos SIEMPRE las columnas oficiales
    X = df[FEATURE_COLUMNS]

    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42,
    )
    model.fit(X)

    return model


# ---------------------------
# 🧠 TASK: guardar modelo local
# ---------------------------
@task
def save_model_local(model):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"model_isoforest_{timestamp}.pkl"
    filepath = os.path.join("data", "models", filename)

    os.makedirs("data/models", exist_ok=True)

    with open(filepath, "wb") as f:
        pickle.dump(model, f)

    print(f"Modelo guardado localmente: {filepath}")
    return filepath


# ---------------------------
# 🧠 TASK: subir modelo a MinIO
# ---------------------------
@task
def upload_model_to_minio(filepath):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    client = Minio(
        os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False,
    )

    bucket_name = "cybersec-ml-models"
    client.make_bucket(bucket_name) if not client.bucket_exists(bucket_name) else None

    object_name = f"model_isoforest_{timestamp}.pkl"
    client.fput_object(bucket_name, object_name, filepath)

    minio_uri = f"s3://{bucket_name}/{object_name}"
    print(f"Modelo subido a MinIO: {minio_uri}")

    return minio_uri


# ---------------------------
# 🧠 TASK: registrar evento en PostgreSQL
# ---------------------------
@task
def register_training_event(minio_uri, df, model_params):
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST", "mlops-postgresql.mlops.svc.cluster.local"),
        port=os.getenv("PG_PORT", "5555"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE", "mlops_db")
    )

    cursor = conn.cursor()

    query = """
        INSERT INTO training_events (
            timestamp_entrenamiento,
            ruta_modelo,
            num_registros,
            parametros,
            estado
        )
        VALUES (NOW(), %s, %s, %s, %s);
    """

    cursor.execute(
        query,
        (minio_uri, len(df), Json(model_params), "SUCCESS")
    )

    conn.commit()
    cursor.close()
    conn.close()

    print("Evento de entrenamiento registrado en PostgreSQL.")


# ---------------------------
# 🚀 FLOW PRINCIPAL
# ---------------------------
@flow(name="model_training_flow")
def model_training_flow():
    df, source_file = load_transformed_data()
    model = train_isolation_forest(df)
    local_path = save_model_local(model)
    minio_path = upload_model_to_minio(local_path)

    model_params = {
        "n_estimators": 100,
        "contamination": "auto",
        "random_state": 42
    }

    register_training_event(
        minio_uri=minio_path,
        df=df,
        model_params=model_params
    )

    print("Entrenamiento completado.")
    return minio_path


if __name__ == "__main__":
    model_training_flow()
