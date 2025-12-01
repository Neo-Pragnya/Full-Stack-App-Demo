#!/bin/bash
# Start Development Services for Numerology Chat Application

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[DEV]${NC} $1"
}

# Check if running from project root
if [ ! -f "docker-compose.yml" ]; then
    echo "Please run this script from the project root directory"
    exit 1
fi

print_header "Starting Numerology Chat Application in Development Mode..."

# Function to start services locally
start_local() {
    print_status "Starting services locally..."
    
    # Start backend
    print_status "Starting FastAPI backend on http://localhost:8000"
    cd backend
    source venv/bin/activate
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend
    print_status "Starting Angular frontend on http://localhost:4200"
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    # Save PIDs for cleanup
    echo $BACKEND_PID > .backend.pid
    echo $FRONTEND_PID > .frontend.pid
    
    print_status "✅ Services started successfully!"
    echo
    echo "🌐 Frontend: http://localhost:4200"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo
    print_warning "Press Ctrl+C to stop all services or run ./scripts/stop.sh"
    
    # Keep script running
    wait
}

# Function to start services with Docker
start_docker() {
    print_status "Starting services with Docker..."
    docker-compose -f docker-compose.dev.yml up --build
}

# Parse command line arguments
MODE="local"
while [[ $# -gt 0 ]]; do
    case $1 in
        --docker)
            MODE="docker"
            shift
            ;;
        --local)
            MODE="local"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--local|--docker]"
            echo "  --local   Start services locally (default)"
            echo "  --docker  Start services with Docker"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

# Start services based on mode
if [ "$MODE" = "docker" ]; then
    start_docker
else
    start_local
fi