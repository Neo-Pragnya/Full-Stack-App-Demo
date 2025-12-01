#!/bin/bash
# Start Production Services with Docker

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[PROD]${NC} $1"
}

# Check if running from project root
if [ ! -f "docker-compose.yml" ]; then
    echo "Please run this script from the project root directory"
    exit 1
fi

print_header "Starting Numerology Chat Application in Production Mode..."

# Build and start services
print_status "Building and starting Docker containers..."
docker-compose up --build -d

# Wait for services to be healthy
print_status "Waiting for services to be ready..."
sleep 10

# Check service health
print_status "Checking service health..."
docker-compose ps

echo
print_status "✅ Production services started successfully!"
echo
echo "🌐 Application: http://localhost"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo
echo "🐳 Docker commands:"
echo "  docker-compose logs -f         - Follow logs"
echo "  docker-compose stop            - Stop services"
echo "  docker-compose down            - Stop and remove containers"
echo "  docker-compose down -v         - Stop and remove containers and volumes"