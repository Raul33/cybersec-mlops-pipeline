import os
import pandas as pd
from datetime import datetime
from minio import Minio
import psycopg2
from prefect import flow, task

RAW_BUCKET = "cybersec-ml-raw"
SILVER_BUCKET = "cybersec-ml-silver"


@task
def find_latest_raw():
    client = Minio(
        os.getenv("MINIO_ENDPOINT"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )

    objects = client.list_objects(RAW_BUCKET)
    parquet_files = [obj.object_name for obj in objects]

    if not parquet_files:
        raise ValueError("No hay archivos parquet en el bucket RAW.")

    latest_file = sorted(parquet_files)[-1]
    return latest_file


@task
def download_from_minio(filename):
    client = Minio(
        os.getenv("MINIO_ENDPOINT"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )

    local_path = f"data/tmp/{filename}"
    os.makedirs("data/tmp", exist_ok=True)

    client.fget_object(RAW_BUCKET, filename, local_path)
    return local_path


@task
def transform_parquet(path):
    df = pd.read_parquet(path)

    df["bytes_per_second"] = df["bytes"] / df["duration"]
    df["timestamp_hour"] = df["timestamp"].dt.hour
    df["flow_size_category"] = pd.cut(
        df["bytes"],
        bins=[0, 500, 1500, 10000],
        labels=["small", "medium", "large"]
    )

    return df


@task
def save_silver(df):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"data/silver/network_events_silver_{ts}.parquet"

    os.makedirs("data/silver", exist_ok=True)
    df.to_parquet(output_path, index=False)

    return output_path


@task
def upload_to_minio(path):
    client = Minio(
        os.getenv("MINIO_ENDPOINT"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )

    filename = os.path.basename(path)
    client.fput_object(SILVER_BUCKET, filename, path)

    return f"s3://{SILVER_BUCKET}/{filename}"


@task
def register_transformation_event(filename, silver_uri, num_rows):
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", "5555"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE", "mlops_db")
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO transformation_events 
        (timestamp_transformacion, nombre_archivo, ruta_minio, num_registros, estado)
        VALUES (NOW(), %s, %s, %s, 'SUCCESS');
    """, (filename, silver_uri, num_rows))

    conn.commit()
    cur.close()
    conn.close()

    print("Evento de transformación registrado.")
    return True


@flow
def data_transformation_flow():
    latest_raw = find_latest_raw()
    local_raw = download_from_minio(latest_raw)
    df_silver = transform_parquet(local_raw)
    local_silver = save_silver(df_silver)
    silver_uri = upload_to_minio(local_silver)

    register_transformation_event(
        os.path.basename(local_silver),
        silver_uri,
        len(df_silver)
    )

    print("Transformación completada.")
    return True


if __name__ == "__main__":
    data_transformation_flow()
