#!/bin/bash
# Test Script for Numerology Chat Application

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[TEST]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Check if running from project root
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_header "Testing Numerology Chat Application"

# Test backend
test_backend() {
    print_status "Testing backend..."
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_warning "Virtual environment not found. Run setup-dev.sh first."
        cd ..
        return 1
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Test Python syntax
    print_status "Checking Python syntax..."
    python -m py_compile app/main.py
    python -m py_compile app/models.py
    python -m py_compile app/services/*.py
    
    # Test imports
    print_status "Testing imports..."
    python -c "from app.main import app; print('✅ FastAPI app import successful')"
    python -c "from app.services.numerology_calculator import NumerologyCalculator; print('✅ NumerologyCalculator import successful')"
    python -c "from app.services.chat_service import ChatService; print('✅ ChatService import successful')"
    python -c "from app.services.event_tracker import EventTracker; print('✅ EventTracker import successful')"
    
    cd ..
    print_status "✅ Backend tests passed"
}

# Test frontend
test_frontend() {
    print_status "Testing frontend..."
    
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        print_warning "Node modules not found. Run setup-dev.sh first."
        cd ..
        return 1
    fi
    
    # Test TypeScript compilation
    print_status "Testing TypeScript compilation..."
    npm run build --silent
    
    # Test linting
    print_status "Running linting..."
    npm run lint --silent || print_warning "Linting issues found (non-blocking)"
    
    cd ..
    print_status "✅ Frontend tests passed"
}

# Test Docker build
test_docker() {
    print_status "Testing Docker build..."
    
    # Test backend Docker build
    print_status "Building backend Docker image..."
    docker build -t numerology-backend-test ./backend
    
    # Test frontend Docker build
    print_status "Building frontend Docker image..."
    docker build -t numerology-frontend-test ./frontend
    
    # Clean up test images
    print_status "Cleaning up test images..."
    docker rmi numerology-backend-test numerology-frontend-test
    
    print_status "✅ Docker build tests passed"
}

# Test API endpoints
test_api() {
    print_status "Testing API endpoints..."
    
    # Check if backend is running
    if ! curl -s http://localhost:8000/health > /dev/null; then
        print_warning "Backend not running. Starting backend..."
        cd backend
        source venv/bin/activate
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
        BACKEND_PID=$!
        cd ..
        
        # Wait for backend to start
        sleep 5
        
        # Test endpoints
        test_endpoints
        
        # Clean up
        kill $BACKEND_PID
    else
        test_endpoints
    fi
}

test_endpoints() {
    print_status "Testing health endpoint..."
    if curl -s http://localhost:8000/health | grep -q "ok"; then
        print_status "✅ Health endpoint working"
    else
        print_error "❌ Health endpoint failed"
        return 1
    fi
    
    print_status "Testing numerology calculation..."
    local response=$(curl -s -X POST http://localhost:8000/calculate \
        -H "Content-Type: application/json" \
        -d '{"name": "John Doe", "birth_date": "1990-01-01"}')
    
    if echo "$response" | grep -q "life_path"; then
        print_status "✅ Numerology calculation working"
    else
        print_error "❌ Numerology calculation failed"
        return 1
    fi
    
    print_status "Testing chat endpoint..."
    local chat_response=$(curl -s -X POST http://localhost:8000/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello", "session_id": "test"}')
    
    if echo "$chat_response" | grep -q "response"; then
        print_status "✅ Chat endpoint working"
    else
        print_error "❌ Chat endpoint failed"
        return 1
    fi
}

# Parse command line arguments
SKIP_BACKEND=false
SKIP_FRONTEND=false
SKIP_DOCKER=false
SKIP_API=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-backend)
            SKIP_BACKEND=true
            shift
            ;;
        --skip-frontend)
            SKIP_FRONTEND=true
            shift
            ;;
        --skip-docker)
            SKIP_DOCKER=true
            shift
            ;;
        --skip-api)
            SKIP_API=true
            shift
            ;;
        --api-only)
            SKIP_BACKEND=true
            SKIP_FRONTEND=true
            SKIP_DOCKER=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --skip-backend    Skip backend tests"
            echo "  --skip-frontend   Skip frontend tests"
            echo "  --skip-docker     Skip Docker tests"
            echo "  --skip-api        Skip API tests"
            echo "  --api-only        Only run API tests"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

# Run tests
if [ "$SKIP_BACKEND" = false ]; then
    test_backend
fi

if [ "$SKIP_FRONTEND" = false ]; then
    test_frontend
fi

if [ "$SKIP_DOCKER" = false ]; then
    test_docker
fi

if [ "$SKIP_API" = false ]; then
    test_api
fi

print_header "All Tests Completed Successfully! 🎉"