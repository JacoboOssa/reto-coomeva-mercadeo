# Imagen base de AWS Lambda para Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Instalar dependencias de compilación necesarias
RUN yum install -y gcc gcc-c++ make && yum clean all

# Copiar requirements e instalar dependencias
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Configurar variables de entorno para Numba y Joblib
ENV NUMBA_DISABLE_JIT=1
ENV NUMBA_CACHE_DIR=/tmp
ENV NUMBA_DISABLE_CACHING=1
ENV JOBLIB_TEMP_FOLDER=/tmp

# Copiar el código y los modelos
COPY . .

# Indica el handler que Lambda ejecutará
CMD ["app.main.handler"]
