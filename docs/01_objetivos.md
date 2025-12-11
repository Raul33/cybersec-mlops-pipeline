# Objetivos del proyecto

## Objetivo general

Implementar una aplicación de detección de anomalías con aprendizaje automático, explicable y reproducible, centrada en demostrar el ciclo de vida completo de un modelo de ML mediante una arquitectura MLOps on-premises, desacoplada de proveedores cloud, utilizando herramientas 100 % open-source sobre Kubernetes.

## Objetivos específicos

1. Diseñar una arquitectura MLOps local y modular que permita entrenar, versionar, servir y monitorizar modelos de ML de forma reproducible.
2. Implementar un pipeline de entrenamiento y scoring para modelos de detección de anomalías no supervisados (Isolation Forest, LOF, One-Class SVM).
3. Desarrollar una API REST (FastAPI) para el consumo de modelos, ingestión de datos y correlación de eventos.
4. Construir una interfaz de usuario (Streamlit) para la visualización interactiva de alertas Sigma, anomalías y métricas de evaluación.
5. Integrar herramientas OSS como MLflow, MinIO, Airflow, Seldon Core/KServe, Harbor y Keycloak en un entorno Kubernetes local usando Helm.
6. Garantizar la seguridad básica del sistema mediante control de accesos centralizado y almacenamiento seguro de credenciales.
7. Validar la trazabilidad del modelo (tracking de experimentos, firma de artefactos, control de versiones y logs).
8. Documentar el ciclo de vida completo del modelo desde la ingesta hasta el despliegue y evaluación, enfatizando la claridad y explicabilidad del sistema.