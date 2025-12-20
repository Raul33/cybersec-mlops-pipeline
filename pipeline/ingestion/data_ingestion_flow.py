from prefect import flow, task
import pandas as pd
from datetime import datetime
import numpy as np

@task
def generate_synthetic_events():
    # 10 filas de ejemplo
    data = {
        "timestamp": [datetime.utcnow() for _ in range(10)],
        "src_ip": [f"192.168.1.{i}" for i in range(10)],
        "dst_ip": [f"10.0.0.{i}" for i in range(10)],
        "bytes": np.random.randint(100, 2000, size=10),
        "duration": np.random.uniform(0.1, 3.5, size=10),
        "protocol": np.random.choice(["TCP", "UDP"], size=10),
    }

    df = pd.DataFrame(data)
    return df

@task
def validate_data(df):
    # Check empty
    if df.empty:
        raise ValueError("El DataFrame está vacío")

    # Expected columns
    expected_cols = {"timestamp", "src_ip", "dst_ip", "bytes", "duration", "protocol"}
    missing_cols = expected_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Columnas faltantes: {missing_cols}")

    # Null check
    if df.isnull().any().any():
        raise ValueError("Se detectaron valores nulos en el DataFrame")

    return True

@task
def save_parquet(df):
    from datetime import datetime
    import os
    
    # Generate timestamped filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"network_events_{timestamp}.parquet"
    filepath = os.path.join("data", "ingested", filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Write parquet
    df.to_parquet(filepath, index=False)

    print(f"Archivo parquet creado: {filepath}")
    return filepath

@task
def upload_to_minio(filepath: str):
    import os
    from minio import Minio
    from minio.error import S3Error

    endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key = os.getenv("MINIO_ACCESS_KEY")
    secret_key = os.getenv("MINIO_SECRET_KEY")

    if not access_key or not secret_key:
        raise ValueError("MINIO_ACCESS_KEY o MINIO_SECRET_KEY no están configuradas.")

    client = Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=False  # importante usando port-forward
    )

    bucket_name = "cybersec-ml-raw"
    filename = os.path.basename(filepath)

    client.fput_object(
        bucket_name,
        filename,
        filepath,
    )

    print(f"Archivo subido a MinIO: s3://{bucket_name}/{filename}")
    return f"s3://{bucket_name}/{filename}"




@task
def print_dataframe(df):
    print(df.head())
    return True

@flow(name="data_ingestion_flow")
def data_ingestion_flow():
    df = generate_synthetic_events()
    validate_data(df)
    filepath = save_parquet(df)
    minio_uri = upload_to_minio(filepath)
    print_dataframe(df)
    return filepath, minio_uri




if __name__ == "__main__":
    data_ingestion_flow()

