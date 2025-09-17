# Stage 1: build
FROM debian:stable-slim AS builder

RUN apt-get update && apt-get install -y \
    g++ cmake make libboost-all-dev nlohmann-json3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Build the server (use separate build dir)
RUN mkdir build && cd build && cmake .. && make -j$(nproc)

# Stage 2: runtime
FROM debian:stable-slim
WORKDIR /app

# Install runtime dependencies (Boost libs etc.)
RUN apt-get update && apt-get install -y \
    libboost-system-dev libboost-thread-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy built binary
COPY --from=builder /app/build/kahoot_server /app/kahoot_server

EXPOSE 8080
CMD ["./kahoot_server"]
