FROM python:3.11-slim

# 1. Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variables de entorno
ENV DB_USER=latam_user
ENV DB_PASS=latam_pass
ENV DB_NAME=latamdb
ENV CLOUD_SQL_CONNECTION_NAME=latamchallenge-487721:us-central1:latam-user-db

EXPOSE 8080

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
