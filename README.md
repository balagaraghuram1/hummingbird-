f# 🏥 Hummingbird Medical AI

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-black.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-orange.svg)](https://langchain.com)

A cutting-edge, production-ready medical AI system powered by the latest language models, vector databases, and advanced AI agents. Built with FastAPI, LangChain, and modern AI technologies for intelligent medical diagnosis, treatment recommendations, and lab analysis.

## 🚀 Features

### 🧠 Advanced AI Capabilities
- **Multi-LLM Support**: GPT-4, Claude, and Gemini integration
- **LangChain Agents**: Specialized medical AI agents for diagnosis, treatment, and lab analysis
- **Vector Database**: ChromaDB for medical knowledge retrieval and similarity search
- **Intelligent Caching**: Redis-based caching for improved performance

### 🔒 Production-Ready
- **Authentication**: JWT-based secure API access
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Logging**: Structured logging with correlation IDs
- **Rate Limiting**: API abuse prevention
- **Health Checks**: Comprehensive service monitoring

### 📊 Medical Intelligence
- **Symptom Analysis**: Advanced symptom-to-diagnosis mapping
- **Treatment Recommendations**: Personalized treatment plans based on medical guidelines
- **Lab Analysis**: Intelligent interpretation of medical test results
- **Medical Knowledge Base**: Continuously updated medical literature integration

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "API Layer"
        A[FastAPI Application]
        B[Authentication Middleware]
        C[Rate Limiting]
    end
    
    subgraph "AI Processing"
        D[LangChain Agents]
        E[Diagnosis Agent]
        F[Treatment Agent]
        G[Lab Analysis Agent]
    end
    
    subgraph "Data Layer"
        H[Vector Database<br/>ChromaDB]
        I[Redis Cache]
        J[PostgreSQL<br/>Medical DB]
    end
    
    subgraph "Monitoring"
        K[Prometheus]
        L[Grafana]
        M[Structured Logging]
    end
    
    A --> D
    D --> E
    D --> F
    D --> G
    E --> H
    F --> H
    G --> H
    D --> I
    A --> K
    A --> L
    A --> M
```

## 🛠️ Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Redis
- PostgreSQL
- OpenAI/Anthropic API keys

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/hummingbird-medical-ai.git
   cd hummingbird-medical-ai
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start services**
   ```bash
   # Development
   docker-compose up -d
   
   # Production
   docker-compose -f docker-compose.prod.yml up -d
   ```

5. **Run the application**
   ```bash
   uvicorn src.main:app --reload
   ```

## 📚 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

#### Authentication
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/refresh` - Refresh JWT token

#### Medical AI Services
- `POST /api/ai/diagnose` - Medical diagnosis from symptoms
- `POST /api/ai/treatment` - Treatment recommendations
- `POST /api/ai/analyze-lab` - Lab result analysis
- `POST /api/ai/chat` - General medical consultation

#### Health Monitoring
- `GET /api/health` - Service health check
- `GET /api/metrics` - Prometheus metrics

## 🔧 Configuration

### Environment Variables

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

### Model Configuration

The system supports multiple AI models:

```python
# src/config/settings.py
AI_MODELS = {
    "primary": "gpt-4",
    "fallback": "claude-3",
    "specialized": "gemini-pro"
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src

# Run specific test categories
pytest tests/test_agents.py
pytest tests/test_api.py
```

## 📊 Monitoring

### Prometheus Metrics
Access metrics at `http://localhost:8000/metrics`

### Grafana Dashboard
1. Start Grafana: `docker-compose up grafana`
2. Access at `http://localhost:3000`
3. Import dashboard from `monitoring/grafana/dashboards/medical_ai.json`

### Key Metrics Tracked
- API response times
- AI model performance
- Error rates
- Cache hit ratios
- Database query performance

## 🔒 Security Features

- **JWT Authentication**: Secure API access with token-based authentication
- **Rate Limiting**: Prevent API abuse with configurable rate limits
- **Input Validation**: Pydantic models for request/response validation
- **CORS Protection**: Configurable cross-origin resource sharing
- **SQL Injection Protection**: ORM-based database access

## 🚀 Deployment

### Docker Deployment

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment

1. **Build the application**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up databases**
   ```bash
   python scripts/setup_db.py
   ```

3. **Start services**
   ```bash
   python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation for new features
- Use type hints throughout the codebase

## 📈 Performance Optimization

### Caching Strategy
- **Response Caching**: Cache frequent API responses
- **Model Results**: Cache AI model outputs
- **Vector Search**: Cache similar queries

### Database Optimization
- **Indexing**: Proper indexing on medical data
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Fast query execution

### AI Model Optimization
- **Model Selection**: Choose optimal models for different tasks
- **Batch Processing**: Process multiple requests efficiently
- **Fallback Mechanisms**: Graceful degradation when models fail

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose ps postgres
   
   # Reset database
   docker-compose down
   docker-compose up -d postgres
   ```

2. **AI Model Failures**
   - Check API keys in `.env`
   - Verify model availability
   - Check network connectivity

3. **Memory Issues**
   - Monitor memory usage with `docker stats`
   - Adjust container limits in `docker-compose.yml`

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn src.main:app --reload --log-level debug
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- LangChain team for the amazing framework
- FastAPI team for the modern web framework
- Medical data providers and research institutions

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/hummingbird-medical-ai/issues)
- **Documentation**: [Full Documentation](docs/)
- **Community**: [Discord Server](https://discord.gg/your-server)

---

Built with ❤️ for the medical AI community