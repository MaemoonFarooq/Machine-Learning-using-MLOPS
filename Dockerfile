# syntax=docker/dockerfile:1

FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV AIRFLOW_HOME=/app/airflow

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p WeatherData PreprocessedWeatherData models mlruns

# Initialize Airflow database
RUN airflow db init

# Create Airflow admin user
RUN airflow users create \
    --username admin \
    --password admin \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email admin@example.com

# Expose ports for Airflow and MLflow
EXPOSE 8080 5000

# Create startup script
RUN echo '#!/bin/bash\n\
airflow webserver --port 8080 -D\n\
airflow scheduler -D\n\
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000\n\
tail -f /dev/null' > /app/start.sh && chmod +x /app/start.sh

# Set the entrypoint
ENTRYPOINT ["/app/start.sh"]