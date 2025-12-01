# Numerology Chat Application

A full-stack web application that combines numerology calculations with an interactive chat interface. Built with Angular frontend and FastAPI backend, featuring real-time numerology analysis, chat functionality with thumbs up/down feedback, and comprehensive event tracking.

## 🌟 Features

- **Interactive Chat Interface**: Real-time chat with numerology-focused conversations
- **Numerology Calculations**: Comprehensive Pythagorean numerology analysis including:
  - Life Path Number
  - Expression Number  
  - Soul Urge Number
  - Personality Number
  - Master Numbers detection
- **Detailed Visualizations**: Tab-based interface showing different aspects of numerology
- **Event Tracking**: User interaction analytics with session management
- **Responsive Design**: Modern Material Design UI that works on all devices
- **Docker Support**: Full containerization for easy deployment
- **Real-time Feedback**: Thumbs up/down rating system for chat responses

## 🏗️ Architecture

```
numerology-chat-app/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── models.py       # Pydantic models
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/               # Angular frontend
│   ├── src/
│   │   ├── app/           # Angular application
│   │   └── assets/        # Static assets
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile        # Frontend container
├── scripts/               # Development and deployment scripts
├── docker-compose.yml    # Production deployment
└── docker-compose.dev.yml # Development environment
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **Node.js 18+** (for local development)
- **Python 3.11+** (for local development)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
cd numerology-chat-app

# Start with production setup
./scripts/start-docker.sh

# OR start with development setup (includes hot reload)
./scripts/start-dev.sh --docker
```

The application will be available at:
- **Frontend**: http://localhost (production) or http://localhost:4200 (development)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Option 2: Local Development

```bash
# Setup development environment
./scripts/setup-dev.sh

# Start development servers
./scripts/start-dev.sh --local
```

## 📖 Detailed Setup Instructions

### 1. Environment Setup

First, set up your development environment:

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run the setup script
./scripts/setup-dev.sh
```

This script will:
- Check prerequisites (Docker, Node.js, Python)
- Create Python virtual environment
- Install backend dependencies
- Install frontend dependencies

### 2. Development Mode

For active development with hot reload:

```bash
# Start services locally (recommended for development)
./scripts/start-dev.sh --local

# OR start with Docker (useful for testing containerization)
./scripts/start-dev.sh --docker
```

### 3. Production Deployment

For production deployment:

```bash
# Build and start production containers
./scripts/start-docker.sh

# View logs
docker-compose logs -f

# Stop services
./scripts/stop.sh
```

### 4. Testing

Run comprehensive tests:

```bash
# Run all tests
./scripts/test.sh

# Run specific test categories
./scripts/test.sh --skip-docker  # Skip Docker build tests
./scripts/test.sh --api-only     # Only test API endpoints
```

## 🔧 API Documentation

### Base URL
- Development: `http://localhost:8000`
- Production: `http://localhost:8000` (or your deployed URL)

### Authentication
Currently using session-based tracking. No authentication required.

### Endpoints

#### Health Check
```http
GET /health
```
Returns application health status.

#### Numerology Calculation
```http
POST /calculate
Content-Type: application/json

{
  "name": "John Doe",
  "birth_date": "1990-01-01"
}
```

Response includes:
- Life Path Number and interpretation
- Expression Number and meaning
- Soul Urge Number and description
- Personality Number and traits
- Master Numbers detection
- Detailed analysis and recommendations

#### Chat Interface
```http
POST /chat
Content-Type: application/json

{
  "message": "Tell me about my numerology",
  "session_id": "unique-session-id",
  "context": {
    "name": "John Doe",
    "birth_date": "1990-01-01"
  }
}
```

#### Event Tracking
```http
POST /track-event
Content-Type: application/json

{
  "event_type": "thumbs_up",
  "session_id": "unique-session-id",
  "data": {
    "message_id": "msg-123",
    "rating": "positive"
  }
}
```

#### Analytics
```http
GET /analytics/{session_id}
```

## 🎨 Frontend Features

### Chat Interface
- Real-time messaging with typing indicators
- Message history with timestamps
- Thumbs up/down feedback system
- Auto-scroll to latest messages
- Responsive design for mobile and desktop

### Numerology Tabs
- **Overview**: Summary of all calculations
- **Life Path**: Detailed life path analysis
- **Expression**: Expression number insights
- **Soul Urge**: Soul urge interpretation
- **Personality**: Personality number traits
- **Analysis**: Comprehensive report

### User Experience
- Material Design components
- Smooth animations and transitions
- Loading states and error handling
- Accessibility features (WCAG compliant)
- Progressive Web App capabilities

## 🔍 Technical Details

### Backend (FastAPI)
- **Framework**: FastAPI 0.104.1
- **Python**: 3.11+
- **Dependencies**: 
  - Pydantic for data validation
  - Uvicorn for ASGI server
  - FastAPI CORS middleware
- **Architecture**: Modular service-based design
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging with different levels

### Frontend (Angular)
- **Framework**: Angular 17
- **UI Library**: Angular Material
- **Styling**: SCSS with responsive design
- **State Management**: RxJS Observables
- **HTTP Client**: Angular HTTP Client with interceptors
- **TypeScript**: Strict mode enabled
- **Build Tool**: Angular CLI with Webpack

### Numerology Engine
- **System**: Pythagorean numerology
- **Calculations**:
  - Life Path: Sum of birth date digits
  - Expression: Sum of full name letter values  
  - Soul Urge: Sum of vowels in name
  - Personality: Sum of consonants in name
- **Master Numbers**: 11, 22, 33 detection and handling
- **Interpretations**: Comprehensive meanings and traits

### Event Tracking
- **Storage**: In-memory with session management
- **Events**: User interactions, feedback, calculations
- **Analytics**: Session-based metrics and insights
- **Privacy**: No personal data storage beyond session

## 🐳 Docker Configuration

### Production Setup
- **Backend**: Python slim image with Uvicorn
- **Frontend**: Multi-stage build with Nginx
- **Networking**: Internal Docker network
- **Volumes**: Persistent data storage
- **Health Checks**: Built-in container health monitoring

### Development Setup
- **Hot Reload**: File watching for both services
- **Port Mapping**: Direct port access for debugging
- **Volume Mounts**: Source code mounted for live editing
- **Environment Variables**: Development-specific configuration

## 🔒 Security Features

- **CORS**: Properly configured cross-origin policies
- **Input Validation**: Pydantic models for API validation
- **XSS Protection**: Angular's built-in XSS protection
- **CSP Headers**: Content Security Policy headers
- **Rate Limiting**: Future enhancement for API protection

## 🚀 Deployment Options

### Docker Compose (Recommended)
```bash
# Production deployment
docker-compose up -d

# With custom configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Kubernetes
```yaml
# Example Kubernetes deployment (adapt as needed)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: numerology-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: numerology-app
  template:
    metadata:
      labels:
        app: numerology-app
    spec:
      containers:
      - name: backend
        image: numerology-backend:latest
        ports:
        - containerPort: 8000
      - name: frontend
        image: numerology-frontend:latest
        ports:
        - containerPort: 80
```

### Cloud Platforms
- **AWS**: Deploy using ECS, EKS, or Elastic Beanstalk
- **Google Cloud**: Use Cloud Run, GKE, or App Engine
- **Azure**: Deploy with Container Instances or AKS
- **Heroku**: Use container registry for deployment

## 📊 Performance Considerations

### Backend Optimization
- Async/await for I/O operations
- Connection pooling for databases (when added)
- Response caching for static calculations
- Background task processing capabilities

### Frontend Optimization
- Lazy loading for routes and modules
- OnPush change detection strategy
- Image optimization and compression
- Service worker for caching (PWA)

### Infrastructure
- CDN for static assets
- Load balancing for high availability
- Database indexing and optimization
- Monitoring and alerting setup

## 🧪 Testing Strategy

### Backend Testing
- Unit tests for calculation logic
- Integration tests for API endpoints
- Performance tests for heavy calculations
- Security tests for input validation

### Frontend Testing
- Component unit tests with Jasmine/Karma
- End-to-end tests with Cypress
- Accessibility testing with axe-core
- Visual regression testing

### Integration Testing
- API contract testing
- Cross-browser compatibility
- Mobile responsive testing
- Docker container testing

## 📈 Monitoring & Analytics

### Application Metrics
- Response times and throughput
- Error rates and status codes
- User engagement metrics
- Calculation accuracy tracking

### Infrastructure Metrics
- Container resource usage
- Database performance
- Network latency
- Storage utilization

### User Analytics
- Feature usage patterns
- User journey analysis
- Feedback sentiment analysis
- Session duration metrics

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and test thoroughly
4. Run the test suite: `./scripts/test.sh`
5. Commit with clear messages: `git commit -m "Add: new feature description"`
6. Push and create a pull request

### Code Standards
- **Python**: Follow PEP 8 style guide
- **TypeScript**: Use Angular style guide
- **Documentation**: Update README for new features
- **Testing**: Maintain test coverage above 80%

### Pull Request Process
1. Ensure all tests pass
2. Update documentation as needed
3. Add screenshots for UI changes
4. Request review from maintainers
5. Address feedback promptly

## 🆘 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Permission denied
sudo chown -R $USER:$USER .

# Port already in use
./scripts/stop.sh --clean
lsof -ti:8000 | xargs kill -9

# Build failures
docker system prune -a
```

#### Development Issues
```bash
# Python virtual environment issues
rm -rf backend/venv
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt

# Node.js issues
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### API Connection Issues
```bash
# Check backend health
curl http://localhost:8000/health

# Check CORS configuration
curl -H "Origin: http://localhost:4200" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS http://localhost:8000/calculate
```

### Logs and Debugging

#### View Application Logs
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Local development logs
tail -f backend/logs/app.log
```

#### Debug Mode
```bash
# Backend debug mode
cd backend
source venv/bin/activate
export LOG_LEVEL=debug
uvicorn app.main:app --reload --log-level debug

# Frontend debug mode
cd frontend
ng serve --configuration development
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

- **Documentation**: Check this README and API docs at `/docs`
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions for questions and ideas
- **Email**: Contact maintainers for security issues

## 🔮 Roadmap

### Short Term (v1.1)
- [ ] User authentication and profiles
- [ ] Persistent data storage with PostgreSQL
- [ ] Advanced numerology calculations
- [ ] Email notifications for results

### Medium Term (v1.5)
- [ ] Multiple numerology systems (Chaldean, Kabbalah)
- [ ] Compatibility analysis between users
- [ ] Advanced analytics dashboard
- [ ] Mobile application

### Long Term (v2.0)
- [ ] AI-powered interpretation enhancement
- [ ] Social features and sharing
- [ ] Premium subscription model
- [ ] Multi-language support

---

## 🎉 Acknowledgments

- **Numerology System**: Based on traditional Pythagorean numerology
- **UI Design**: Inspired by modern chat interfaces and Material Design
- **Architecture**: Following FastAPI and Angular best practices
- **Community**: Thanks to all contributors and users

**Happy Numerology Analysis!** ✨🔢✨