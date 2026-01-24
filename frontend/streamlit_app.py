# frontend/streamlit_app.py
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="SOC Copilot", layout="wide")
st.title("🛡️ SOC Copilot")

st.sidebar.header("Parámetros")
threshold = st.sidebar.slider("Umbral de alerta ML", 0.0, 1.0, 0.8, 0.01)

# Cargar alertas ML desde CSV
from minio import Minio
import os
import pickle

# -----------------------
# 1️⃣ Inicializar cliente MinIO
# -----------------------
# --- MinIO config (portable) ---
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "mlops-minio.mlops.svc.cluster.local:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"

MODELS_BUCKET = os.getenv("MODELS_BUCKET", "cybersec-ml-models")
EVAL_BUCKET   = os.getenv("EVAL_BUCKET", "cybersec-ml-eval")

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE,
)


# -----------------------
# 2️⃣ Obtener lista de modelos y seleccionar el más reciente
# -----------------------
objects = client.list_objects(MODELS_BUCKET, recursive=False)
models = sorted(objects, key=lambda x: x.last_modified, reverse=True)

if not models:
    st.error(f"❌ No hay modelos disponibles en MinIO (bucket: {MODELS_BUCKET})")
    st.stop()

latest_model_obj = models[0]
latest_model_name = latest_model_obj.object_name

st.sidebar.write("📌 Último modelo detectado:")
st.sidebar.code(latest_model_name)

# -----------------------
# 3️⃣ Descargar modelo al contenedor
# -----------------------
local_model_path = f"/tmp/{latest_model_name}"
client.fget_object(MODELS_BUCKET, latest_model_name, local_model_path)

with open(local_model_path, "rb") as f:
    model = pickle.load(f)

# -----------------------
# 4️⃣ Descargar el parquet de evaluación más reciente (métricas)
# -----------------------
import tempfile

eval_objects = client.list_objects(EVAL_BUCKET, recursive=False)
evals = sorted(eval_objects, key=lambda x: x.last_modified, reverse=True)

if not evals:
    st.error(f"❌ No hay resultados de evaluación disponibles (bucket: {EVAL_BUCKET})")
    st.stop()

latest_eval = evals[0].object_name
st.sidebar.write("📌 Última evaluación detectada:")
st.sidebar.code(latest_eval)

tmp_parquet = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
client.fget_object(EVAL_BUCKET, latest_eval, tmp_parquet.name)

df = pd.read_parquet(tmp_parquet.name)

# -----------------------
# 5️⃣ Mostrar métricas (lo que realmente contiene el parquet)
# -----------------------
st.subheader("📈 Métricas de evaluación (ML)")
st.metric("Total métricas", len(df))

# Validación defensiva: el parquet debería tener ['metric','value']
expected_cols = {"metric", "value"}
if not expected_cols.issubset(set(df.columns)):
    st.error(f"❌ Formato inesperado en evaluación. Columnas: {list(df.columns)}")
    st.stop()

st.dataframe(df, use_container_width=True, height=250)

# Gráfico de barras (métricas)
st.markdown("## 📊 Métricas (bar chart)")
fig, ax = plt.subplots(figsize=(5, 2.2))
ax.bar(df["metric"], df["value"])
ax.set_ylim(0, 1)
ax.set_title("Métricas de evaluación", fontsize=10)

ax.tick_params(axis="x", labelrotation=30, labelsize=8)
ax.tick_params(axis="y", labelsize=8)

plt.tight_layout()
st.pyplot(fig, use_container_width=False)

