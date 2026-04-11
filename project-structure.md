# Hummingbird Medical AI - Project Structure & Dependencies

## Project Architecture Overview

A production-ready medical AI system with vector databases, caching, monitoring, and advanced AI capabilities.

## Directory Structure

```
hummingbird/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py         # Application configuration
│   │   ├── database.py         # Database configuration
│   │   └── security.py         # Security and auth configuration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py             # API routes
│   │   ├── dependencies.py     # API dependencies
│   │   └── middleware.py       # API middleware
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication service
│   │   ├── medical_service.py  # Medical AI service
│   │   ├── vector_service.py   # Vector database service
│   │   └── cache_service.py    # Redis caching service
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── diagnosis_agent.py  # Medical diagnosis agent
│   │   ├── treatment_agent.py  # Treatment recommendation agent
│   │   └── lab_agent.py       # Lab analysis agent
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic models
│   │   └── database.py         # Database models
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py           # Logging configuration
│   │   ├── monitoring.py       # Monitoring utilities
│   │   └── helpers.py          # Helper functions
│   └── core/
│       ├── __init__.py
│       ├── exceptions.py       # Custom exceptions
│       └── events.py           # Event handlers
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_services.py
│   ├── test_agents.py
│   └── conftest.py
├── data/
│   ├── medical_knowledge/
│   │   ├── diseases.json
│   │   ├── treatments.json
│   │   └── symptoms.json
│   └── embeddings/
│       └── medical_embeddings.json
├── scripts/
│   ├── setup.sh
│   ├── migrate.sh
│   └── test.sh
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
├── monitoring/
│   ├── prometheus.yml
│   └ grafana/
│       ├── dashboards/
│       └   └ medical_ai.json
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── DEVELOPMENT.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Core Dependencies

### AI and ML Stack
- **OpenAI**: `openai>=1.30.0` - GPT-4 integration
- **Anthropic**: `anthropic>=0.8.0` - Claude integration
- **LangChain**: `langchain>=0.1.0` - AI orchestration framework
- **Vector DB**: `chromadb>=0.4.0` - Vector database for medical knowledge

### Caching and Performance
- **Redis**: `redis>=5.0.0` - In-memory caching
- **Cachetools**: `cachetools>=5.3.0` - Python caching utilities

### Database and Storage
- **SQLAlchemy**: `sqlalchemy>=2.0.0` - ORM for PostgreSQL
- **PostgreSQL**: `psycopg2-binary>=2.9.0` - PostgreSQL driver

### Web Framework
- **FastAPI**: `fastapi>=0.104.0` - Modern web framework
- **Uvicorn**: `uvicorn>=0.24.0` - ASGI server
- **Pydantic**: `pydantic>=2.5.0` - Data validation

### Security
- **JWT**: `python-jose[cryptography]>=3.3.0` - JWT tokens
- **Passlib**: `passlib[bcrypt]>=1.7.4` - Password hashing

### Monitoring and Logging
- **Prometheus**: `prometheus-client>=0.19.0` - Metrics collection
- **Structlog**: `structlog>=23.2.0` - Structured logging

### Testing
- **Pytest**: `pytest>=7.4.0` - Testing framework
- **HTTPX**: `httpx>=0.25.0` - HTTP client for testing

### Data Processing
- **Pandas**: `pandas>=2.1.0` - Data manipulation
- **Scikit-learn**: `scikit-learn>=1.3.0` - Machine learning utilities

## Configuration Files

### Environment Variables (`.env.example`)
```env
# AI Model Configuration
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
MODEL_NAME=gpt-4

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/medical_ai
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Application
DEBUG=false
LOG_LEVEL=INFO
```

### Docker Configuration
- **Dockerfile**: Multi-stage build for production
- **docker-compose.yml**: Development environment
- **docker-compose.prod.yml**: Production environment

## Key Features

### 1. AI Agents
- **Diagnosis Agent**: Analyzes symptoms and provides differential diagnosis
- **Treatment Agent**: Recomm personalized treatment plans
- **Lab Agent**: Analyzes medical test results

### 2. Data Management
- **Vector Database**: Stores medical knowledge embeddings
- **Caching Layer**: Redis for frequent queries and responses
- **PostgreSQL**: Structured data storage

### 3. Monitoring
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization dashboards
- **Logging**: Structured logging with correlation IDs

### 4. Security
- **JWT Authentication**: Secure API access
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Pydantic models

### 5. Production Features
- **Health Checks**: Service monitoring
- **Error Handling**: Comprehensive error management
- **Performance Optimization**: Caching and async processing

## Development Workflow

1. **Setup**: `scripts/setup.sh`
2. **Development**: Run with `docker-compose up`
3. **Testing**: `pytest tests/`
4. **Deployment**: `docker-compose -f docker-compose.prod.yml up`

## Scaling Strategy

- **Horizontal Scaling**: Load balancer with multiple instances
- **Database**: Read replicas for scaling
- **Cache**: Redis cluster for high availability
- **AI Models**: Load balancing across multiple providers