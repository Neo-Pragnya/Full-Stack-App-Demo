# Demo Instructions

## Quick Start Demo

Follow these steps to run the Numerology Chat Application:

### 1. Initial Setup (One Time)

```bash
# Navigate to the project directory
cd numerology-chat-app

# Make scripts executable
chmod +x scripts/*.sh

# Run the setup script
./scripts/setup-dev.sh
```

### 2. Start the Application

#### Option A: Start with Docker (Recommended for Production)
```bash
# Start production environment
./scripts/start-docker.sh

# The application will be available at:
# - Frontend: http://localhost
# - Backend API: http://localhost:8000
# - API Documentation: http://localhost:8000/docs
```

#### Option B: Start Locally (Development)
```bash
# Start development environment
./scripts/start-dev.sh --local

# The application will be available at:
# - Frontend: http://localhost:4200
# - Backend API: http://localhost:8000
# - API Documentation: http://localhost:8000/docs
```

### 3. Test the Application

#### Quick API Test
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test numerology calculation
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "birth_date": "1990-01-01"}'
```

#### Frontend Demo Steps

1. **Open the application** in your browser
   - Production: http://localhost
   - Development: http://localhost:4200

2. **Enter your information**
   - Full Name: "John Doe"
   - Birth Date: "1990-01-01"
   - Click "Calculate"

3. **Explore the Chat Interface**
   - Ask questions like: "Tell me about my life path number"
   - Use thumbs up/down to rate responses
   - Try different conversation topics

4. **Navigate the Numerology Tabs**
   - **Summary**: Overview of all calculations
   - **Core Numbers**: Life Path, Destiny, Soul Urge, Personality
   - **Advanced**: Birth Day, Balance, Hidden Passion numbers
   - **Life Cycles**: Personal Year, Challenges, Pinnacles
   - **Spiritual**: Karmic Lessons and spiritual insights
   - **Timing**: Personal year analysis and timing guidance

5. **Interactive Features**
   - Real-time chat responses
   - Tab-based detailed numerology analysis
   - Feedback system with thumbs up/down
   - Responsive design for mobile and desktop

### 4. Stop the Application

```bash
# Stop all services
./scripts/stop.sh

# Stop and clean up (removes data)
./scripts/stop.sh --clean
```

### 5. Run Tests

```bash
# Run all tests
./scripts/test.sh

# Run specific test categories
./scripts/test.sh --skip-docker    # Skip Docker build tests
./scripts/test.sh --api-only       # Only test API endpoints
./scripts/test.sh --skip-frontend  # Skip frontend tests
```

## Demo Scenarios

### Scenario 1: New User Experience
1. Open application for first time
2. Enter name and birth date
3. Calculate numerology
4. Explore different tabs to understand numbers
5. Ask chat questions about specific numbers

### Scenario 2: Interactive Chat Demo
1. Start with calculation
2. Ask: "What does my life path number mean for my career?"
3. Rate the response with thumbs up
4. Ask: "How do my numbers work together?"
5. Switch between tabs while chatting

### Scenario 3: Different Profiles
Test with various profiles:

**Profile A - Master Number**
- Name: "Alexandra Smith"
- Birth Date: "1985-11-29" (Life Path 11)

**Profile B - Regular Numbers**
- Name: "Michael Johnson" 
- Birth Date: "1992-06-15" (Life Path 7)

**Profile C - Multiple Master Numbers**
- Name: "Sarah Elizabeth Wilson"
- Birth Date: "1988-02-11" (Multiple master numbers)

### Scenario 4: Error Handling Demo
1. Try invalid dates: "invalid-date"
2. Leave name empty
3. Enter special characters
4. Test network disconnection

### Scenario 5: Mobile Responsive Demo
1. Open on mobile device
2. Test portrait and landscape modes
3. Verify touch interactions
4. Check chat scrolling

## Expected Results

### Successful Calculation Response
```json
{
  "life_path": {
    "number": 5,
    "interpretation": "You are adventurous and freedom-loving..."
  },
  "destiny": {
    "number": 8, 
    "interpretation": "You are ambitious and goal-oriented..."
  },
  "soul_urge": {
    "number": 3,
    "interpretation": "You are creative and expressive..."
  },
  "personality": {
    "number": 5,
    "interpretation": "You appear dynamic and energetic..."
  },
  "master_numbers": [],
  "summary": "Your numerology profile shows..."
}
```

### Chat Response Example
```json
{
  "response": "Your Life Path number 5 indicates a natural desire for freedom and adventure. This suggests you thrive in careers that offer variety, travel, or entrepreneurial opportunities...",
  "message_id": "msg-123",
  "timestamp": "2024-01-01T00:00:00Z",
  "context_used": true
}
```

## Troubleshooting Demo Issues

### Backend Not Starting
```bash
# Check Python environment
cd backend
source venv/bin/activate
python --version

# Check dependencies
pip list | grep fastapi

# Check for port conflicts
lsof -i:8000
```

### Frontend Build Issues
```bash
# Clean and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check Angular version
ng version
```

### Docker Issues
```bash
# Check Docker status
docker --version
docker-compose --version

# View Docker logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose down
docker-compose up --build
```

### Port Conflicts
```bash
# Kill processes on port 8000
lsof -ti:8000 | xargs kill -9

# Kill processes on port 4200
lsof -ti:4200 | xargs kill -9
```

## Performance Benchmarks

### Expected Response Times
- Health endpoint: < 50ms
- Numerology calculation: < 200ms
- Chat response: < 500ms
- Page load: < 3 seconds

### Resource Usage
- Backend memory: ~50MB
- Frontend build size: ~474KB
- Docker containers: ~200MB total

## Demo Customization

### Adding New Demo Data
1. Edit `backend/app/services/numerology_calculator.py`
2. Add new interpretation texts
3. Update chat response templates
4. Test with different birth dates and names

### UI Theme Customization
1. Edit `frontend/src/styles/globals.scss`
2. Modify color variables
3. Update Material theme configuration
4. Test responsive breakpoints

## Live Demo URLs

When deployed, the application will be available at:
- **Production**: Your deployed domain
- **Development**: http://localhost:4200
- **API Docs**: http://your-domain/docs
- **Health Check**: http://your-domain/health

This completes the demo setup. The application showcases a full-stack numerology chat system with modern web technologies!