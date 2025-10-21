# ---------- Dockerfile ----------
# Base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# We DO NOT copy the source code here.
# It will be mounted from the host when running the container.

EXPOSE 8000

# Default command: run your server script
CMD ["python", "main_rest_api.py"]
# --------------------------------
# kahoot-db/Dockerfile
FROM postgres:15

# Set environment variables (can also be done in docker-compose)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=kahootdb

# Optionally copy initialization SQL scripts
# (they run automatically when the container starts)
# COPY init.sql /docker-entrypoint-initdb.d/
