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
