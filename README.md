# Reto Mercadeo Coomeva - Documentación Completa

## 📋 Índice

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Componentes del Sistema](#componentes-del-sistema)
4. [Manual de Despliegue](#manual-de-despliegue)
   - [Backend de Clusterización (FastAPI + AWS Lambda)](#1-backend-de-clusterización-fastapi--aws-lambda)
   - [Frontend (React + Vite)](#2-frontend-react--vite)
   - [Base de Datos (Supabase)](#3-base-de-datos-supabase)
   - [Agente N8N](#4-agente-n8n)
5. [Manual de Operación](#manual-de-operación)
6. [Manual de Funcionamiento Técnico](#manual-de-funcionamiento-técnico)
7. [Notebooks de Análisis](#notebooks-de-análisis)
8. [Configuración de Servicios Externos](#configuración-de-servicios-externos)
9. [Troubleshooting](#troubleshooting)
10. [Recomendaciones de Seguridad](#recomendaciones-de-seguridad)

---

## Descripción General

Solución integral para la segmentación y análisis avanzado de clientes en Coomeva. El sistema combina procesamiento de datos, clusterización mediante técnicas de Machine Learning (UMAP + KMeans), y visualización interactiva, todo orquestado por flujos automatizados en N8N y desplegado sobre infraestructura serverless para máxima eficiencia y mínimo costo.

### Objetivos del Sistema

- **Segmentación de Clientes**: Agrupar clientes en clusters homogéneos basados en características demográficas, financieras y de comportamiento
- **Análisis de Perfiles**: Generar arquetipos y perfiles detallados para cada cliente
- **Recomendaciones Personalizadas**: Proporcionar estrategias de comunicación y productos sugeridos por cliente
- **Operación Automatizada**: Flujos automatizados mediante N8N para procesamiento y consultas

### Tecnologías Principales

- **Backend**: FastAPI (Python 3.11), AWS Lambda, Docker
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, shadcn/ui
- **Base de Datos**: Supabase (PostgreSQL)
- **Orquestación**: N8N
- **Machine Learning**: UMAP, KMeans, scikit-learn
- **Procesamiento de Datos**: Pandas, NumPy

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO FINAL                            │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Portal de Ventas Coomeva                                 │   │
│  │  • Consulta de clientes                                  │   │
│  │  • Clusterización de nuevos clientes                      │   │
│  │  • Búsqueda por arquetipos                                │   │
│  └───────────────────────┬──────────────────────────────────┘   │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           │ HTTP Requests
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENTE N8N (Orquestador)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Flujos Automatizados                                     │   │
│  │  • Webhook para consultas                                 │   │
│  │  • Invocación de Lambda                                   │   │
│  │  • Consultas a Supabase                                   │   │
│  │  • Integración con Gemini AI                              │   │
│  └───────┬───────────────────────────────┬───────────────────┘   │
└──────────┼───────────────────────────────┼──────────────────────┘
           │                               │
           │                               │
           ▼                               ▼
┌──────────────────────┐      ┌──────────────────────────────┐
│  AWS Lambda          │      │  Supabase (PostgreSQL)        │
│  (FastAPI Backend)   │      │  • Tabla: datos               │
│  ┌────────────────┐  │      │  • Almacenamiento de          │
│  │ Preprocessing  │  │      │    resultados                  │
│  │ UMAP + KMeans │  │      │  • Consultas de perfiles       │
│  │ Clustering    │  │      └──────────────────────────────┘
│  └────────────────┘  │
└──────────────────────┘
```

### Flujo de Datos Principal

1. **Consulta de Cliente**: Usuario → Frontend → N8N → Supabase → Gemini AI → Frontend
2. **Clusterización**: Usuario → Frontend → N8N → AWS Lambda → Supabase → Frontend
3. **Búsqueda por Arquetipo**: Usuario → Frontend → N8N → Supabase → Gemini AI → Frontend

---

## Componentes del Sistema

### 1. Backend de Clusterización (`/clusterizacion-coomeva`)

**Descripción**: API REST desarrollada en FastAPI que realiza la clusterización de clientes usando técnicas de Machine Learning.

**Funcionalidades**:
- Preprocesamiento de datos: Limpieza, transformación de variables categóricas y creación de features derivados
- Reducción de dimensionalidad: Aproximación UMAP para condensar más de 170 variables en 2 dimensiones
- Clusterización: Algoritmo KMeans para agrupar clientes en segmentos significativos

**Tecnologías**:
- FastAPI 0.115.0
- Pandas 2.2.3
- NumPy 2.0.2
- scikit-learn 1.6.1
- Mangum (adaptador AWS Lambda)

**Endpoints**:
- `POST /api/v1/cluster`: Recibe archivo CSV/XLSX y retorna archivo con clusters asignados
- `GET /health`: Health check del servicio
- `GET /`: Información básica de la API

### 2. Frontend (`/coomeva-sales-hub`)

**Descripción**: Aplicación web moderna desarrollada en React con TypeScript que proporciona una interfaz intuitiva para consultar clientes, clusterizar nuevos datos y buscar por arquetipos.

**Funcionalidades**:
- Consulta de cliente por ID y producto
- Carga y procesamiento de archivos para clusterización
- Búsqueda y visualización de arquetipos
- Autenticación mediante Supabase Auth
- Visualización de resultados con componentes interactivos

**Tecnologías**:
- React 18.3.1
- TypeScript 5.8.3
- Vite 5.4.19
- TailwindCSS 3.4.17
- shadcn/ui (componentes)
- Supabase Client 2.79.0
- React Router 6.30.1

**Páginas Principales**:
- `/auth`: Autenticación de usuarios
- `/dashboard`: Panel principal con todas las funcionalidades

### 3. Base de Datos (Supabase)

**Descripción**: Base de datos PostgreSQL alojada en Supabase que almacena todos los datos de clientes, clusters y resultados de análisis.

**Esquema Principal**:
- Tabla `datos`: Contiene todos los datos de clientes con 178 columnas incluyendo información demográfica, financiera, productos y cluster asignado

**Archivo de Esquema**: `coomeva_cluster_db_schema.sql`

### 4. Agente N8N

**Descripción**: Flujos automatizados que orquestan las operaciones entre el frontend, backend y base de datos.

**Flujos Principales**:
- **Consulta de Cliente**: Recibe cédula y producto, consulta Supabase, genera perfil con Gemini AI
- **Clusterización**: Recibe archivo, invoca AWS Lambda, almacena resultados en Supabase
- **Búsqueda por Arquetipo**: Consulta clusters y genera estrategias con Gemini AI

**Archivos de Configuración**:
- `COOMEVA AGENTE - W FRONTEND.json`: Flujo principal integrado con frontend

### 5. Notebooks de Análisis

**Descripción**: Jupyter notebooks que contienen el análisis exploratorio y el proceso de entrenamiento de los modelos.

**Archivos**:
- `Nueva_Clusterizacion(UMAP+Kmeans).ipynb`: Notebook principal con el proceso completo de clusterización
- `Analisis-Exploratorio-2.ipynb`: Análisis exploratorio de datos

---

## Manual de Despliegue

### 1. Backend de Clusterización (FastAPI + AWS Lambda)

#### 1.1 Requisitos Previos

- Cuenta de AWS con permisos para:
  - AWS Lambda
  - Amazon ECR (Elastic Container Registry)
  - API Gateway
  - CloudWatch Logs
- Docker instalado
- AWS CLI configurado (`aws configure`)

#### 1.2 Preparación del Entorno Local

```bash
# 1. Navegar al directorio del backend
cd clusterizacion-coomeva

# 2. Crear entorno virtual (opcional, para desarrollo local)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias localmente (solo para testing)
pip install -r requirements.txt

# 4. Verificar que existen los modelos entrenados
ls -la models/
# Debe contener:
#   - scaler_model.pkl
#   - kmeans_model.pkl
#   - umap_data.pkl
```

#### 1.3 Construcción y Subida de Imagen Docker a AWS ECR

```bash
# 1. Autenticarse en AWS
aws configure

# 2. Obtener el ID de cuenta de AWS
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION="us-east-1"  # Ajustar según tu región

# 3. Crear repositorio ECR (solo la primera vez)
aws ecr create-repository \
  --repository-name coomeva-cluster-api \
  --region $AWS_REGION

# 4. Obtener token de autenticación de Docker para ECR
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# 5. Construir la imagen Docker
cd clusterizacion-coomeva
docker build -t coomeva-cluster-api:latest .

# 6. Etiquetar la imagen para ECR
docker tag coomeva-cluster-api:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/coomeva-cluster-api:latest

# 7. Subir la imagen a ECR
docker push \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/coomeva-cluster-api:latest
```

#### 1.4 Crear Función Lambda desde Imagen ECR

**Opción A: Desde la Consola Web (Recomendado para principiantes)**

1. Ve a AWS Lambda en la consola de AWS
2. Click en "Crear función"
3. Selecciona "Desde imagen de contenedor"
4. Configura:
   - **Nombre de función**: `coomeva-cluster-lambda`
   - **URI de imagen**: Selecciona el repositorio `coomeva-cluster-api` y la imagen `latest`
   - **Arquitectura**: `x86_64`
5. Click en "Crear función"
6. Configurar variables de entorno (si es necesario):
   - Ve a "Configuración" → "Variables de entorno"
7. Configurar recursos:
   - **Memoria**: 3008 MB (recomendado)
   - **Timeout**: 5 minutos (300 segundos)
8. Configurar el handler:
   - El handler ya está configurado en el Dockerfile: `app.main.handler`

**Opción B: Desde Terminal (CLI)**

```bash
# Crear función Lambda
aws lambda create-function \
  --function-name coomeva-cluster-lambda \
  --package-type Image \
  --code ImageUri=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/coomeva-cluster-api:latest \
  --role arn:aws:iam::$AWS_ACCOUNT_ID:role/lambda-execution-role \
  --timeout 300 \
  --memory-size 3008 \
  --region $AWS_REGION

# Nota: Necesitas crear un IAM Role primero con permisos de ejecución Lambda
```

#### 1.5 Configurar API Gateway para Exponer Lambda

**Opción A: Desde la Consola Web**

1. Ve a API Gateway en la consola de AWS
2. Click en "Crear API"
3. Selecciona "REST API" → "Nuevo API"
4. Configura:
   - **Nombre**: `CoomevaClusterAPI`
   - **Tipo de endpoint**: Regional
5. Crear recurso y método:
   - Click en "Acciones" → "Crear recurso"
   - **Nombre del recurso**: `cluster`
   - Click en "Crear recurso"
   - Selecciona el recurso `/cluster` → "Acciones" → "Crear método" → `POST`
   - Selecciona "Función Lambda" como tipo de integración
   - Selecciona la función `coomeva-cluster-lambda`
   - Click en "Guardar"
6. Implementar API:
   - Click en "Acciones" → "Implementar API"
   - **Etapa de implementación**: `prod` (o crear nueva)
   - Click en "Implementar"
7. Copiar la URL del endpoint generado

**Opción B: Desde Terminal (CLI)**

```bash
# Crear API REST
API_ID=$(aws apigateway create-rest-api \
  --name "CoomevaClusterAPI" \
  --region $AWS_REGION \
  --query 'id' --output text)

# Crear recurso
RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --path-part cluster \
  --parent-id $(aws apigateway get-resources \
    --rest-api-id $API_ID \
    --query 'items[0].id' --output text) \
  --region $AWS_REGION \
  --query 'id' --output text)

# Crear método POST
aws apigateway put-method \
  --rest-api-id $API_ID \
  --resource-id $RESOURCE_ID \
  --http-method POST \
  --authorization-type NONE \
  --region $AWS_REGION

# Integrar con Lambda
aws apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $RESOURCE_ID \
  --http-method POST \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri arn:aws:apigateway:$AWS_REGION:lambda:path/2015-03-31/functions/arn:aws:lambda:$AWS_REGION:$AWS_ACCOUNT_ID:function:coomeva-cluster-lambda/invocations \
  --region $AWS_REGION

# Implementar API
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod \
  --region $AWS_REGION
```

#### 1.6 Actualizar Función Lambda (Re-despliegue)

Cuando hagas cambios en el código:

```bash
# 1. Reconstruir imagen
docker build -t coomeva-cluster-api:latest .

# 2. Re-etiquetar
docker tag coomeva-cluster-api:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/coomeva-cluster-api:latest

# 3. Subir nueva versión
docker push \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/coomeva-cluster-api:latest

# 4. Actualizar función Lambda
aws lambda update-function-code \
  --function-name coomeva-cluster-lambda \
  --image-uri $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/coomeva-cluster-api:latest \
  --region $AWS_REGION
```

#### 1.7 Pruebas Locales (Opcional)

```bash
# Ejecutar localmente con uvicorn
cd clusterizacion-coomeva
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Probar endpoint
curl -X POST "http://localhost:8000/api/v1/cluster" \
  -H "accept: application/json" \
  -F "file=@test_data.xlsx" \
  --output resultado.csv
```

---

### 2. Frontend (React + Vite)

#### 2.1 Requisitos Previos

- Node.js 18+ y npm (o yarn/pnpm)
- Cuenta de Supabase configurada

#### 2.2 Instalación

```bash
# 1. Navegar al directorio del frontend
cd coomeva-sales-hub

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
# Crear archivo .env.local en la raíz del proyecto
cat > .env.local << EOF
VITE_SUPABASE_URL=https://tu-proyecto.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=tu-anon-key-aqui
EOF
```

#### 2.3 Desarrollo Local

```bash
# Iniciar servidor de desarrollo
npm run dev

# La aplicación estará disponible en:
# http://localhost:8000
```

#### 2.4 Construcción para Producción

```bash
# Construir aplicación optimizada
npm run build

# Los archivos generados estarán en la carpeta dist/
```

#### 2.5 Opciones de Despliegue

Las siguientes son las opciones disponibles para desplegar el frontend:

- **Vercel**: Plataforma serverless para aplicaciones frontend
- **Netlify**: Hosting estático con CI/CD integrado
- **Render**: Plataforma cloud para aplicaciones web
- **AWS S3 + CloudFront**: Almacenamiento estático con CDN de AWS
- **Servidor Propio**: Cualquier servidor web (nginx, Apache, etc.) con la carpeta `dist/` construida

#### 2.6 Configuración de Webhook N8N

Actualizar la URL del webhook en los componentes:

**Archivo**: `coomeva-sales-hub/src/components/dashboard/ConsultCard.tsx`
```typescript
const WEBHOOK_URL = "https://tu-instancia-n8n.app.n8n.cloud/webhook-test/tu-webhook-id";
```

**Archivo**: `coomeva-sales-hub/src/components/dashboard/ClusterCard.tsx`
```typescript
const WEBHOOK_URL = "https://tu-instancia-n8n.app.n8n.cloud/webhook-test/tu-webhook-id";
```

---

### 3. Base de Datos

#### 3.1 Opciones de Base de Datos

Las siguientes son las opciones disponibles para la base de datos PostgreSQL:

- **Supabase**: Plataforma backend-as-a-service con PostgreSQL, autenticación y APIs REST
- **Neon**: Base de datos PostgreSQL serverless con branching
- **AWS RDS**: Servicio de base de datos relacional de Amazon Web Services

#### 3.2 Importar Esquema

Una vez configurada la base de datos, importa el esquema desde el archivo `coomeva_cluster_db_schema.sql` usando el método proporcionado por tu proveedor (SQL Editor, psql, o herramienta de administración).

#### 3.3 Configurar Permisos y Políticas RLS (Row Level Security)

Configura las políticas de seguridad según las capacidades de tu proveedor de base de datos. Para Supabase, habilita RLS y crea políticas para usuarios autenticados.

#### 3.4 Obtener Credenciales

Obtén las credenciales de conexión (URL, usuario, contraseña, keys) desde el dashboard de tu proveedor de base de datos.

---

### 4. Agente N8N

#### 4.1 Opciones de Despliegue de N8N

Las siguientes son las opciones disponibles para desplegar N8N:

- **N8N Cloud**: Servicio gestionado de N8N (recomendado para producción)
- **Self-hosting de N8N**: Instalación propia de N8N (Docker, npm, etc.)
- **Servidor Propio**: Instalación de N8N en servidor propio (VPS, EC2, etc.)

#### 4.2 Importar Flujo

1. En N8N, click en "Workflows" → "Import from File"
2. Selecciona el archivo `COOMEVA AGENTE - W FRONTEND.json`
3. Click en "Import"
4. El flujo se cargará con todos los nodos configurados

#### 4.3 Configurar Credenciales en N8N

**Supabase Credentials**:

1. En N8N, ve a "Credentials"
2. Click en "Add Credential"
3. Busca "HTTP Request" o "Supabase"
4. Configura:
   - **Name**: `Supabase Service Role`
   - **Authentication**: `Header Auth`
   - **Name**: `apikey`
   - **Value**: `<SERVICE_ROLE_SECRET>` (de Supabase)
   - **Additional Header**:
     - **Name**: `Authorization`
     - **Value**: `Bearer <SERVICE_ROLE_SECRET>`
     - **Name**: `Content-Type`
     - **Value**: `application/json`
     - **Name**: `Prefer`
     - **Value**: `return=minimal`

**Google Sheets Credentials**:

1. Ve a "Credentials" → "Add Credential"
2. Selecciona "Google Sheets"
3. Sigue el proceso de autenticación OAuth
4. Asegúrate de que el archivo `cluster_arquetipos_precisos_con_riesgo.xlsx` esté compartido con la cuenta autenticada

**Gemini API Key**:

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Genera una nueva API Key
3. En N8N, ve a "Credentials" → "Add Credential"
4. Selecciona "HTTP Request" o crea una credencial personalizada
5. Guarda la API Key como variable de entorno o en la credencial

**AWS Lambda Credentials**:

1. En N8N, ve a "Credentials" → "Add Credential"
2. Selecciona "AWS"
3. Configura:
   - **Access Key ID**: Tu AWS Access Key
   - **Secret Access Key**: Tu AWS Secret Key
   - **Region**: `us-east-1` (o tu región)

#### 4.4 Configurar Webhooks

1. En el workflow importado, busca el nodo "Webhook"
2. Click en el nodo para editarlo
3. Configura:
   - **HTTP Method**: `POST`
   - **Path**: `/webhook-test/e0d3199e-1b27-4ee7-8787-56f7e0ef680f` (o el que prefieras)
4. Activa el workflow (toggle en la esquina superior derecha)
5. Copia la URL del webhook (se muestra en el nodo)
6. Actualiza esta URL en el frontend (ver sección 2.6)

#### 4.5 Configurar Nodos del Flujo

**Nodo de Consulta de Cliente**:
- Verifica que apunte a la tabla `datos` en Supabase
- Configura la query SQL para buscar por `idunico`

**Nodo de Clusterización**:
- Verifica que invoque la función Lambda correcta
- Configura el nombre de la función: `coomeva-cluster-lambda`
- Verifica que el payload incluya el archivo correctamente

**Nodo de Gemini AI**:
- Verifica que use la API Key correcta
- Ajusta los prompts según necesidad

---

## Manual de Operación

### 1. Consultar Cliente por ID y Producto

**Descripción**: Permite buscar información de un cliente específico y obtener recomendaciones personalizadas.

**Pasos**:

1. Accede al frontend en la URL desplegada
2. Inicia sesión con tus credenciales de Supabase
3. En el dashboard, localiza la tarjeta "Consultar Cliente"
4. Ingresa:
   - **Número de cédula**: ID único del cliente (ej: `1234567890`)
   - **Producto**: Producto de interés (ej: `Crédito hipotecario`)
5. Click en "Consultar"
6. El sistema mostrará:
   - Arquetipo y perfil del cliente
   - Mensaje personalizado
   - Idea de valor
   - Canal de comunicación recomendado
   - Recomendación estratégica

**Flujo Técnico**:
```
Frontend → N8N Webhook → Supabase (consulta) → Gemini AI (generación) → Frontend
```

### 2. Clusterizar Nuevos Clientes

**Descripción**: Procesa un archivo con datos de nuevos clientes y los asigna a clusters.

**Pasos**:

1. Prepara un archivo CSV o XLSX con los datos de clientes
2. Asegúrate de que el archivo contenga al menos estas columnas:
   - `IdUnico`
   - `Ingresos`
   - `Saldo_aportes`
   - `Cuotas_canceladas_aportes`
   - `Cuotas_mora_aportes`
   - `Vlr_mora`
3. En el dashboard, localiza la tarjeta "Clusterizar Clientes"
4. Click en "Seleccionar archivo" y elige tu archivo
5. Click en "Subir y procesar"
6. Espera a que se complete el procesamiento (puede tomar varios minutos)
7. El sistema mostrará un mensaje de éxito cuando termine
8. Los resultados se almacenan automáticamente en Supabase

**Flujo Técnico**:
```
Frontend → N8N Webhook → AWS Lambda (clusterización) → Supabase (almacenamiento) → Frontend
```

**Notas Importantes**:
- El procesamiento puede tardar dependiendo del tamaño del archivo
- Archivos grandes (>10,000 registros) pueden requerir más tiempo
- Los clientes sin datos completos en columnas críticas serán eliminados del procesamiento

### 3. Buscar por Arquetipos

**Descripción**: Obtiene estrategias y recomendaciones para llegar a diferentes tipos de clientes (arquetipos).

**Pasos**:

1. En el dashboard, localiza la tarjeta "Buscar por Arquetipo"
2. Selecciona un producto de interés
3. Click en "Buscar"
4. El sistema mostrará:
   - Arquetipos relevantes para el producto
   - Estrategias de comunicación
   - Canales recomendados
   - Ideas de valor

**Flujo Técnico**:
```
Frontend → N8N Webhook → Supabase (consulta clusters) → Gemini AI (generación) → Frontend
```

---

## Manual de Funcionamiento Técnico

### Proceso de Clusterización

#### 1. Preprocesamiento de Datos

**Archivo**: `clusterizacion-coomeva/app/preprocessing.py`

**Proceso**:

1. **Limpieza Inicial**:
   - Elimina columnas redundantes
   - Elimina filas con valores nulos en columnas críticas
   - Preserva columnas con prefijo "Nombre_"

2. **Transformación de Variables**:
   - Calcula `log_ingresos` y `log_ingresos_deflactados` (si no existen)
   - Calcula `Antiguedad_dias` desde `Fecha_Ingreso`
   - Calcula `Edad` desde `Fecha_Nacimiento`
   - Mapea `Zona` a `Region` (Andina, Caribe, Pacífica, etc.)
   - Agrupa `Nombre_Titulo_Obtenido` en `Area_Titulo` (Salud, Tecnología, etc.)

3. **One-Hot Encoding**:
   - Convierte variables categóricas a formato numérico
   - Ejemplo: `Estado_Civil` → `Estado_Civil_Soltero`, `Estado_Civil_Casado`, etc.
   - Usa `drop_first=False` para mantener todas las columnas dummy

4. **Estandarización**:
   - Reindexa el DataFrame para tener exactamente 175 columnas
   - Rellena columnas faltantes con 0
   - Convierte todas las columnas numéricas a `float64`

**Salida**: DataFrame con 175 columnas numéricas listo para el modelo

#### 2. Reducción de Dimensionalidad (UMAP)

**Archivo**: `clusterizacion-coomeva/app/prediction.py`

**Proceso**:

1. **Escalado**:
   - Aplica `StandardScaler` para normalizar features (media=0, std=1)

2. **Aproximación UMAP**:
   - **IMPORTANTE**: No usa `umap.transform()` directamente
   - En su lugar, usa interpolación KNN sobre embeddings pre-calculados:
     - Encuentra k vecinos más cercanos en el espacio original
     - Obtiene las coordenadas UMAP de esos vecinos
     - Calcula posición como promedio ponderado por distancia inversa
   - Reduce de 175 dimensiones a 2 dimensiones (UMAP_1, UMAP_2)

**Razón de la Aproximación**:
- El modelo UMAP completo es muy pesado para Lambda
- La aproximación es más ligera y rápida
- Precisión: ~85-95% comparado con el modelo original

#### 3. Clusterización (KMeans)

**Proceso**:

1. **Predicción**:
   - Aplica el modelo KMeans entrenado sobre las coordenadas UMAP
   - Asigna cada cliente al cluster más cercano

2. **Resultado**:
   - Array de labels (0, 1, 2, 3, 4, ...)
   - Cada label representa un cluster diferente

#### 4. Generación de Resultado

**Archivo**: `clusterizacion-coomeva/app/routes/clustering.py`

**Proceso**:

1. **Combinación**:
   - Combina datos originales con columna `Cluster`
   - Filtra solo las filas válidas (sin nulos)

2. **Conversión de Tipos**:
   - Columnas one-hot: `float64` → `bool`
   - Fechas: `datetime` → `string` (YYYY-MM-DD)
   - `IdUnico` y `Cluster`: `string`
   - Columnas monetarias: `int` (bigint para Supabase)

3. **Normalización de Nombres**:
   - Convierte a minúsculas
   - Reemplaza espacios y caracteres especiales por guiones bajos
   - Elimina acentos

4. **Exportación**:
   - Genera archivo CSV en memoria
   - Retorna como respuesta HTTP para descarga

### Modelos Entrenados

Los modelos se encuentran en `clusterizacion-coomeva/models/`:

- **scaler_model.pkl**: StandardScaler entrenado con datos históricos
- **kmeans_model.pkl**: Modelo KMeans con n clusters
- **umap_data.pkl**: Diccionario con:
  - `embeddings`: Coordenadas UMAP del conjunto de entrenamiento
  - `knn_index`: Índice KNN para búsqueda rápida
  - `feature_names`: Lista de nombres de features esperados

**Nota**: Estos modelos deben ser entrenados previamente usando los notebooks de análisis.

---

## Notebooks de Análisis

### 1. Nueva_Clusterizacion(UMAP+Kmeans).ipynb

**Descripción**: Notebook principal que contiene el proceso completo de clusterización.

**Contenido**:
- Carga y exploración de datos
- Preprocesamiento completo
- Entrenamiento de modelos (UMAP + KMeans)
- Evaluación de clusters
- Guardado de modelos entrenados

**Uso**:
1. Abre el notebook en Jupyter Lab o Google Colab
2. Ejecuta todas las celdas en orden
3. Los modelos entrenados se guardarán en la carpeta `models/`
4. Copia estos modelos a `clusterizacion-coomeva/models/` para usar en producción

### 2. Analisis-Exploratorio-2.ipynb

**Descripción**: Análisis exploratorio de datos (EDA).

**Contenido**:
- Estadísticas descriptivas
- Visualizaciones de distribuciones
- Análisis de correlaciones
- Identificación de outliers
- Preparación de datos para modelado

---

## Configuración de Servicios Externos

### Supabase

#### Configuración de Headers para N8N

Para cualquier operación sobre la base de datos desde N8N, usa estos headers:

```json
{
  "apikey": "<SERVICE_ROLE_SECRET>",
  "Authorization": "Bearer <SERVICE_ROLE_SECRET>",
  "Content-Type": "application/json",
  "Prefer": "return=minimal"
}
```

**Ejemplo de Inserción en N8N**:

1. Nodo: **HTTP Request**
2. Método: `POST`
3. URL: `https://<HOST>.supabase.co/rest/v1/datos`
4. Headers: Como se muestra arriba
5. Body: JSON con los datos a insertar

**Ejemplo de Consulta en N8N**:

1. Nodo: **HTTP Request**
2. Método: `GET`
3. URL: `https://<HOST>.supabase.co/rest/v1/datos?idunico=eq.1234567890`
4. Headers: Como se muestra arriba

**Troubleshooting**:
- Error 401/403: Verifica que el Service Role Secret sea correcto
- Error de formato: Ajusta `Content-Type` a `text/csv` si envías CSV
- Error de permisos: Verifica las políticas RLS en Supabase

### Google Sheets

#### Configuración

1. Asegúrate de tener el archivo `cluster_arquetipos_precisos_con_riesgo.xlsx` en Google Drive
2. Comparte el archivo con la cuenta autenticada en N8N (permiso de lectura)
3. En N8N, crea una credencial de Google Sheets
4. Selecciona la cuenta correcta
5. En los flujos, selecciona el archivo por nombre exacto

**Troubleshooting**:
- Archivo no aparece: Verifica permisos y que el nombre sea exacto
- Credencial falla: Reautentica la cuenta en N8N

### Gemini API

#### Configuración

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Click en "Create API Key"
4. Copia la API Key generada
5. En N8N, configura la API Key en el nodo Gemini o como variable de entorno

**Troubleshooting**:
- API Key no funciona: Verifica que esté activa y asociada a tu cuenta
- Límite de cuota: Verifica los límites de uso en Google AI Studio

### AWS Lambda

#### Configuración de Invocación desde N8N

1. En N8N, usa el nodo "AWS Lambda"
2. Configura:
   - **Function Name**: `coomeva-cluster-lambda`
   - **Region**: `us-east-1` (o tu región)
   - **Payload**: JSON con el archivo en base64 o URL de S3

**Ejemplo de Payload**:

```json
{
  "body": "<base64-encoded-file>",
  "headers": {
    "Content-Type": "multipart/form-data"
  }
}
```

**Troubleshooting**:
- Timeout: Aumenta el timeout en la configuración de Lambda
- Memoria insuficiente: Aumenta la memoria asignada (máx 10GB)
- Error de formato: Verifica que el payload esté en el formato correcto

---

## Troubleshooting

### Problemas Comunes

#### 1. Error en Clusterización: "Faltan columnas esperadas"

**Síntoma**: La API retorna error indicando que faltan columnas.

**Solución**:
- Verifica que el archivo de entrada tenga todas las columnas requeridas
- Revisa los logs de Lambda en CloudWatch para ver qué columnas faltan
- Asegúrate de que el preprocesamiento esté generando todas las columnas necesarias

#### 2. Error 401/403 en Supabase desde N8N

**Síntoma**: Las consultas a Supabase fallan con error de autenticación.

**Solución**:
- Verifica que estés usando el `SERVICE_ROLE_SECRET` y no el `anon key`
- Asegúrate de que los headers estén configurados correctamente
- Verifica que las políticas RLS permitan las operaciones necesarias

#### 3. Lambda Timeout

**Síntoma**: La función Lambda se detiene antes de completar.

**Solución**:
- Aumenta el timeout en la configuración de Lambda (máx 15 minutos)
- Reduce el tamaño del archivo o procesa en lotes más pequeños
- Aumenta la memoria asignada (puede mejorar el rendimiento)

#### 4. Frontend no se conecta a N8N

**Síntoma**: Las peticiones desde el frontend fallan.

**Solución**:
- Verifica que la URL del webhook sea correcta
- Asegúrate de que el workflow de N8N esté activo
- Verifica los logs de N8N para ver errores
- Revisa CORS si estás en desarrollo local

#### 5. Modelos no se cargan en Lambda

**Síntoma**: Error al cargar modelos desde la carpeta `models/`.

**Solución**:
- Verifica que los archivos `.pkl` estén en la carpeta `models/` del contenedor
- Revisa que el Dockerfile copie la carpeta `models/` correctamente
- Verifica los permisos de lectura de los archivos

#### 6. Precisión de Clusters Diferente al Notebook

**Síntoma**: Los clusters asignados no coinciden exactamente con el notebook.

**Solución**:
- Esto es esperado debido a la aproximación UMAP
- La precisión esperada es 85-95%
- Para mayor precisión, considera usar un servidor siempre activo (EC2/ECS)

### Logs y Monitoreo

#### CloudWatch Logs (Lambda)

```bash
# Ver logs en tiempo real
aws logs tail /aws/lambda/coomeva-cluster-lambda --follow

# Buscar errores
aws logs filter-pattern /aws/lambda/coomeva-cluster-lambda "ERROR"

# Ver logs de las últimas 24 horas
aws logs tail /aws/lambda/coomeva-cluster-lambda --since 24h
```

#### N8N Logs

- En N8N Cloud: Ve a "Executions" para ver logs de cada ejecución
- En auto-hospedado: Revisa los logs de Docker o del proceso

#### Supabase Logs

- Ve a "Logs" → "Postgres Logs" en el dashboard de Supabase
- Revisa "API Logs" para ver las peticiones HTTP

---

## Recomendaciones de Seguridad

### Credenciales y Secretos

1. **Nunca compartas el Service Role Secret**:
   - Solo úsalo en backend o N8N
   - Nunca lo expongas en el frontend
   - Rótalo periódicamente

2. **API Keys**:
   - Mantén las API Keys en entornos seguros
   - Usa variables de entorno, no hardcodees valores
   - Rótalas periódicamente

3. **AWS Credentials**:
   - Usa IAM Roles cuando sea posible
   - Limita los permisos al mínimo necesario
   - No compartas Access Keys

### Base de Datos

1. **Row Level Security (RLS)**:
   - Habilita RLS en todas las tablas
   - Define políticas restrictivas
   - Revisa periódicamente las políticas

2. **Backups**:
   - Configura backups automáticos en Supabase
   - Prueba restauraciones periódicamente

### Infraestructura

1. **CORS**:
   - Limita los orígenes permitidos en producción
   - No uses `allow_origins=["*"]` en producción

2. **Rate Limiting**:
   - Implementa rate limiting en API Gateway
   - Protege contra abuso

3. **Monitoreo**:
   - Configura alertas en CloudWatch
   - Monitorea intentos de acceso no autorizados

---

## Videos Tutoriales

- [Video Agente N8N disparado por un formulario](https://youtu.be/MrhYheFAB_w)
- [Video Agente N8N integrado con frontend](https://youtu.be/VKbyi4FUpF4)

---

## Contacto y Soporte

Para preguntas, problemas o sugerencias:
1. Revisa esta documentación primero
2. Consulta los logs de los servicios
3. Contacta al equipo de desarrollo

---

**Última actualización**: Diciembre 2024  
**Versión**: 1.0.0  
**Mantenido por**: Equipo de Data Science - Coomeva
