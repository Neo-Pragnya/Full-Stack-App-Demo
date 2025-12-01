# API Reference

Complete reference for the Numerology Chat Application REST API.

```{toctree}
:maxdepth: 2

endpoints
models
examples
```
errors
examples
```

## API Overview

The Numerology Chat Application provides a RESTful API built with FastAPI, offering:

- **Interactive Documentation**: Auto-generated Swagger UI at `/docs`
- **OpenAPI Schema**: Machine-readable API specification
- **Type Safety**: Pydantic models for request/response validation
- **Performance**: Async endpoints with sub-200ms response times
- **Standards Compliant**: Follows REST conventions and HTTP standards

## Configuration

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

### API Version
- **Current Version**: `v1`
- **Base Path**: `/api/v1/`

### Content Type
All API endpoints expect and return JSON:
```
Content-Type: application/json
```

## Architecture

### Request/Response Flow
```
Client → Load Balancer → API Gateway → FastAPI → Business Logic → Response
   ↓         ↓             ↓           ↓           ↓              ↓
HTTP      Routing       CORS        Validation   Processing    JSON
Request   Rules         Headers     Pydantic     Services      Response
```

### Service Layers

#### API Layer (`app/main.py`)
- HTTP request handling
- Route definitions
- Middleware configuration
- Error handling

#### Business Logic (`app/services/`)
- Numerology calculations
- Chat processing
- Event tracking
- Session management

#### Data Models (`app/models.py`)
- Request/response schemas
- Validation rules
- Type definitions

## Quick Start

### Health Check
```bash
curl http://localhost:8000/health
```

### Calculate Numerology
```bash
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "birth_date": "1990-01-01"
  }'
```

### Start Chat Session
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "session_id": "unique-session-123"
  }'
```

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "status": "success",
  "data": {
    // Response data here
  },
  "timestamp": "2025-11-30T22:40:02.184375"
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      // Specific error details
    }
  },
  "timestamp": "2025-11-30T22:40:02.184375"
}
```

## Development Tools

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### Testing Tools
```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs

# Raw OpenAPI spec
curl http://localhost:8000/openapi.json | jq
```

## 📊 Performance Metrics

| Endpoint | Avg Response Time | Max Response Time | RPS Capacity |
|----------|------------------|------------------|--------------|
| `/health` | 15ms | 50ms | 1000+ |
| `/api/v1/calculate` | 180ms | 300ms | 100+ |
| `/api/v1/chat` | 250ms | 500ms | 50+ |
| `/api/v1/track-event` | 25ms | 100ms | 500+ |

## 🛡️ Security Features

### Input Validation
- Pydantic models validate all inputs
- Type checking and format validation
- SQL injection prevention
- XSS protection

### Rate Limiting (Planned)
```
- 1000 requests per hour per IP
- 100 calculations per hour per session
- 50 chat messages per minute per session
```

### CORS Configuration
```python
allow_origins = [
    "http://localhost:4200",  # Development
    "http://localhost:80",    # Production
    "https://your-domain.com" # Custom domains
]
```

## 🔍 Monitoring & Analytics

### Health Checks
- Application health: `/health`
- Database connectivity (when implemented)
- External service status
- Memory and CPU usage

### Metrics Collection
- Request/response times
- Error rates by endpoint
- User interaction patterns
- Numerology calculation frequency

### Logging
- Structured JSON logs
- Request/response logging
- Error tracking with stack traces
- Performance monitoring

## 🚀 SDK & Client Libraries

### Python Client (Planned)
```python
from numerology_client import NumerologyAPI

client = NumerologyAPI(base_url="http://localhost:8000")
result = client.calculate("John Doe", "1990-01-01")
print(result.life_path.number)
```

### JavaScript/TypeScript Client
```typescript
import { NumerologyClient } from '@numerology/client';

const client = new NumerologyClient('http://localhost:8000');
const result = await client.calculate({
  fullName: 'John Doe',
  birthDate: '1990-01-01'
});
console.log(result.data.lifePathNumber);
```

## 📚 Additional Resources

- **[Endpoints](endpoints.md)** - Detailed endpoint documentation
- **[Models](models.md)** - Complete data model reference  
- **[Examples](examples.md)** - Code examples and tutorials
- [OpenAPI Specification](http://localhost:8000/openapi.json)
- [Interactive API Explorer](http://localhost:8000/docs)