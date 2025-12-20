# Ingesta de Datos – Pipeline Batch Diaria

Este módulo implementa el flujo de ingesta de datos sintéticos para el proyecto de detección de anomalías en eventos de red. La ingesta se ejecuta mediante **Prefect** y actúa como primera fase dentro del pipeline MLOps del sistema.

---

## 🧱 Estado actual del módulo

✓ Entorno virtual Python 3.11 creado
✓ Dependencias reproducibles en `requirements.txt`
✓ Prefect funcionando correctamente
✓ Flow base ejecutable en local
✓ Trazabilidad desde logs Prefect

---

## 📌 Motivación técnica

Se eligió **Python 3.11** para asegurar compatibilidad con Prefect 2.14.x. La versión 3.12 provoca errores en dependencias internas (especialmente `pendulum`), por lo que se reconstruyó el entorno virtual para garantizar:

* estabilidad
* reproducibilidad
* portabilidad
* coherencia académica

---

## 📦 Dependencias clave

```
prefect==2.14.10
griffe==0.36.5
```

Estas versiones se fijaron por motivos de compatibilidad y reproducibilidad del pipeline.

---

## 🏗 Estructura del módulo

```
pipeline/
  ingestion/
    data_ingestion_flow.py
    README.md  ← este archivo
```

---

## ▶️ Ejecución del flow local

1. Activar el entorno virtual

```
source .venv311/bin/activate
```

2. Ejecutar el flow

```
python pipeline/ingestion/data_ingestion_flow.py
```

3. Resultado esperado

```
Prefect está funcionando correctamente 🚀
```

Además, se mostrará trazabilidad Prefect en terminal, incluyendo:

* creación del flow run
* ejecución de task
* estado final

Esto confirma que la infraestructura base está operativa.

---

## 📌 Próximos pasos

☑️ Implementar generación sintética de datos
☑️ Validar esquema
☑️ Guardar en formato parquet
☑️ Subir a MinIO
☑️ Registrar metadatos

El objetivo final es construir una ingesta batch diaria automática dentro de Kubernetes.

---

## ✏️ Notas académicas

Las decisiones técnicas tomadas en esta fase podrán incluirse en el TFM como evidencia de:

* control de versión de dependencias
* decisiones de ingeniería fundamentadas
* trazabilidad del ciclo de vida del pipeline
* gestión de compatibilidad entre paquetes
