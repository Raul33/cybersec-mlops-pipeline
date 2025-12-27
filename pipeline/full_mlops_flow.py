import sys
from pathlib import Path

# Asegura imports desde la raíz del repo
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from prefect import flow

# Importa tus subflows existentes (no se modifica su lógica)
from pipeline.ingestion.data_ingestion_flow import data_ingestion_flow
from pipeline.transformation.data_transformation_flow import data_transformation_flow
from pipeline.training.model_training_flow import model_training_flow
from pipeline.evaluation.model_evaluation_flow import model_evaluation_flow


@flow(name="full_mlops_flow")
def full_mlops_flow():
    """
    Pipeline end-to-end:
      1) Ingesta -> RAW (MinIO) + evento en PostgreSQL
      2) Transformación -> SILVER (MinIO) + evento en PostgreSQL
      3) Entrenamiento -> MODELS (MinIO) + evento en PostgreSQL
      4) Evaluación -> EVAL (MinIO) + evento en PostgreSQL

    Reutiliza los flows existentes sin reescritura.
    """

    # 1) Ingesta (devuelve filepath local + uri en minio)
    ingestion_local_path, ingestion_minio_uri = data_ingestion_flow()
    print(f"[FULL] Ingestion OK: {ingestion_local_path} | {ingestion_minio_uri}")

    # 2) Transformación (actualmente devuelve True)
    transformation_ok = data_transformation_flow()
    print(f"[FULL] Transformation OK: {transformation_ok}")

    # 3) Entrenamiento (devuelve uri del modelo en minio)
    model_minio_uri = model_training_flow()
    print(f"[FULL] Training OK: {model_minio_uri}")

    # 4) Evaluación (actualmente devuelve True)
    evaluation_ok = model_evaluation_flow()
    print(f"[FULL] Evaluation OK: {evaluation_ok}")

    return {
        "ingestion_local_path": ingestion_local_path,
        "ingestion_minio_uri": ingestion_minio_uri,
        "transformation_ok": transformation_ok,
        "model_minio_uri": model_minio_uri,
        "evaluation_ok": evaluation_ok,
    }


if __name__ == "__main__":
    full_mlops_flow()
