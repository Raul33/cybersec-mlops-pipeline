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
st.subheader("📊 Distribución de scores ML")
scores = df["ml_score"].to_numpy()
bins = np.linspace(0, 1, 21)
counts, bins_edges = np.histogram(scores, bins=bins)
fig = plt.figure(figsize=(4.5, 2))
st.markdown("---")
plt.bar(bins_edges[:-1], counts, width=(bins_edges[1] - bins_edges[0]), align="edge")
plt.xlabel("ml_score")
plt.ylabel("Frecuencia")
plt.title("Distribución de scores")
st.pyplot(fig)
