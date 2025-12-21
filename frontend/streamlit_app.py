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
client = Minio(
    os.getenv("MINIO_ENDPOINT", "minio.mlops.svc.cluster.local:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False,
)


bucket_name = "cybersec-ml-models"

# -----------------------
# 2️⃣ Obtener lista de objetos y seleccionar el más reciente
# -----------------------
objects = client.list_objects(bucket_name, recursive=False)
models = sorted(objects, key=lambda x: x.last_modified, reverse=True)

if not models:
    st.error("❌ No hay modelos disponibles en MinIO")
    st.stop()

latest_model_obj = models[0]
latest_model_name = latest_model_obj.object_name

st.sidebar.write(f"📌 Último modelo detectado:")
st.sidebar.code(latest_model_name)

# -----------------------
# 3️⃣ Descargar modelo al contenedor
# -----------------------
local_model_path = f"/tmp/{latest_model_name}"
client.fget_object(bucket_name, latest_model_name, local_model_path)

with open(local_model_path, "rb") as f:
    model = pickle.load(f)


import tempfile

alerts_bucket = "cybersec-ml-eval"

# Descargar el archivo de evaluación más reciente
eval_objects = client.list_objects(alerts_bucket, recursive=False)
evals = sorted(eval_objects, key=lambda x: x.last_modified, reverse=True)

if not evals:
    st.error("❌ No hay resultados de evaluación disponibles")
    st.stop()

latest_eval = evals[0].object_name

# Guardar temporalmente
tmp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet")
client.fget_object(alerts_bucket, latest_eval, tmp_csv.name)

# Leer parquet
df = pd.read_parquet(tmp_csv.name)


st.subheader("🔍 Alertas de Anomalías (ML)")
st.metric("Total alertas", len(df))
st.dataframe(df[df["ml_score"] >= threshold], use_container_width=True, height=400)

# Histograma
st.markdown("## 📊 Distribución de scores ML")

col1, col2, col3 = st.columns([1,3,1])

with col2:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(df["ml_score"], bins=20)
    ax.set_title("Distribución de scores ML")
    st.pyplot(fig)
