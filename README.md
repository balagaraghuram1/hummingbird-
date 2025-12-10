<div align="center">

# Hummingbird Medical AI

**Production-ready medical AI system for clinical decision support**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://langchain.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

</div>

---

## Overview

Hummingbird is a medical AI assistant designed for healthcare professionals and developers building clinical decision support systems. It leverages large language models (GPT-4, Claude, Gemini) with LangChain for structured medical analysis, including symptom-to-diagnosis mapping, treatment plan generation, and laboratory result interpretation.

The system is built with production requirements in mind: type-safe APIs, comprehensive error handling, caching, monitoring, and containerized deployment.

**Disclaimer**: This system is intended for research and educational purposes only. It does not provide medical advice and should not be used as a substitute for professional medical judgment.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Applications                     │
│                   (Web, Mobile, Third-party)                 │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS
┌──────────────────────────────▼──────────────────────────────┐
│                        API Gateway                          │
│              FastAPI + CORS + Rate Limiting                 │
│                  + Request Validation                       │
└──────┬───────────────┬───────────────────┬──────────────────┘
       │               │                   │
┌──────▼──────┐ ┌──────▼──────┐ ┌─────────▼─────────┐
│  Diagnosis  │ │  Treatment  │ │   Lab Analysis    │
│    Agent    │ │    Agent    │ │      Agent        │
└──────┬──────┘ └──────┬──────┘ └─────────┬─────────┘
       │               │                   │
┌──────▼───────────────▼───────────────────▼──────────────────┐
│                    LangChain Orchestration                  │
│              (LLM Chains + Prompt Engineering)              │
└──────┬──────────────────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────────────┐
│                   External AI Providers                     │
│              OpenAI (GPT-4) | Anthropic (Claude)            │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

### Core Capabilities

- **Symptom-to-Diagnosis**: Multi-differential diagnosis from patient-reported symptoms
- **Treatment Planning**: Evidence-based treatment recommendations with medication guidance
- **Lab Analysis**: Automated interpretation of laboratory results with reference range checking
- **Knowledge Retrieval**: Vector-based medical knowledge search via ChromaDB

### Production Infrastructure

- **JWT Authentication**: Secure API access with token-based authentication
- **Redis Caching**: Response caching for improved performance and reduced API costs
- **Prometheus Metrics**: Real-time monitoring of API performance and AI model usage
- **Grafana Dashboards**: Visual monitoring of system health and performance
- **Structured Logging**: JSON-formatted logs with request tracing

### Developer Experience

- **Type-Safe APIs**: Full Pydantic v2 model validation
- **Comprehensive Tests**: Unit and integration test suite
- **Docker Support**: Multi-stage builds with non-root containers
- **Environment Configuration**: `.env`-based configuration management

---

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for production)
- OpenAI API key (or Anthropic API key)

### Local Development

```bash
# Clone the repository
git clone https://github.com/balagaraghuram1/hummingbird-.git
cd hummingbird-

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the application
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment

```bash
# Set environment variables
export OPENAI_API_KEY=your_key_here
export SECRET_KEY=$(openssl rand -base64 32)
export POSTGRES_PASSWORD=$(openssl rand -base64 16)

# Start all services
docker compose up -d

# View logs
docker compose logs -f app

# Stop services
docker compose down
```

### API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc` (debug mode only)

---

## API Reference

### Health Check

```http
GET /api/health
```

Response:
```json
{
  "status": "ok",
  "service": "hummingbird-medical-ai",
  "version": "1.0.0",
  "ai_model": "available",
  "cache": "available"
}
```

### Diagnosis

```http
POST /api/diagnose
Content-Type: application/json

{
  "symptoms": ["fever", "cough", "fatigue"],
  "patient_age": 35,
  "patient_sex": "male"
}
```

Response:
```json
{
  "diagnosis": "Upper respiratory infection...",
  "confidence": 0.85,
  "recommendations": ["Rest", "Hydration", "Monitor symptoms"],
  "warning": "This is AI-generated analysis..."
}
```

### Treatment Plan

```http
POST /api/treatment-plan
Content-Type: application/json

{
  "diagnosis": "Upper respiratory infection",
  "patient_age": 35,
  "allergies": ["penicillin"]
}
```

### Lab Analysis

```http
POST /api/analyze-lab
Content-Type: application/json

{
  "results": {
    "hemoglobin": 14.2,
    "glucose": 95,
    "cholesterol_total": 180,
    "white_blood_cells": 7.5
  }
}
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | OpenAI API key for GPT models |
| `ANTHROPIC_API_KEY` | - | Anthropic API key for Claude models |
| `DATABASE_URL` | `sqlite:///./hummingbird.db` | Database connection URL |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection URL |
| `SECRET_KEY` | (auto-generated) | JWT signing secret |
| `MODEL_NAME` | `gpt-4o` | Primary LLM model |
| `MODEL_TEMPERATURE` | `0.2` | LLM temperature (0-2) |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |

### Model Configuration

The system supports multiple LLM providers. Configure via environment variables:

```bash
# Use OpenAI
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o

# Use Anthropic (via LangChain)
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── conftest.py          # Shared fixtures
├── test_api.py          # API endpoint tests
├── test_services.py     # Service layer tests
└── test_agents.py       # Agent tests
```

---

## Monitoring

### Prometheus Metrics

Access metrics at `http://localhost:9090/metrics` (Docker) or `http://localhost:8000/metrics` (local).

Key metrics:
- `hummingbird_requests_total` - Total API requests
- `hummingbird_request_latency_seconds` - Request latency histogram
- `hummingbird_ai_requests_total` - AI model requests
- `hummingbird_cache_hits_total` - Cache hit count

### Grafana Dashboard

1. Access Grafana at `http://localhost:3001`
2. Login with admin credentials
3. Import dashboard from `monitoring/grafana/dashboards/medical_ai.json`

---

## Project Structure

```
hummingbird/
├── src/
│   ├── api/                    # API routes and middleware
│   │   ├── main.py            # Route definitions
│   │   ├── middleware.py       # Request processing
│   │   └── dependencies.py    # Dependency injection
│   ├── agents/                 # AI agents
│   │   ├── diagnosis_agent.py
│   │   ├── treatment_agent.py
│   │   └── lab_agent.py
│   ├── config/                 # Configuration
│   │   ├── settings.py
│   │   ├── database.py
│   │   └── security.py
│   ├── core/                   # Core utilities
│   │   ├── events.py
│   │   └── exceptions.py
│   ├── medical_ai/             # AI model
│   │   └── model.py
│   ├── models/                 # Data models
│   │   ├── schemas.py
│   │   └── database.py
│   ├── services/               # Business logic
│   │   ├── medical_service.py
│   │   ├── cache_service.py
│   │   ├── vector_service.py
│   │   └── auth_service.py
│   ├── utils/                  # Utilities
│   │   ├── logger.py
│   │   ├── monitoring.py
│   │   └── helpers.py
│   └── main.py                 # App factory
├── tests/                      # Test suite
├── data/                       # Medical knowledge base
├── docs/                       # Documentation
├── monitoring/                 # Prometheus/Grafana config
├── scripts/                    # Deployment scripts
├── Dockerfile                  # Multi-stage build
├── docker-compose.yml          # Service orchestration
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## Security Considerations

- **Never commit secrets**: `.env` files are excluded from version control
- **Use environment variables**: All sensitive configuration via env vars
- **Non-root containers**: Docker runs as unprivileged user
- **Input validation**: All API inputs validated via Pydantic
- **Rate limiting**: Configurable per-minute request limits
- **CORS**: Configurable cross-origin resource sharing

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run linting
flake8 src/ tests/
black src/ tests/ --check
mypy src/
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [OpenAI](https://openai.com) for GPT models
- [Anthropic](https://anthropic.com) for Claude models
- [LangChain](https://langchain.com) for the AI orchestration framework
- [FastAPI](https://fastapi.tiangolo.com) for the web framework
- [Pydantic](https://docs.pydantic.dev) for data validation

---

<div align="center">

**Built with care for the medical AI community**

</div>
