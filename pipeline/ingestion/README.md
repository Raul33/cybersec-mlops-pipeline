# Ingesta de Datos – Pipeline Batch Diaria

Este módulo implementa el flujo de ingesta de datos sintéticos para el proyecto de detección de anomalías en eventos de red. La ingesta se ejecuta mediante **Prefect** y actúa como primera fase dentro del pipeline MLOps del sistema.

---

## 🧱 Estado actual del módulo

✓ Entorno virtual Python 3.11 creado
✓ Dependencias reproducibles en `requirements.txt`
✓ Prefect funcionando correctamente
✓ Flow base ejecutable en local
✓ Trazabilidad desde logs Prefect
✔️ Generación sintética de eventos de red  
✔️ Validación de esquema y contenido  
✔️ Serialización en formato Parquet  
✔️ Almacenamiento en MinIO (RAW layer)  
✔️ Registro de metadatos en PostgreSQL  
✔️ Orquestación completa mediante Prefect  
✔️ Ejecución automática en Kubernetes (Job)


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

> El resto de dependencias (pandas, numpy, minio, psycopg2-binary) se gestionan a nivel de imagen Docker y no se listan aquí para evitar duplicidades.

---


## 🔁 Flujo de ingesta de datos (data_ingestion_flow)

El flujo de ingesta se implementa mediante **Prefect** y está diseñado para ejecutar una **ingesta batch diaria** de eventos de red sintéticos, garantizando calidad de datos, trazabilidad y versionado.

El flujo completo está definido en el archivo:

```bash
pipeline/ingestion/data_ingestion_flow.py
```

---


### 📌 Objetivos del flujo

- Simular eventos de red realistas
- Validar la calidad de los datos generados
- Persistir los datos en formato Parquet (capa RAW)
- Almacenar los datos en MinIO (object storage)
- Registrar metadatos de la ingesta en PostgreSQL
- Proporcionar trazabilidad completa del proceso

---

### 🧠 Descripción de tasks

#### 1️⃣ `generate_synthetic_events`

Genera un conjunto de eventos de red sintéticos representados como un `DataFrame` de pandas.

**Campos generados:**
- `timestamp`
- `src_ip`
- `dst_ip`
- `bytes`
- `duration`
- `protocol`

Este enfoque evita dependencias de datos reales, facilita la reproducibilidad y es adecuado para entornos académicos y de pruebas.

---

#### 2️⃣ `validate_data`

Aplica validaciones básicas de calidad de datos:

- Verifica que el DataFrame no esté vacío
- Comprueba la existencia de las columnas esperadas
- Detecta valores nulos

Este task actúa como un **data quality gate** que previene la propagación de datos corruptos al resto del pipeline.

---

#### 3️⃣ `save_parquet`

Guarda los eventos generados en formato **Parquet**, utilizando un nombre versionado con timestamp UTC.

**Ruta de salida:**

```bash
data/ingested/network_events_<timestamp>.parquet
```


El formato Parquet permite:
- Almacenamiento eficiente
- Lectura columnar
- Integración con herramientas analíticas y de ML

---

#### 4️⃣ `upload_to_minio`

Sube el archivo Parquet generado al bucket **RAW** en MinIO.

- Las credenciales se gestionan mediante variables de entorno
- Se devuelve la URI del objeto almacenado (`s3://bucket/archivo`)
- Compatible con ejecución local y en Kubernetes

Este paso desacopla el almacenamiento de datos del sistema de archivos local.

---

#### 5️⃣ `register_ingestion_event`

Registra metadatos de la ingesta en una base de datos PostgreSQL:

- Timestamp de ingesta
- Nombre del archivo
- Ruta en MinIO
- Número de registros procesados
- Estado del proceso

Este registro proporciona **trazabilidad, auditoría y observabilidad** del pipeline MLOps.

---

#### 6️⃣ `print_dataframe`

Task auxiliar utilizada para mostrar una vista previa de los datos en los logs de ejecución.  
Es útil para depuración y validación visual durante el desarrollo.

---

### 🔗 Orquestación del flow

El flow `data_ingestion_flow` coordina la ejecución secuencial de los tasks, gestionando las dependencias entre ellos y devolviendo:

- Ruta local del archivo generado
- URI del objeto almacenado en MinIO

Este flow actúa como **primer bloque funcional** del pipeline MLOps completo.


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

```bash
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

> Nota: En producción, este flow se ejecuta automáticamente como un Job de Kubernetes dentro del clúster.

---

## 📌 Evolución del módulo

El módulo ha evolucionado desde una ingesta local básica hasta una ingesta batch completamente automatizada, integrada en un pipeline MLOps ejecutado en Kubernetes.

Actualmente, la ingesta constituye la capa RAW del sistema y sirve como punto de entrada para las fases de transformación, entrenamiento y evaluación de modelos.


---


## 🧪 Generación sintética

Se añadió el task `generate_synthetic_events` para producir un DataFrame sintético con 10 eventos de red. Este paso valida la capacidad del pipeline para:

- procesar datos estructurados en forma tabular
- generar contenido reproducible
- orquestar ejecución mediante Prefect
- devolver estructuras complejas entre tasks

Este es el primer bloque funcional real del pipeline y servirá como base para:

- validación de datos
- serialización parquet
- almacenamiento en MinIO
- registro de metadatos

---

## 🔗 Integración en el pipeline MLOps

Este flow se ejecuta como subflow dentro del pipeline completo definido en:

pipeline/full_mlops_flow.py

Su correcta ejecución es un prerrequisito para las siguientes fases:

- Transformación de datos (Silver layer)
- Entrenamiento del modelo
- Evaluación del rendimiento
- Registro de artefactos

De esta forma, la ingesta garantiza que todo el pipeline trabaje sobre datos validados, versionados y trazables.


