# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim AS production

# Security: run as non-root
RUN groupadd -r hummingbird && useradd -r -g hummingbird hummingbird

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies
COPY --from=builder /install /usr/local

# Create app directories
RUN mkdir -p /app/data/chroma_db /app/data/medical_knowledge /app/logs \
    && chown -R hummingbird:hummingbird /app

WORKDIR /app

# Copy application code
COPY --chown=hummingbird:hummingbird . .

# Switch to non-root user
USER hummingbird

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
# v23 - updated 2026-06-11
