# Quick Start Guide

Get up and running with the Numerology Chat Application in just a few minutes!

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker Desktop** 4.0+ (recommended approach)
- **Node.js** 18+ and **Python** 3.11+ (for local development)
- **Git** for cloning the repository

## 🚀 Option 1: Docker Quick Start (Recommended)

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd numerology-chat-app
```

### 2. Start the Application
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Start production environment
./scripts/start-docker.sh
```

### 3. Access the Application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

That's it! The application is now running.

## 🔧 Option 2: Local Development Setup

### 1. Environment Setup
```bash
# Run the setup script
./scripts/setup-dev.sh
```

### 2. Start Development Services
```bash
# Start both frontend and backend locally
./scripts/start-dev.sh --local
```

### 3. Access Development Environment
- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 First Steps - Using the Application

### 1. Calculate Your Numerology Profile
1. Open http://localhost:4200 (or http://localhost for Docker)
2. Enter your **full name** (e.g., "John Michael Smith")
3. Enter your **birth date** in YYYY-MM-DD format (e.g., "1990-01-15")
4. Click **"Calculate"** to generate your numerology profile

### 2. Explore Your Results
Navigate through the different tabs to explore your numbers:

- **📊 Summary**: Overview of all your key numbers
- **🎯 Core Numbers**: Life Path, Destiny, Soul Urge, Personality
- **🔬 Advanced**: Birth Day, Balance, Hidden Passion numbers
- **🔄 Life Cycles**: Personal Year, Challenges, Pinnacles
- **🕉️ Spiritual**: Karmic Lessons and spiritual insights
- **⏰ Timing**: Personal year analysis and timing guidance

### 3. Chat with the Assistant
Use the chat interface to ask questions about your numerology:

**Example Questions:**
- "What does my Life Path number mean for my career?"
- "How do my core numbers work together?"
- "Tell me about my karmic lessons"
- "What should I focus on this personal year?"

### 4. Provide Feedback
Rate the chat responses using the thumbs up/down buttons to help improve the experience.

## 🧪 Quick API Test

Test the backend API directly:

```bash
# Health check
curl http://localhost:8000/health

# Calculate numerology
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "birth_date": "1990-01-01"
  }'

# Start a chat conversation
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, can you help me understand my numerology?",
    "session_id": "test-123"
  }'
```

## 🛠️ Development Commands

Once you have the application running, here are useful commands:

```bash
# Run tests
./scripts/test.sh

# Stop all services
./scripts/stop.sh

# Stop and clean up (removes data)
./scripts/stop.sh --clean

# View logs (Docker mode)
docker-compose logs -f

# Backend logs only
docker-compose logs backend

# Frontend logs only  
docker-compose logs frontend
```

## 🐛 Troubleshooting

### Port Conflicts
If you encounter port conflicts:

```bash
# Check what's using port 8000
lsof -i:8000

# Check what's using port 4200
lsof -i:4200

# Kill processes if needed
./scripts/stop.sh --clean
```

### Docker Issues
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# Check container status
docker-compose ps

# View container logs
docker-compose logs [service-name]
```

### Backend Issues
```bash
# Check Python environment
cd backend
source venv/bin/activate
python --version

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues
```bash
# Clean install
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check Angular version
ng version
```

## ✅ Verification Checklist

Confirm everything is working:

- [ ] Frontend loads at http://localhost:4200 (or :80 for Docker)
- [ ] Backend API responds at http://localhost:8000/health
- [ ] Can calculate numerology for a test name/date
- [ ] Chat interface responds to messages
- [ ] Can navigate between different tabs
- [ ] Thumbs up/down feedback works
- [ ] Mobile-responsive design works

## 📚 Next Steps

Now that you have the application running:

1. **Explore the API**: Visit http://localhost:8000/docs for interactive API documentation
2. **Read the guides**: Check out the API reference and documentation guides
3. **Try examples**: Look at the API examples for common use cases
4. **Customize**: Learn how to modify and extend the application

## 🆘 Getting Help

If you encounter issues:

1. Check the documentation guides
2. Review the logs using the commands above
3. Check the GitHub repository for issues
4. Refer to the comprehensive API documentation

---

**🎉 Congratulations!** You now have a fully functional numerology chat application running locally. Enjoy exploring the mystical world of numbers!