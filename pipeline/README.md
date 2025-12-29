# 🧩 Pipeline MLOps – Visión global

Este directorio contiene la implementación completa de un **pipeline MLOps end-to-end** para un sistema de detección de anomalías en eventos de red, diseñado para ejecutarse de forma **reproducible, trazable y desacoplada** sobre Kubernetes.

El pipeline automatiza todo el ciclo de vida del modelo, desde la ingesta de datos hasta la evaluación final, siguiendo principios de **ingeniería MLOps moderna**.

---

## 🎯 Objetivo del pipeline

El objetivo principal del pipeline es:

- Automatizar el procesamiento de eventos de red
- Entrenar y evaluar un modelo de detección de anomalías
- Versionar datasets y modelos
- Registrar eventos clave para auditoría y trazabilidad
- Ejecutarse de forma controlada dentro de un clúster Kubernetes

Este pipeline está pensado para **entornos de ciberseguridad**, donde la reproducibilidad y la trazabilidad son críticas.

---

## 🔄 Flujo general del pipeline

El pipeline se compone de cuatro grandes fases, orquestadas de forma secuencial:

1. **Ingesta de datos**
2. **Transformación**
3. **Entrenamiento del modelo**
4. **Evaluación**

Cada fase está implementada como un **flow independiente de Prefect**, lo que permite:

- Reutilización
- Aislamiento de responsabilidades
- Escalabilidad futura
- Observabilidad del proceso completo

---

## 🧠 Arquitectura lógica

A alto nivel, el pipeline sigue la siguiente lógica:

- **Prefect** actúa como orquestador del flujo completo
- **MinIO** se utiliza como data lake y model registry
- **PostgreSQL** almacena metadatos de ejecución
- **Kubernetes** ejecuta el pipeline como un Job desacoplado

Todo el pipeline puede ejecutarse sin dependencias locales, utilizando únicamente servicios internos del clúster.

---

## 📦 Componentes principales

El pipeline está organizado en los siguientes módulos:

```text
pipeline/
├── full_mlops_flow.py        # Orquestador principal del pipeline
├── ingestion/                # Ingesta de datos (RAW)
├── transformation/           # Transformación y feature engineering (SILVER)
├── training/                 # Entrenamiento del modelo
├── evaluation/               # Evaluación del modelo
└── config/                   # Configuración compartida (features, esquemas, etc.)
```

---

## 🧠 Rol de `full_mlops_flow.py`

El archivo `full_mlops_flow.py` actúa como **orquestador principal del pipeline MLOps**, conectando y ejecutando de forma secuencial todos los flows funcionales del sistema.

Este flow **no implementa lógica de negocio propia**, sino que reutiliza flows ya existentes, garantizando:

- separación de responsabilidades
- reutilización de código
- trazabilidad completa end-to-end
- facilidad de mantenimiento

### 🔄 Secuencia de ejecución

El pipeline completo se ejecuta en el siguiente orden:

1. **Ingesta de datos**  
   Ejecuta `data_ingestion_flow`  
   - genera eventos sintéticos
   - guarda datos RAW en MinIO
   - registra la ingesta en PostgreSQL

2. **Transformación de datos**  
   Ejecuta `data_transformation_flow`  
   - transforma datos RAW → SILVER
   - sube datasets procesados a MinIO
   - registra auditoría en PostgreSQL

3. **Entrenamiento del modelo**  
   Ejecuta `model_training_flow`  
   - entrena Isolation Forest
   - versiona el modelo en MinIO
   - registra parámetros y metadata

4. **Evaluación del modelo**  
   Ejecuta `model_evaluation_flow`  
   - evalúa el modelo entrenado
   - almacena métricas en MinIO
   - registra resultados en PostgreSQL

### ☸️ Ejecución en Kubernetes

Este flow se ejecuta como un **Job de Kubernetes**, utilizando una imagen Docker específica del proyecto.

- No requiere intervención manual
- No depende de estado persistente local
- Se apoya exclusivamente en servicios internos del clúster

De esta forma, `full_mlops_flow.py` representa una **implementación realista de un pipeline MLOps batch productivo**, alineado con prácticas industriales.
---

## 🧭 Uso de Prefect como orquestador ligero

En este proyecto se utiliza **Prefect** como framework de orquestación de flujos, **sin desplegar Prefect Server ni Prefect Cloud**.

Esta decisión es **intencionada y justificada**, y responde a los objetivos del proyecto.

### 🧠 ¿Por qué usar Prefect sin servidor?

Prefect permite ejecutar flows de dos formas:

- modo **orquestado centralizado** (Prefect Server / Cloud)
- modo **local o embebido** (flow execution engine)

En este pipeline se utiliza el segundo enfoque, lo que permite:

- definir flujos declarativos (`@flow`, `@task`)
- mantener trazabilidad estructurada por logs
- controlar dependencias entre tasks
- ejecutar todo dentro de Kubernetes como un Job estándar

sin introducir infraestructura adicional innecesaria.

### ⚖️ Justificación de diseño

No se utiliza Prefect Server porque:

- el pipeline se ejecuta como batch diario
- no se requieren reintentos distribuidos complejos
- no se necesita scheduling externo (lo aporta Kubernetes)
- no se requiere UI de orquestación para este alcance

Kubernetes ya actúa como **scheduler, aislador y runtime**, por lo que añadir Prefect Server duplicaría responsabilidades.

### 🎯 Beneficios del enfoque adoptado

Este enfoque permite:

- mantener el pipeline **simple y robusto**
- reducir superficie operativa
- mejorar la reproducibilidad
- facilitar la evaluación académica
- evolucionar fácilmente a Prefect Server si fuese necesario

El diseño demuestra que **MLOps no implica sobreingeniería**, sino decisiones coherentes con el caso de uso.
---

## 🗄️ Rol de PostgreSQL en el pipeline MLOps

En este pipeline, **PostgreSQL no se utiliza como base de datos de eventos ni como data lake**, sino exclusivamente como **repositorio de metadatos y auditoría** del ciclo de vida MLOps.

### 📌 ¿Qué se almacena en PostgreSQL?

PostgreSQL registra únicamente información estructurada sobre cada ejecución del pipeline, incluyendo:

- eventos de ingesta de datos
- transformaciones ejecutadas
- entrenamientos realizados
- evaluaciones completadas

Cada registro representa una **evidencia auditable** de una operación del pipeline.

### 📦 ¿Qué NO se almacena en PostgreSQL?

PostgreSQL **no almacena**:

- datasets (RAW / SILVER)
- modelos entrenados
- artefactos de evaluación
- ficheros parquet o binarios

Todos los artefactos pesados se almacenan en **MinIO**, que actúa como data lake y model registry.

### 🧠 Separación clara de responsabilidades

Esta separación responde a un principio fundamental de MLOps:

- **MinIO** → datos y modelos versionados
- **PostgreSQL** → metadatos, estado y trazabilidad
- **Prefect** → orquestación del proceso
- **Kubernetes** → ejecución y aislamiento

Gracias a este diseño, el pipeline es:

- escalable
- auditable
- fácil de mantener
- alineado con arquitecturas MLOps reales

### 🔍 Beneficio para trazabilidad y compliance

El uso de PostgreSQL permite responder preguntas críticas como:

- ¿Cuándo se entrenó este modelo?
- ¿Con qué dataset?
- ¿Cuántos registros se usaron?
- ¿Qué métricas obtuvo?
- ¿Falló o fue exitoso?

Esto es especialmente relevante en **entornos de ciberseguridad**, donde la explicabilidad y la auditoría son requisitos clave.

---

## 🪣 Rol de MinIO como Data Lake y Model Registry

MinIO actúa como el **sistema de almacenamiento persistente principal** del pipeline MLOps, cumpliendo dos funciones críticas:

- **Data Lake** para datasets versionados
- **Model Registry** para artefactos de machine learning

MinIO implementa una interfaz compatible con **Amazon S3**, lo que permite aplicar patrones estándar de almacenamiento utilizados en entornos industriales.

---

### 📊 Organización por capas (Data Lake)

Los datos y artefactos se organizan en buckets independientes que representan distintas capas del pipeline:

- **RAW** (`cybersec-ml-raw`)  
  Datos ingeridos sin procesar

- **SILVER** (`cybersec-ml-silver`)  
  Datos transformados y enriquecidos

- **MODELS** (`cybersec-ml-models`)  
  Modelos entrenados y versionados

- **EVAL** (`cybersec-ml-eval`)  
  Resultados de evaluación del modelo

Esta separación facilita:

- trazabilidad entre capas
- rollback de versiones
- reproducibilidad total del pipeline

---

### 🧠 MinIO como Model Registry ligero

En lugar de utilizar una solución compleja de model registry, MinIO se emplea como un **registro de modelos sencillo pero eficaz**, donde:

- cada modelo se guarda con un nombre versionado por timestamp
- los modelos son inmutables
- los modelos pueden ser recuperados por otros servicios (batch o serving)

Este enfoque es coherente con pipelines batch y entornos Kubernetes-first.

---

### 🔐 Persistencia desacoplada del entorno de ejecución

El pipeline se ejecuta dentro de contenedores efímeros en Kubernetes.  
Los archivos locales generados durante la ejecución:

- existen únicamente durante la vida del contenedor
- se utilizan como almacenamiento temporal
- se suben inmediatamente a MinIO

Esto garantiza que:

- el pipeline sea completamente reproducible
- no existan dependencias del entorno local
- el almacenamiento persistente esté desacoplado del cómputo

---

### ⚙️ Ventajas frente a almacenamiento local

El uso de MinIO aporta:

- compatibilidad S3 estándar
- integración nativa con Kubernetes
- escalabilidad horizontal
- aislamiento entre ejecución y persistencia
- alineación con arquitecturas cloud-native

Gracias a esto, el pipeline puede ejecutarse íntegramente dentro del clúster sin acceso al sistema de archivos del host.

---

## ☸️ Ejecución del pipeline en Kubernetes

El pipeline MLOps se ejecuta **íntegramente dentro de un clúster Kubernetes**, utilizando un **Job** como unidad de ejecución.  
No existe dependencia alguna de ejecución local ni de servicios externos al clúster.

---

### 🧠 Modelo de ejecución

El flujo completo se ejecuta como:

- un contenedor efímero
- lanzado mediante un objeto `Job`
- que ejecuta el flow principal `full_mlops_flow.py`
- y finaliza automáticamente al completar el pipeline

Este enfoque es ideal para pipelines **batch MLOps**, donde cada ejecución es independiente y reproducible.

---

### 📦 Imagen Docker del pipeline

El pipeline se empaqueta en una imagen Docker específica que contiene:

- Python 3.11
- dependencias del pipeline (`requirements.pipeline.txt`)
- código del directorio `pipeline/`

La imagen **no contiene datos persistentes** y se limita a ejecutar el pipeline end-to-end.

Ejemplo de imagen utilizada:

```text
rcabe005/cybersec-mlops-runner:latest
```

### 🗂️ Job de Kubernetes

La ejecución se define mediante un manifiesto Kubernetes (Job) que:

- lanza un único contenedor

- inyecta variables de entorno mediante Secrets

- no expone puertos

- no mantiene estado tras la finalización

Archivo de referencia:

```text
infra/k8s/job-full-mlops.yaml
```

Este diseño garantiza:

- aislamiento por ejecución

- control total del ciclo de vida

- fácil re-ejecución del pipeline

- integración natural con CI/CD

### 🔐 Gestión de configuración y secretos

Las credenciales necesarias (MinIO, PostgreSQL, etc.):

- no se incluyen en la imagen Docker

- se inyectan mediante **Secrets de Kubernetes**

- se consumen como variables de entorno

Esto cumple con buenas prácticas de seguridad y separación de responsabilidades.

### 🔁 Reproducibilidad y limpieza automática

Cada ejecución del Job:

- comienza desde un entorno limpio

- descarga únicamente los artefactos necesarios desde MinIO

- genera nuevos artefactos versionados

- finaliza sin dejar estado residual en el nodo

Gracias a este enfoque:

- no existen efectos colaterales entre ejecuciones

- el pipeline es totalmente reproducible

- el sistema es escalable horizontalmente

### ✅ Ventajas del enfoque Job-based

- alineado con arquitecturas cloud-native

- evita servicios persistentes innecesarios

- simplifica el debugging y el control de versiones

- refleja escenarios reales de producción batch

Este modelo constituye la base para futuras extensiones como:

- programación periódica (CronJob)

- integración CI/CD

- despliegue de inferencia online

---


## 📌 Nota sobre los paths locales

En el contexto de este pipeline, los términos *local* o *ruta local* hacen referencia **exclusivamente al sistema de archivos del contenedor que ejecuta el Job en Kubernetes**, no al equipo del desarrollador.

Todos los paths como:

```text
data/ingested/
data/silver/
data/models/
data/eval/
```

existen únicamente **durante la ejecución del contenedor** y se utilizan como almacenamiento temporal antes de subir los artefactos a MinIO.

Esto garantiza que:

- el pipeline sea completamente reproducible

- no existan dependencias del entorno local

- el almacenamiento persistente esté desacoplado (MinIO)

El pipeline puede ejecutarse íntegramente dentro del clúster sin acceso al sistema de archivos del host.

---

## 📊 Gestión de datos y modelos

El pipeline implementa una separación clara de capas:

- RAW: datos ingeridos sin procesar

- SILVER: datos transformados y listos para modelado

- MODELS: artefactos entrenados y versionados

- EVAL: resultados de evaluación

Todos los artefactos se almacenan en MinIO, con nombres versionados basados en timestamps para garantizar reproducibilidad.

---

## 🧾 Trazabilidad y auditoría

Cada ejecución del pipeline registra eventos clave en PostgreSQL, incluyendo:

- Ingestas realizadas

- Transformaciones aplicadas

- Entrenamientos ejecutados

- Evaluaciones completadas

Esto permite responder a preguntas como:

- ¿Qué datos se usaron para entrenar este modelo?

- ¿Cuándo se generó?

- ¿Con qué parámetros?

- ¿Qué métricas obtuvo?

---

## ⚠️ Alcance y decisiones de diseño

Este pipeline no incluye todavía:

- Tracking avanzado con MLflow

- Serving online del modelo

- Monitorización en tiempo real

Estas funcionalidades se consideran trabajo futuro, y se han excluido deliberadamente para mantener el foco en la robustez del pipeline batch, que es la base de cualquier sistema MLOps sólido.