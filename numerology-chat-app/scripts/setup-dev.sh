#!/bin/bash
# Development Setup Script for Numerology Chat Application

set -e  # Exit on any error

echo "🚀 Setting up Numerology Chat Application for Development..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running from project root
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Check prerequisites
print_status "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check Node.js (for local development)
if ! command -v node &> /dev/null; then
    print_warning "Node.js is not installed. You'll need it for local frontend development."
fi

# Check Python (for local development)
if ! command -v python3 &> /dev/null; then
    print_warning "Python 3 is not installed. You'll need it for local backend development."
fi

print_status "Prerequisites check completed!"

# Setup backend
print_status "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
print_status "Installing backend dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cd ..

# Setup frontend
print_status "Setting up frontend..."
cd frontend

# Install Node.js dependencies
if [ -f "package.json" ]; then
    print_status "Installing frontend dependencies..."
    npm install
else
    print_warning "No package.json found in frontend directory"
fi

cd ..

print_status "✅ Development setup completed!"

echo
echo "🔧 Available development commands:"
echo "  ./scripts/start-dev.sh     - Start development servers"
echo "  ./scripts/start-docker.sh  - Start with Docker"
echo "  ./scripts/test.sh          - Run tests"
echo "  ./scripts/stop.sh          - Stop all services"
echo
print_status "Happy coding! 🎉"