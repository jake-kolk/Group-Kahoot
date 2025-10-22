# ---------- Dockerfile ----------
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files into the container
COPY . .

EXPOSE 8080

# Default command: run your server script
CMD ["python", "logic.py"]
# --------------------------------
