#!/bin/bash
# Stop All Services for Numerology Chat Application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Stopping Numerology Chat Application services..."

# Stop Docker services
if docker-compose ps -q > /dev/null 2>&1; then
    print_status "Stopping Docker services..."
    docker-compose down
    
    # Optional: Remove volumes
    if [ "$1" = "--clean" ]; then
        print_warning "Removing volumes and data..."
        docker-compose down -v
    fi
fi

# Stop local development services
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null; then
        print_status "Stopping backend process (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
    fi
    rm .backend.pid
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
        print_status "Stopping frontend process (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
    fi
    rm .frontend.pid
fi

# Stop any remaining Node.js processes on port 4200
print_status "Checking for processes on port 4200..."
if lsof -ti:4200 > /dev/null 2>&1; then
    print_warning "Stopping processes on port 4200..."
    lsof -ti:4200 | xargs kill -9
fi

# Stop any remaining Python processes on port 8000
print_status "Checking for processes on port 8000..."
if lsof -ti:8000 > /dev/null 2>&1; then
    print_warning "Stopping processes on port 8000..."
    lsof -ti:8000 | xargs kill -9
fi

print_status "✅ All services stopped successfully!"

if [ "$1" = "--help" ]; then
    echo
    echo "Usage: $0 [--clean]"
    echo "  --clean   Also remove Docker volumes and data"
fi