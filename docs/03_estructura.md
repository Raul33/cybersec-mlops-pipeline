# 03 – Estructura del proyecto y arquitectura

Este documento describe la estructura del proyecto **cybersec-mlops-pipeline**, el propósito de cada componente y cómo encajan entre sí.

El objetivo es que cualquier lector (técnico o no) pueda entender:
- Qué hace cada archivo
- Qué entradas recibe
- Qué salidas genera
- Cómo se relaciona con el notebook de introducción

---

## 1. Visión general de la arquitectura

El proyecto se divide en cuatro grandes bloques:

1. **Datos (`data/`)**
2. **Modelo de Machine Learning (`ml/`)**
3. **Aplicación de visualización (`frontend/`)**
4. **Ejecución y automatización (`scripts/`)**

La lógica sigue el mismo flujo que el notebook:


---

## 2. Relación con el notebook

El notebook incluido en el proyecto cumple una función **didáctica**:

- Explica qué es la detección de anomalías
- Justifica el uso de Isolation Forest
- Muestra métricas y visualizaciones exploratorias
- Simula correlación con reglas tipo Sigma

La **aplicación** es la **traducción operativa** de ese notebook:
- Menos modelos
- Menos teoría
- Más foco en ejecución, reproducibilidad y despliegue

---

## 3. Estructura de carpetas

```text
cybersec-mlops-pipeline/
├── data/
├── docs/
├── frontend/
├── ml/
├── models/
├── scripts/
├── requirements.txt
└── Dockerfile
