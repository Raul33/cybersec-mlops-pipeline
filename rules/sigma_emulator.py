# rules/sigma_emulator.py
import pandas as pd

def emulate_sigma_rules(events: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica reglas Sigma simuladas sobre eventos y devuelve las coincidencias
    con columnas: timestamp, user, host, src_ip, dest_ip, rule_id, title, severity, summary, risk
    """
    alerts = []

    for _, row in events.iterrows():
        # Regla 1: acción "exec" es sospechosa
        if row.get("action") == "exec":
            alerts.append({
                "timestamp": row["timestamp"],
                "user": row["user"],
                "host": row["host"],
                "src_ip": row["src_ip"],
                "dest_ip": row["dest_ip"],
                "rule_id": "SIGMA-001",
                "title": "Ejecución sospechosa detectada",
                "severity": "medium",
                "summary": f"Acción sospechosa: {row['action']}",
                "risk": 0.6
            })

        # Regla 2: acceso root desde IP interna rara
        if row.get("user") == "root" and row.get("src_ip", "").startswith("10."):
            alerts.append({
                "timestamp": row["timestamp"],
                "user": row["user"],
                "host": row["host"],
                "src_ip": row["src_ip"],
                "dest_ip": row["dest_ip"],
                "rule_id": "SIGMA-002",
                "title": "Acceso root desde red interna",
                "severity": "high",
                "summary": f"Acceso root desde IP interna: {row['src_ip']}",
                "risk": 0.8
            })

    return pd.DataFrame(alerts)