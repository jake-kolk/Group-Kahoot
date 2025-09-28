# ---------- Dockerfile ----------
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# We DO NOT copy the source code here.
# It will be mounted from the host when running the container.

# Default command: run your server script
CMD ["python", "kahoot_server.py"]
# --------------------------------
