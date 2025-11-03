FROM python:3.13-slim

WORKDIR /app

# Install system dependencies (required for llama-cpp-python)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download TinyLLaMA model (GGUF format - optimized for CPU)
RUN pip install huggingface-hub && \
    python -c "from huggingface_hub import hf_hub_download; \
    hf_hub_download('TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF', \
    'tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf', \
    local_dir='/app/models')"

# Copy MCP server
COPY mcp_server.py .

EXPOSE 8001

CMD ["python", "mcp_server.py"]