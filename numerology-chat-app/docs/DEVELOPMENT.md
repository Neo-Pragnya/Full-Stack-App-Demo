# Development Guide

## Getting Started with Development

This guide covers everything you need to know to develop and contribute to the Numerology Chat Application.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Backend Development](#backend-development)
4. [Frontend Development](#frontend-development)
5. [Testing](#testing)
6. [Debugging](#debugging)
7. [Contributing Guidelines](#contributing-guidelines)

---

## Development Environment Setup

### Prerequisites

- **Docker Desktop** 4.0+ (recommended)
- **Node.js** 18.0+ with npm
- **Python** 3.11+ with pip
- **Git** for version control

### Initial Setup

```bash
# Clone and setup
git clone <repository-url>
cd numerology-chat-app

# Run setup script
./scripts/setup-dev.sh

# Start development environment
./scripts/start-dev.sh --local
```

### IDE Configuration

#### VS Code (Recommended)
Install these extensions:
- Python
- Angular Language Service
- TypeScript Importer
- Docker
- GitLens
- Prettier
- ESLint

#### PyCharm/WebStorm
- Enable Python/TypeScript support
- Configure Docker integration
- Set up remote debugging

---

## Project Structure

```
numerology-chat-app/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── models.py          # Pydantic models
│   │   └── services/          # Business logic
│   │       ├── __init__.py
│   │       ├── numerology_calculator.py
│   │       ├── chat_service.py
│   │       └── event_tracker.py
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Production container
│   └── venv/                 # Virtual environment (created)
│
├── frontend/                  # Angular frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/    # Angular components
│   │   │   ├── services/      # Angular services
│   │   │   ├── models/        # TypeScript interfaces
│   │   │   └── app.module.ts  # Main module
│   │   ├── assets/           # Static assets
│   │   └── styles/           # Global styles
│   ├── package.json          # Node.js dependencies
│   ├── angular.json          # Angular configuration
│   ├── tsconfig.json         # TypeScript configuration
│   └── Dockerfile           # Production container
│
├── scripts/                   # Development scripts
│   ├── setup-dev.sh         # Environment setup
│   ├── start-dev.sh         # Start development
│   ├── start-docker.sh      # Start production
│   ├── test.sh              # Run tests
│   └── stop.sh              # Stop services
│
├── docs/                     # Documentation
│   ├── API.md               # API documentation
│   ├── DEVELOPMENT.md       # This file
│   └── DEPLOYMENT.md        # Deployment guide
│
├── docker-compose.yml        # Production deployment
├── docker-compose.dev.yml   # Development environment
└── README.md                # Project overview
```

---

## Backend Development

### Architecture

The backend follows a modular service-oriented architecture:

- **main.py**: FastAPI application with routes
- **models.py**: Pydantic models for validation
- **services/**: Business logic separated by domain

### Key Components

#### NumerologyCalculator
```python
# Location: app/services/numerology_calculator.py
# Purpose: Core numerology calculations
# Methods:
#   - calculate_life_path(birth_date)
#   - calculate_expression(name)
#   - calculate_soul_urge(name)
#   - calculate_personality(name)
```

#### ChatService
```python
# Location: app/services/chat_service.py
# Purpose: Chat interaction handling
# Methods:
#   - process_message(message, context)
#   - generate_response(message, numerology_data)
```

#### EventTracker
```python
# Location: app/services/event_tracker.py
# Purpose: User interaction tracking
# Methods:
#   - track_event(event_type, session_id, data)
#   - get_analytics(session_id)
```

### Adding New Features

#### 1. Add New Calculation

```python
# In numerology_calculator.py
def calculate_karmic_debt(self, birth_date: str) -> Dict[str, Any]:
    """Calculate karmic debt numbers"""
    # Your calculation logic here
    return {
        "numbers": [13, 14, 16, 19],
        "interpretation": "Karmic debt interpretation..."
    }
```

#### 2. Add New Endpoint

```python
# In main.py
@app.post("/karmic-debt")
async def calculate_karmic_debt(person: PersonInput):
    try:
        calculator = NumerologyCalculator()
        result = calculator.calculate_karmic_debt(person.birth_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### 3. Add New Model

```python
# In models.py
class KarmicDebtInput(BaseModel):
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD format")
    
class KarmicDebtResult(BaseModel):
    numbers: List[int]
    interpretation: str
```

### Testing Backend

```bash
# Run backend tests
cd backend
source venv/bin/activate

# Test specific module
python -m pytest tests/test_numerology.py -v

# Test with coverage
python -m pytest --cov=app tests/

# Test API endpoints
python -m pytest tests/test_api.py -v
```

### Debugging Backend

```bash
# Start with debug mode
cd backend
source venv/bin/activate
export LOG_LEVEL=debug
uvicorn app.main:app --reload --log-level debug

# Use debugger
import pdb; pdb.set_trace()  # Add to code

# View logs
tail -f logs/app.log
```

---

## Frontend Development

### Architecture

The frontend uses Angular with a component-based architecture:

- **Components**: UI components for different features
- **Services**: API communication and business logic
- **Models**: TypeScript interfaces for type safety

### Key Components

#### ChatComponent
```typescript
// Location: src/app/components/chat/
// Purpose: Main chat interface
// Features:
//   - Real-time messaging
//   - Thumbs up/down feedback
//   - Message history
```

#### NumerologyTabsComponent
```typescript
// Location: src/app/components/numerology-tabs/
// Purpose: Display numerology results
// Features:
//   - Tabbed interface
//   - Detailed interpretations
//   - Visual representations
```

#### ApiService
```typescript
// Location: src/app/services/api.service.ts
// Purpose: HTTP communication with backend
// Methods:
//   - calculateNumerology()
//   - sendChatMessage()
//   - trackEvent()
```

### Adding New Features

#### 1. Add New Component

```bash
# Generate component
ng generate component components/new-feature

# Generate with options
ng generate component components/new-feature --standalone --inline-template
```

#### 2. Add New Service

```bash
# Generate service
ng generate service services/new-service

# Add to providers in app.module.ts
```

#### 3. Add New Model

```typescript
// In src/app/models/
export interface NewModel {
  id: string;
  name: string;
  value: number;
}
```

### Styling

The application uses Angular Material with custom SCSS:

```scss
// src/styles/globals.scss
.custom-theme {
  @include mat.all-component-themes($theme);
}

// Component-specific styles
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
```

### Testing Frontend

```bash
# Unit tests
ng test

# E2E tests
ng e2e

# Build test
ng build --configuration production

# Lint
ng lint
```

### Debugging Frontend

```bash
# Development server with source maps
ng serve --source-map

# Debug in browser
# Open Developer Tools > Sources > webpack:// > src/app

# Using Angular DevTools extension
# Install Angular DevTools browser extension
```

---

## Testing

### Backend Testing Strategy

#### Unit Tests
```python
# tests/test_numerology.py
import pytest
from app.services.numerology_calculator import NumerologyCalculator

def test_life_path_calculation():
    calculator = NumerologyCalculator()
    result = calculator.calculate_life_path("1990-01-01")
    assert result["number"] == 5
    assert "interpretation" in result
```

#### Integration Tests
```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_calculate_endpoint():
    response = client.post("/calculate", json={
        "name": "John Doe", 
        "birth_date": "1990-01-01"
    })
    assert response.status_code == 200
    assert "life_path" in response.json()
```

### Frontend Testing Strategy

#### Component Tests
```typescript
// chat.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatComponent } from './chat.component';

describe('ChatComponent', () => {
  let component: ChatComponent;
  let fixture: ComponentFixture<ChatComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ChatComponent]
    });
    fixture = TestBed.createComponent(ChatComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should send message', () => {
    component.messageText = 'Hello';
    component.sendMessage();
    expect(component.messages).toHaveLength(1);
  });
});
```

#### Service Tests
```typescript
// api.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ApiService } from './api.service';

describe('ApiService', () => {
  let service: ApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ApiService]
    });
    service = TestBed.inject(ApiService);
  });

  it('should calculate numerology', () => {
    // Test implementation
  });
});
```

### E2E Testing

```typescript
// e2e/src/app.e2e-spec.ts
import { AppPage } from './app.po';

describe('workspace-project App', () => {
  let page: AppPage;

  beforeEach(() => {
    page = new AppPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getTitleText()).toEqual('Numerology Chat Application');
  });

  it('should perform calculation', () => {
    page.navigateTo();
    page.fillForm('John Doe', '1990-01-01');
    page.clickCalculate();
    expect(page.getResult()).toContain('Life Path');
  });
});
```

---

## Debugging

### Common Issues

#### Backend Issues

**Import Errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt
```

**CORS Errors**
```python
# Check CORS configuration in main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Frontend Issues

**Module Not Found**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Angular version compatibility
ng version
```

**TypeScript Errors**
```bash
# Check TypeScript configuration
npx tsc --noEmit

# Update types
npm install @types/node --save-dev
```

### Debug Tools

#### Backend
- **PyCharm Debugger**: Set breakpoints in IDE
- **pdb**: Add `import pdb; pdb.set_trace()` in code
- **FastAPI Debug**: Use `--reload` flag for hot reload
- **Logs**: Check application logs in `logs/` directory

#### Frontend
- **Angular DevTools**: Browser extension for component inspection
- **Chrome DevTools**: Network, console, and source debugging
- **Angular CLI**: Use `ng serve --source-map` for better debugging
- **RxJS Debug**: Use tap operators to debug observables

---

## Contributing Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints for all functions
- Maximum line length: 100 characters
- Use docstrings for all public methods

```python
def calculate_life_path(self, birth_date: str) -> Dict[str, Any]:
    """
    Calculate life path number from birth date.
    
    Args:
        birth_date: Birth date in YYYY-MM-DD format
        
    Returns:
        Dictionary containing number and interpretation
        
    Raises:
        ValueError: If birth_date format is invalid
    """
    # Implementation here
```

#### TypeScript (Frontend)
- Follow Angular style guide
- Use strict TypeScript configuration
- Prefer interfaces over classes for data models
- Use async/await over promises

```typescript
interface CalculationRequest {
  name: string;
  birthDate: string;
}

async calculateNumerology(request: CalculationRequest): Promise<NumerologyResult> {
  try {
    const response = await this.http.post<NumerologyResult>('/calculate', request).toPromise();
    return response;
  } catch (error) {
    console.error('Calculation failed:', error);
    throw error;
  }
}
```

### Git Workflow

#### Branch Naming
- **Feature**: `feature/add-karmic-debt-calculation`
- **Bugfix**: `bugfix/fix-chat-scroll-issue`
- **Hotfix**: `hotfix/security-patch`
- **Chore**: `chore/update-dependencies`

#### Commit Messages
```bash
# Format: type(scope): description
feat(backend): add karmic debt calculation endpoint
fix(frontend): resolve chat scroll issue
docs(readme): update setup instructions
test(api): add integration tests for chat endpoints
```

#### Pull Request Process
1. Create feature branch from main
2. Make changes and add tests
3. Run full test suite: `./scripts/test.sh`
4. Update documentation if needed
5. Submit PR with clear description
6. Address review feedback
7. Merge after approval

### Testing Requirements
- Maintain 80%+ test coverage
- All new features must include tests
- Integration tests for API endpoints
- Component tests for UI features

### Documentation Requirements
- Update API.md for new endpoints
- Add JSDoc comments for TypeScript
- Update README for significant changes
- Include examples in documentation

---

## Performance Guidelines

### Backend Optimization
- Use async/await for I/O operations
- Implement response caching where appropriate
- Profile CPU-intensive calculations
- Monitor memory usage for large datasets

### Frontend Optimization
- Use OnPush change detection strategy
- Implement lazy loading for routes
- Optimize bundle size with tree shaking
- Use Angular's built-in performance tools

### Monitoring
- Add logging for performance bottlenecks
- Monitor API response times
- Track user interaction patterns
- Set up alerts for error rates

---

## Deployment

### Development Deployment
```bash
# Quick development deployment
./scripts/start-dev.sh --docker

# With custom configuration
docker-compose -f docker-compose.dev.yml up
```

### Production Deployment
```bash
# Production deployment
./scripts/start-docker.sh

# With environment file
docker-compose --env-file .env.prod up -d
```

### Environment Variables

#### Backend
```env
ENVIRONMENT=development
LOG_LEVEL=debug
CORS_ORIGINS=http://localhost:4200,http://localhost:80
```

#### Frontend
```env
API_BASE_URL=http://localhost:8000
ENVIRONMENT=development
```

---

This development guide should help you get started with contributing to the Numerology Chat Application. For specific questions or issues, please check the main README or create an issue in the repository.