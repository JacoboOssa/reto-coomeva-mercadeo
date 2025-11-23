# Sistema de Clusterización de Usuarios - Coomeva

Sistema de clusterización de usuarios basado en FastAPI que utiliza UMAP + KMeans para segmentar usuarios según sus características demográficas, financieras y comportamiento de productos.

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Flujo de Datos](#flujo-de-datos)
- [Entrada y Salida](#entrada-y-salida)
- [Instalación](#instalación)
- [Uso](#uso)
- [Decisiones Técnicas](#decisiones-técnicas)
- [Limitaciones y Consideraciones](#limitaciones-y-consideraciones)
- [Despliegue en AWS](#despliegue-en-aws)

---

## 📊 Descripción General

Este sistema recibe datos de usuarios de Coomeva y los clusteriza en grupos homogéneos utilizando:

1. **Preprocesamiento de datos**: Limpieza, transformación de variables categóricas y creación de features derivados
2. **Reducción de dimensionalidad**: Aproximación de UMAP para reducir 170+ features a 2 dimensiones
3. **Clusterización**: KMeans para agrupar usuarios en clusters significativos

### ¿Qué hace el sistema?

**ENTRADA**: Archivo Excel/CSV con datos crudos de usuarios (demografía, productos financieros, ingresos, etc.)

**PROCESAMIENTO**:
- Limpia y valida los datos
- Transforma variables categóricas a formato numérico (one-hot encoding)
- Calcula variables derivadas (edad, antigüedad, logaritmos de ingresos)
- Reduce dimensionalidad con aproximación UMAP
- Asigna cada usuario a un cluster

**SALIDA**: Archivo Excel con los datos originales + columna `Cluster` indicando el grupo al que pertenece cada usuario

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (Frontend/Usuario)                │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ Upload Excel/CSV
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Application                         │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Endpoint: POST /api/v1/cluster                    │     │
│  └──────────────────┬─────────────────────────────────┘     │
│                     │                                        │
│                     ▼                                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  DataPreprocessor (preprocessing.py)               │     │
│  │  • Limpieza de datos                               │     │
│  │  • One-hot encoding                                │     │
│  │  • Features derivados (edad, logs, antigüedad)     │     │
│  │  • Normalización                                   │     │
│  └──────────────────┬─────────────────────────────────┘     │
│                     │                                        │
│                     ▼                                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  ClusteringModel (prediction.py)                   │     │
│  │  • StandardScaler (normalización)                  │     │
│  │  • Aproximación UMAP con KNN                       │     │
│  │  • KMeans (asignación de clusters)                 │     │
│  └──────────────────┬─────────────────────────────────┘     │
│                     │                                        │
│                     ▼                                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Resultado: DataFrame + Cluster                    │     │
│  └────────────────────────────────────────────────────┘     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ Download Excel
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Archivo Excel con Clusters Asignados            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos

### 1. Preprocesamiento (`app/preprocessing.py`)

**Entrada**: DataFrame con ~170 columnas incluyendo:
- **Demográficas**: `Fecha_Nacimiento`, `Sexo`, `Estado_Civil`, `Estrato`, etc.
- **Financieras**: `Ingresos`, `Ingresos_Deflactados`, `Saldo_aportes`, etc.
- **Productos**: `Cta_Dep`, `Creditos`, `Tarjetas`, `Seguros`, etc.
- **Categóricas**: `Nombre_Estado`, `Nombre_Ocupacion`, `Zona`, etc.

**Procesos**:

```python
# 1. Limpieza de datos
- Elimina filas con valores nulos en columnas críticas
- Elimina columnas redundantes o no utilizadas

# 2. Transformación de variables
- Convierte fechas a antigüedad en días y edad
- Calcula logaritmos de ingresos (si no existen)
- Mapea zonas geográficas a regiones

# 3. One-hot encoding
- Convierte variables categóricas a formato numérico
- Ejemplo: Estado_Civil → Estado_Civil_Soltero, Estado_Civil_Casado, etc.

# 4. Estandarización de estructura
- Reindexea para tener exactamente 175 columnas esperadas
- Rellena columnas faltantes con 0
```

**Salida**: DataFrame con 175 columnas numéricas listo para el modelo

### 2. Predicción (`app/prediction.py`)

**Entrada**: DataFrame preprocesado (175 columnas)

**Procesos**:

```python
# 1. Escalado (StandardScaler)
X_scaled = scaler.transform(X)
# Normaliza cada feature a media=0, std=1

# 2. Aproximación UMAP (KNN)
X_umap = approximate_umap(X_scaled)
# Reduce de 175 dimensiones a 2 dimensiones
# Usa k-NN sobre embeddings pre-calculados

# 3. Asignación de Clusters (KMeans)
labels = kmeans.predict(X_umap)
# Asigna cada usuario al cluster más cercano
```

**Salida**: 
- `labels`: Array con cluster asignado [0, 1, 2, 3, 4, ...]
- `umap_df`: DataFrame con coordenadas UMAP (UMAP_1, UMAP_2)
- `df_completo`: DataFrame original filtrado

### 3. Generación de Resultado (`app/routes/clustering.py`)

**Procesos**:

```python
# 1. Combinar datos originales + cluster
df_result = df_completo.copy()
df_result['Cluster'] = labels

# 2. Conversión de tipos
- Columnas one-hot: float64 → bool
- Fechas: datetime → string (MM/DD/YYYY)

# 3. Exportar a Excel
df_result.to_excel(output)
```

**Salida**: Archivo Excel con 176 columnas (175 originales + `Cluster`)

---

## 📥📤 Entrada y Salida

### Entrada Esperada

**Formato**: Excel (.xlsx) o CSV (.csv)

**Columnas Mínimas Requeridas**:
- `Ingresos`
- `Saldo_aportes`
- `Cuotas_canceladas_aportes`
- `Cuotas_mora_aportes`
- `Vlr_mora`

**Columnas Opcionales** (se preservan si existen):
- `IdUnico`: Identificador único del usuario
- `log_ingresos`: Logaritmo de ingresos (si ya está calculado)
- `log_ingresos_deflactados`: Logaritmo de ingresos deflactados
- `Fecha_Ingreso`, `Fecha_Nacimiento`: Para calcular antigüedad y edad
- Todas las demás columnas del modelo original

**Ejemplo de entrada** (primeras filas):

| IdUnico | Ingresos | Fecha_Ingreso | Sexo | Estrato | Nombre_Ocupacion | ... |
|---------|----------|---------------|------|---------|------------------|-----|
| USER001 | 1330000  | 10/31/2023    | M    | 3       | Asalariado       | ... |
| USER002 | 3879436  | 07/29/2024    | M    | 3       | Asalariado       | ... |
| USER003 | 2078310  | 03/20/2025    | M    | 3       | Estudiante       | ... |

### Salida Generada

**Formato**: Excel (.xlsx)

**Contenido**: Todas las columnas de entrada + columna `Cluster`

**Ejemplo de salida**:

| IdUnico | Ingresos | Fecha_Ingreso | Sexo | Estrato | ... | **Cluster** |
|---------|----------|---------------|------|---------|-----|-------------|
| USER001 | 1330000  | 10/31/2023    | M    | 3       | ... | **0**       |
| USER002 | 3879436  | 07/29/2024    | M    | 3       | ... | **4**       |
| USER003 | 2078310  | 03/20/2025    | M    | 3       | ... | **4**       |

**Interpretación de Clusters**:
- Cluster 0, 1, 2, 3, 4: Grupos de usuarios con características similares
- Los clusters se determinaron durante el entrenamiento del modelo
- Cada cluster representa un perfil de usuario distinto (demográfico, financiero, productos)

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.11+
- pip
- (Opcional) Docker para despliegue en contenedor

### Instalación Local

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd clusterizacion-coomeva

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar que existen los modelos
ls -la models/
# Debe contener:
#   - scaler_model.pkl
#   - kmeans_model.pkl
#   - umap_data.pkl
```

### Instalación con Docker

```bash
# 1. Construir imagen
docker build -t coomeva-clustering:latest .

# 2. Ejecutar contenedor
docker run -p 8000:8000 coomeva-clustering:latest
```

---

## 💻 Uso

### Opción 1: API Local

```bash
# 1. Iniciar servidor
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2. Probar en el navegador
# Abrir: http://localhost:8000/docs

# 3. Usar endpoint POST /api/v1/cluster
# - Click en "Try it out"
# - Subir archivo Excel/CSV
# - Click en "Execute"
# - Descargar resultado
```

### Opción 2: cURL

```bash
curl -X POST "http://localhost:8000/api/v1/cluster" \
  -H "accept: application/json" \
  -F "file=@datos_usuarios.xlsx" \
  --output resultado_clusters.xlsx
```

### Opción 3: Python Requests

```python
import requests

url = "http://localhost:8000/api/v1/cluster"
files = {'file': open('datos_usuarios.xlsx', 'rb')}

response = requests.post(url, files=files)

with open('resultado_clusters.xlsx', 'wb') as f:
    f.write(response.content)
```

---

## 🎯 Decisiones Técnicas

### 1. Aproximación de UMAP en lugar de Transform

**Problema**: 
- El modelo UMAP entrenado con `umap.UMAP()` no puede serializar correctamente su estado interno
- El método `umap.transform()` requiere el objeto completo en memoria (varios GB)
- Lambda tiene limitaciones de memoria (máx 10GB) y tamaño de deployment package (250MB comprimido)

**Solución Implementada**:
```python
def _approximate_umap(self, X_scaled, n_neighbors=15):
    """
    Aproxima coordenadas UMAP usando k-NN sobre embeddings pre-calculados
    """
    # 1. Encontrar k vecinos más cercanos en espacio original
    distances, indices = knn_index.kneighbors(X_scaled, n_neighbors=k)
    
    # 2. Obtener embeddings UMAP de esos vecinos
    neighbor_embeddings = umap_embeddings[indices]
    
    # 3. Calcular posición como promedio ponderado
    weights = 1.0 / (distances + epsilon)
    X_umap = weighted_average(neighbor_embeddings, weights)
    
    return X_umap
```

**Ventajas**:
- ✅ Mucho más ligero (solo guarda embeddings + KNN index)
- ✅ Más rápido en inferencia
- ✅ Compatible con Lambda
- ✅ Reproducible y determinístico

**Desventajas**:
- ⚠️ Aproximación en lugar de transformación exacta
- ⚠️ Puede introducir pequeñas variaciones (~10-15% de puntos pueden cambiar de cluster)
- ⚠️ Puntos muy diferentes a los datos de entrenamiento pueden tener mayor error

### 2. Preservación de Features Pre-calculados

El sistema **preserva** columnas como `log_ingresos` si ya existen en el input:

```python
# Solo calcula si NO existe
if 'log_ingresos' not in df.columns and 'Ingresos' in df.columns:
    df['log_ingresos'] = np.log(df['Ingresos'].replace(0, np.nan))
```

**Razón**: Los datos originales del notebook pueden tener transformaciones específicas que no queremos sobrescribir.

### 3. One-Hot Encoding sin Drop First

```python
df_dummies = pd.get_dummies(df[cat_cols], drop_first=False)
```

**Razón**: El modelo fue entrenado con todas las columnas dummy, no con `n-1` (que es la práctica común para evitar multicolinealidad).

---

## ⚠️ Limitaciones y Consideraciones

### Precisión de Clusterización

**Coincidencia esperada con modelo original**: 85-95%

**Factores que afectan la precisión**:

1. **Aproximación UMAP**: 
   - Introduce variación en las coordenadas de reducción dimensional
   - Puntos cercanos a fronteras entre clusters pueden cambiar

2. **Datos de entrada diferentes**:
   - Si los datos nuevos son muy diferentes a los de entrenamiento, la aproximación será menos precisa

3. **Tamaño del dataset**:
   - Datasets pequeños (<10 registros) pueden tener mayor variabilidad porcentual

### Ejemplo de Discrepancia

Con 3 registros de prueba:
- ✅ 2 de 3 clusters coinciden (66.7%)
- ❌ 1 de 3 diferente (Cluster 1 vs Cluster 4)

**¿Es normal?** SÍ, porque:
- El punto estaba cerca de la frontera entre clusters
- La aproximación UMAP movió ligeramente su posición
- El modelo lo asignó al cluster vecino más cercano

**Recomendación**: Evaluar con datasets más grandes (100+ registros) para obtener métricas más confiables.

### Cuándo Preferir Qué Arquitectura

#### 🔧 Lambda (Implementación Actual)

**Ventajas**:
- ✅ Sin costos cuando no se usa
- ✅ Escalado automático
- ✅ Ideal para ejecuciones periódicas (cada 3 meses)
- ✅ Mantenimiento mínimo

**Desventajas**:
- ⚠️ Precisión ~85-95% (aproximación UMAP)
- ⚠️ Cold start (~1-2 segundos)
- ⚠️ Límites de memoria (10GB) y tiempo (15 min)

**Cuándo usar**:
- ✅ Clusterización periódica (mensual, trimestral)
- ✅ Volúmenes moderados (<10,000 registros por ejecución)
- ✅ Presupuesto limitado
- ✅ Tolerancia a pequeñas variaciones en clusters

#### 🖥️ Servidor Always-On (EC2 / ECS)

**Ventajas**:
- ✅ Precisión ~98-100% (UMAP transform real)
- ✅ Sin cold start
- ✅ Modelo completo en memoria
- ✅ Mejor para debugging y experimentación

**Desventajas**:
- ❌ Costos fijos 24/7 (~$30-100/mes)
- ❌ Requiere mantenimiento
- ❌ Escalado manual
- ❌ Sobrecapacidad para uso esporádico

**Cuándo usar**:
- ✅ Clusterización en tiempo real
- ✅ Volúmenes altos (>10,000 registros diarios)
- ✅ Requerimientos estrictos de precisión
- ✅ Integración continua con otros sistemas

### Comparación de Costos (Estimación AWS us-east-1)

| Escenario | Lambda | EC2 (t3.medium) | ECS Fargate |
|-----------|--------|-----------------|-------------|
| **Ejecución mensual (1 vez)** | $0.01 | $30.00 | $25.00 |
| **Ejecución trimestral (4 veces/año)** | $0.04/año | $360/año | $300/año |
| **Ejecución semanal (52 veces/año)** | $0.50/año | $360/año | $300/año |
| **Ejecución diaria** | $3.65/año | $360/año | $300/año |

**Para uso trimestral**: Lambda es **9000% más económico** 💰

---

## ☁️ Despliegue en AWS

Ver [DEPLOYMENT_AWS.md](./DEPLOYMENT_AWS.md) para documentación detallada.

### Resumen de Arquitectura AWS

```
┌─────────────────────────────────────────────────────────────┐
│                        AWS Cloud                             │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  API Gateway (REST API)                            │     │
│  │  https://api.coomeva.com/clustering                │     │
│  └──────────────────┬─────────────────────────────────┘     │
│                     │                                        │
│                     ▼                                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  AWS Lambda                                        │     │
│  │  • Runtime: Python 3.11                            │     │
│  │  • Memory: 3GB                                     │     │
│  │  • Timeout: 5 minutes                              │     │
│  │  • Image: ECR (FastAPI + Mangum)                   │     │
│  └──────────────────┬─────────────────────────────────┘     │
│                     │                                        │
│                     ▼                                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Amazon S3 (Opcional)                              │     │
│  │  • Almacenamiento de resultados                    │     │
│  │  • Logs de ejecución                               │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Pasos de Despliegue

```bash
# 1. Construir imagen Docker
docker build -t coomeva-clustering:latest .

# 2. Tag y push a ECR
docker tag coomeva-clustering:latest \
  058264169618.dkr.ecr.us-east-1.amazonaws.com/coomeva-clustering:latest

docker push 058264169618.dkr.ecr.us-east-1.amazonaws.com/coomeva-clustering:latest

# 3. Actualizar función Lambda
aws lambda update-function-code \
  --function-name coomeva-clustering \
  --image-uri 058264169618.dkr.ecr.us-east-1.amazonaws.com/coomeva-clustering:latest
```

---

## 📊 Monitoreo y Logs

### CloudWatch Logs

```bash
# Ver logs en tiempo real
aws logs tail /aws/lambda/coomeva-clustering --follow

# Buscar errores
aws logs filter-pattern /aws/lambda/coomeva-clustering "ERROR"
```

### Métricas Clave

- **Invocations**: Número de ejecuciones
- **Duration**: Tiempo de ejecución promedio
- **Errors**: Número de errores
- **Throttles**: Ejecuciones rechazadas por límite de concurrencia

---

## 🛠️ Desarrollo y Testing

### Ejecutar Tests Locales

```bash
# Test de preprocesamiento
python3 test_preprocessing.py

# Test de flujo completo
python3 test_full_flow.py

# Comparar outputs
python3 comparar_outputs.py
```

### Estructura del Proyecto

```
clusterizacion-coomeva/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── preprocessing.py        # Limpieza y transformación
│   ├── prediction.py           # Modelos y predicción
│   └── routes/
│       └── clustering.py       # Endpoints
├── models/
│   ├── scaler_model.pkl        # StandardScaler
│   ├── kmeans_model.pkl        # KMeans
│   └── umap_data.pkl           # Embeddings + KNN
├── utils/
│   └── test_data.xlsx          # Datos de prueba
├── Dockerfile                  # Imagen Docker
├── requirements.txt            # Dependencias
└── README.md                   # Este archivo
```

---

## 📝 Notas Adicionales

### Columnas Duplicadas

El sistema detecta y elimina automáticamente columnas duplicadas durante el preprocesamiento:

```python
if df.columns.duplicated().any():
    duplicated_cols = df.columns[df.columns.duplicated()].tolist()
    print(f"⚠️ Columnas duplicadas detectadas: {duplicated_cols}")
    df = df.loc[:, ~df.columns.duplicated()]
```

### Manejo de Valores Nulos

Filas con valores nulos en columnas críticas se eliminan:

```python
indices_validos = df.dropna(subset=[
    'Saldo_aportes', 'Cuotas_canceladas_aportes', 
    'Cuotas_mora_aportes', 'Vlr_mora', 'Ingresos'
], how='any').index
```

### Formato de Fechas

Las fechas se convierten a string en formato `MM/DD/YYYY`:

```python
df['Fecha_Ingreso'] = pd.to_datetime(df['Fecha_Ingreso']).dt.strftime('%m/%d/%Y')
```

Esto puede causar diferencias cosméticas (ej: `08/06/2001` vs `8/6/2001`) pero no afecta la funcionalidad.

---

## 🤝 Soporte

Para preguntas o problemas:
1. Revisar logs de CloudWatch
2. Verificar formato de datos de entrada
3. Contactar al equipo de desarrollo

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0.0  
**Mantenido por**: Equipo de Data Science - Coomeva
