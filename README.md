# Reto Mercadeo Coomeva

## Índice
1. [Descripción General](#descripción-general)
2. [Arquitectura y Componentes](#arquitectura-y-componentes)
3. [Manual de Operación](#manual-de-operación)
4. [Manual de Despliegue](#manual-de-despliegue)
   - Backend de Clusterización
   - Frontend
   - Base de Datos
   - Agente N8N
   - Configuración de Credenciales y Servicios Externos
5. [Recomendaciones de Seguridad](#recomendaciones-de-seguridad)
6. [Videos Tutoriales](#videos-tutoriales)

---

## Descripción General

Solución integral para la segmentación y análisis avanzado de clientes en Coomeva. El sistema combina procesamiento de datos, clusterización y visualización, todo orquestado por flujos automatizados en N8N y desplegado sobre infraestructura serverless para máxima eficiencia y mínimo costo.

---

## Arquitectura y Componentes

### 1. Frontend (`/coomeva-sales-hub`)
- Stack: Next.js + Supabase
- Permite consultar clientes, arquetipos y clusters, y visualizar resultados de segmentación.

### 2. Backend de Clusterización (`/clusterizacion-coomeva`)
- API desarrollada en FastAPI, expuesta vía AWS Lambda usando Docker.
- Funcionalidades principales:
  - Preprocesamiento de datos: Limpieza, transformación de variables categóricas y creación de features derivados.
  - Reducción de dimensionalidad: UMAP para condensar más de 170 variables en solo 2 dimensiones.
  - Clusterización: Algoritmo KMeans para agrupar clientes en segmentos significativos y accionables.

### 3. Infraestructura Serverless
- Dockerfile optimizado para AWS Lambda:
  - Sin costos cuando no se usa
  - Escalado automático
  - Ideal para ejecuciones periódicas (cada 3 meses)
  - Mantenimiento mínimo
- Imagen desplegada en AWS ECR, utilizada por Lambda y expuesta mediante API Gateway.

### 4. Agente N8N (`COOMEVA AGENTE - W FRONTEND.json`)
- Orquestador de flujos automatizados:
  - Consulta de cliente por ID y producto
  - Clusterización de nuevos clientes (invoca Lambda)
  - Sugerencias de arquetipos y estrategias para productos/clientes

### 5. Base de Datos (Supabase)
- Backend centralizado para almacenamiento y consulta de resultados, con esquema definido en `coomeva_cluster_db_schema.sql`.

---

## Manual de Operación

### 1. Consultar Cliente por ID y Producto
1. Accede al frontend.
2. Ingresa el ID del cliente y el producto.
3. El agente N8N consulta la base de datos y retorna la información relevante.

### 2. Clusterizar Nuevos Clientes
1. Sube los datos de nuevos clientes desde el frontend.
2. El agente N8N llama al endpoint AWS Lambda, que:
   - Preprocesa los datos.
   - Reduce la dimensionalidad.
   - Realiza la clusterización.
3. Los resultados se almacenan en Supabase y se muestran en el frontend.

### 3. Buscar por Arquetipos
1. Selecciona un producto en el frontend.
2. El agente N8N sugiere ideas para llegar a diferentes arquetipos o tipos de clientes, basándose en los clusters y perfiles generados.

---

## Manual de Despliegue

### 1. Backend de Clusterización (FastAPI + Docker + AWS Lambda)
#### 1.1 Construcción y subida de imagen Docker a AWS ECR
1. Autentícate en AWS:
   ```zsh
   aws configure
   ```
2. Crea un repositorio ECR:
   ```zsh
   aws ecr create-repository --repository-name coomeva-cluster-api
   ```
3. Obtén el login de Docker para ECR:
   ```zsh
   aws ecr get-login-password | docker login --username AWS --password-stdin <tu-id-de-cuenta>.dkr.ecr.<region>.amazonaws.com
   ```
4. Construye la imagen:
   ```zsh
   cd clusterizacion-coomeva
   docker build -t coomeva-cluster-api .
   ```
5. Etiqueta la imagen:
   ```zsh
   docker tag coomeva-cluster-api:latest <tu-id-de-cuenta>.dkr.ecr.<region>.amazonaws.com/coomeva-cluster-api:latest
   ```
6. Sube la imagen:
   ```zsh
   docker push <tu-id-de-cuenta>.dkr.ecr.<region>.amazonaws.com/coomeva-cluster-api:latest
   ```

#### 1.2 Crear función Lambda desde imagen ECR
**Desde la consola web (UI):**
1. Ve a AWS Lambda > Crear función > "Desde imagen de contenedor".
2. Selecciona el repositorio ECR y la imagen subida.
3. Configura memoria, timeout y variables de entorno según necesidad.
4. Crea la función.

**Desde terminal:**
```zsh
aws lambda create-function \
  --function-name coomeva-cluster-lambda \
  --package-type Image \
  --code ImageUri=<tu-id-de-cuenta>.dkr.ecr.<region>.amazonaws.com/coomeva-cluster-api:latest \
  --role <arn-del-role-lambda>
```

#### 1.3 Configurar API Gateway para exponer Lambda
**Desde la consola web (UI):**
1. Ve a API Gateway > Crear API > REST API o HTTP API.
2. Crea un recurso y método (POST/GET) que apunte a la función Lambda.
3. Implementa y copia el endpoint generado.

**Desde terminal:**
```zsh
aws apigateway create-rest-api --name "CoomevaClusterAPI"
# (Luego crea recursos, métodos y vincula la función Lambda)
```

---

### 2. Frontend (Next.js + Supabase)
1. Instala dependencias:
   ```zsh
   cd coomeva-sales-hub
   npm install
   ```
2. Configura las variables de entorno de Supabase (`.env.local`).
3. Inicia el servidor de desarrollo:
   ```zsh
   npm run dev
   ```

---

### 3. Base de Datos (Supabase)
1. Crea el proyecto en Supabase.
2. Importa el esquema desde `coomeva_cluster_db_schema.sql`.

---

### 4. Agente N8N
1. Importa el flujo desde `COOMEVA AGENTE - W FRONTEND.json` en tu instancia de N8N.
2. Configura las credenciales y endpoints necesarios.

#### 4.1 Configuración de Credenciales y Servicios Externos

**Supabase**
- Accede a Supabase y selecciona tu proyecto.
- Ve a `Project Settings > API`.
  - Host: Copia la URL (ejemplo: `https://xxxx.supabase.co`).
  - Service Role Secret: Copia el valor de `service_role`. Este es confidencial y solo debe usarse en backend o N8N.
- En N8N, crea una credencial HTTP y usa los siguientes headers para cualquier operación sobre la base de datos:
  ```json
  {
    "apikey": "<SERVICE_ROLE_SECRET>",
    "Authorization": "Bearer <SERVICE_ROLE_SECRET>",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
  }
  ```
- Ejemplo visual en N8N:
  - Nodo: HTTP Request
  - Método: POST
  - URL: `https://<HOST>.supabase.co/rest/v1/<tabla>`
  - Headers: como el ejemplo anterior
  - Body: JSON con los datos a insertar
**Troubleshooting:**
- Si recibes error 401/403, revisa que el Service Role Secret sea correcto y que la tabla tenga permisos de inserción.
- Si el formato de datos es incorrecto, ajusta el Content-Type a `text/csv` si envías CSV.

**Google Sheets**
- En tu Google Drive, asegúrate de tener el archivo `cluster_arquetipos_precisos_con__riesgo`.
- Comparte el archivo con la cuenta autenticada en N8N (permiso de lectura).
- En N8N, crea una credencial de Google Sheets y selecciona la cuenta.
- En los flujos, selecciona el archivo por nombre exacto.
**Troubleshooting:**
- Si el archivo no aparece, revisa permisos y que el nombre sea exacto.
- Si la credencial falla, reautentica la cuenta en N8N.

**Gemini API Key**
- Accede a Google AI Studio con tu cuenta.
- Ve a API Keys y genera una nueva clave.
- Copia el valor y configúralo en N8N como credencial HTTP o en el nodo Gemini.
**Troubleshooting:**
- Si la API Key no funciona, verifica que esté activa y asociada a tu cuenta.

**Ejemplo de Inserción de Registros en Supabase vía HTTP Request**
- Headers recomendados:
  ```json
  {
    "apikey": "<SERVICE_ROLE_SECRET>",
    "Authorization": "Bearer <SERVICE_ROLE_SECRET>",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
  }
  ```
- Usa el mismo valor para `apikey` y `Authorization` (Service Role Secret).
- Ajusta `Content-Type` según el formato de datos.
- `Prefer` optimiza la respuesta y es recomendable.
- Ejemplo visual en N8N:
  - Nodo: HTTP Request
  - Método: POST
  - URL: `https://<HOST>.supabase.co/rest/v1/<tabla>`
  - Headers: como el ejemplo anterior
  - Body: JSON o CSV según corresponda
**Troubleshooting:**
- Si la inserción falla, revisa los permisos de la tabla y el formato del body.

---

## Recomendaciones de Seguridad
- Nunca compartas el Service Role Secret en canales públicos ni lo expongas en frontend.
- Limita el acceso a los archivos de Google Sheets solo a cuentas necesarias.
- Mantén las API Keys en entornos seguros y rotalas periódicamente.
- Documenta cualquier cambio en credenciales y notifica al responsable de despliegue.

---

## Videos Tutoriales
Agrega aquí los links a los videos explicativos:
- [Video Agente N8N disparado por un formulario](https://youtu.be/MrhYheFAB_w)
- [Video Agente N8N integrado con frontend](#)


---