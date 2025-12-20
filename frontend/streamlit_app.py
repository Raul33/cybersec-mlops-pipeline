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
alerts_path = Path("data/alerts_ml.csv")
if not alerts_path.exists():
    st.error("Archivo data/alerts_ml.csv no encontrado. Ejecuta el modelo primero.")
    st.stop()

df = pd.read_csv(alerts_path, parse_dates=["timestamp"])
df["ml_score"] = df["ml_score"].clip(0, 1)

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
