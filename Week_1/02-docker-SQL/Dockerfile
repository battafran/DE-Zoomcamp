FROM python:3.9

# Instalar dependencias necesarias
RUN apt-get update && apt-get clean

# Instalar librerías de Python necesarias
RUN pip install pandas sqlalchemy psycopg2 requests

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el script Python al contenedor
COPY ingest_data.py ingest_data.py

# Definir el punto de entrada del contenedor
ENTRYPOINT ["python", "ingest_data.py"]