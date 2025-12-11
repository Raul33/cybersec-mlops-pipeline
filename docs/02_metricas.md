# Métricas y criterios de éxito

Este documento define las métricas técnicas y operativas que permitirán evaluar el rendimiento del sistema desarrollado, tanto a nivel de modelo de machine learning como de arquitectura MLOps.

## Métricas técnicas

### Detección de anomalías
- % de eventos clasificados como anómalos: ≤ 10%
- Score promedio por evento: variable según algoritmo
- Curva PR proxy (utilizando reglas Sigma como etiqueta): AUC ≥ 0.70

### Correlación de alertas
- % de incidentes correlados vs. total alertas: ≥ 50%
- Tiempo medio de correlación: ≤ 1 segundo

### API REST
- SLA latencia del endpoint `/ml_alerts`: ≤ 200 ms
- Disponibilidad de servicio: ≥ 99%

### Pipelines
- % de DAGs completados sin errores: 100%
- Tiempo medio de ejecución de pipeline: ≤ 5 minutos

### Sistema
- Reproducibilidad total del modelo: 100% con mismo seed
- Trazabilidad de experimentos y artefactos: 100%

### Seguridad y control
- Acceso autenticado con Keycloak: 100%
- Artefactos firmados/verificados: si aplica
