# scripts/generate_test_parquet.py

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pathlib

# ==== Parámetros ====
N_EVENTS = 250
USERS = [f"user{i}" for i in range(1, 6)]
HOSTS = [f"host{i}" for i in range(1, 4)]
IPS = [f"192.168.1.{i}" for i in range(1, 20)]
ACTIONS = ["login", "file_access", "download", "upload", "scan"]
NOW = datetime.utcnow()

# ==== Generar eventos simulados ====
timestamps = [NOW - timedelta(minutes=i * 3) for i in range(N_EVENTS)]

df = pd.DataFrame({
    "timestamp": timestamps,
    "user": np.random.choice(USERS, size=N_EVENTS),
    "host": np.random.choice(HOSTS, size=N_EVENTS),
    "src_ip": np.random.choice(IPS, size=N_EVENTS),
    "dest_ip": np.random.choice(IPS, size=N_EVENTS),
    "action": np.random.choice(ACTIONS, size=N_EVENTS),
})

# ==== Guardar como Parquet ====
parquet_path = pathlib.Path("data/normalized/zeek.parquet")
parquet_path.parent.mkdir(parents=True, exist_ok=True)
df.to_parquet(parquet_path, index=False)

print(f"✔ Parquet de prueba generado en: {parquet_path}")
