#!/usr/bin/env python3
"""
Live Demo of Numerology Chat Application
Shows both backend API and frontend functionality
"""
import requests
import json
import time

def demo_backend_api():
    """Demonstrate the backend API functionality"""
    base_url = "http://localhost:8000"
    
    print("🔍 BACKEND API DEMO")
    print("=" * 50)
    
    try:
        # Test 1: Health Check
        print("\n1. 🏥 Health Check")
        print("   GET /health")
        response = requests.get(f"{base_url}/health")
        print(f"   ✅ Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   📋 Response: {response.json()}")
        
        # Test 2: Get available endpoints
        print("\n2. 📚 Available Endpoints")
        print("   GET /")
        response = requests.get(f"{base_url}/")
        print(f"   ✅ Status: {response.status_code}")
        
        # Test 3: API Documentation
        print("\n3. 📖 Interactive API Documentation")
        print("   Available at: http://localhost:8000/docs")
        print("   This provides Swagger UI for testing all endpoints")
        
        # Test 4: Test numerology calculation endpoint (if it exists)
        print("\n4. 🔢 Testing Numerology Calculation")
        print("   POST /calculate")
        person_data = {
            "name": "John Doe", 
            "birth_date": "1990-01-01"
        }
        
        # Check if endpoint exists by trying different possible paths
        endpoints_to_try = ['/calculate', '/numerology', '/api/calculate']
        
        for endpoint in endpoints_to_try:
            try:
                response = requests.post(f"{base_url}{endpoint}", json=person_data)
                if response.status_code != 404:
                    print(f"   ✅ Found endpoint: {endpoint}")
                    print(f"   📊 Status: {response.status_code}")
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   🎯 Sample calculation result:")
                        for key, value in result.items():
                            if isinstance(value, dict):
                                print(f"      {key}: {value.get('number')} - {value.get('interpretation', '')[:50]}...")
                            else:
                                print(f"      {key}: {value}")
                    break
            except:
                continue
        else:
            print("   ⚠️ Numerology calculation endpoint not found at standard paths")
        
        print("\n" + "="*50)
        print("🌐 FRONTEND DEMO")
        print("="*50)
        print("\n🚀 Frontend is running at: http://localhost:4200")
        print("\n📋 Demo Steps for Frontend:")
        print("1. Open http://localhost:4200 in your browser")
        print("2. Enter your full name (e.g., 'John Doe')")
        print("3. Enter your birth date (e.g., '1990-01-01')")
        print("4. Click 'Calculate' to see numerology analysis")
        print("5. Explore different tabs:")
        print("   • Summary: Overview of all numbers")
        print("   • Core Numbers: Life Path, Destiny, Soul Urge, Personality")
        print("   • Advanced: Additional calculations")
        print("   • Life Cycles: Personal Year, Challenges, Pinnacles")
        print("   • Spiritual: Karmic Lessons")
        print("   • Timing: Personal year analysis")
        print("6. Use the chat interface:")
        print("   • Ask: 'What does my life path number mean?'")
        print("   • Try: 'How do my numbers work together?'")
        print("   • Give feedback with thumbs up/down")
        
        print("\n🎨 UI Features:")
        print("• Responsive Material Design")
        print("• Real-time chat interface")
        print("• Interactive feedback system")
        print("• Comprehensive numerology analysis")
        print("• Tab-based navigation")
        print("• Mobile-friendly design")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend at http://localhost:8000")
        print("   Make sure the backend server is running:")
        print("   cd backend && ./venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_project_structure():
    """Show the project architecture"""
    print("\n📁 PROJECT ARCHITECTURE")
    print("=" * 50)
    print("""
    numerology-chat-app/
    ├── 🐍 backend/                 # FastAPI Backend
    │   ├── app/
    │   │   ├── main.py            # API entry point  
    │   │   ├── models.py          # Data models
    │   │   └── services/          # Business logic
    │   │       ├── numerology_calculator.py
    │   │       ├── chat_service.py
    │   │       └── event_tracker.py
    │   ├── requirements.txt       # Python dependencies
    │   └── Dockerfile            # Backend container
    │
    ├── 🅰️ frontend/               # Angular Frontend  
    │   ├── src/app/
    │   │   ├── components/       # UI components
    │   │   ├── services/         # API communication
    │   │   └── models/           # TypeScript interfaces
    │   ├── package.json          # Node dependencies
    │   └── Dockerfile           # Frontend container
    │
    ├── 🛠️ scripts/               # Automation
    │   ├── setup-dev.sh         # Environment setup
    │   ├── start-dev.sh         # Start development
    │   ├── start-docker.sh      # Start production
    │   └── test.sh              # Run tests
    │
    └── 📚 docs/                  # Documentation
        ├── README.md            # Project overview
        ├── API.md               # API documentation  
        └── DEVELOPMENT.md       # Developer guide
    """)

if __name__ == "__main__":
    print("🌟 NUMEROLOGY CHAT APPLICATION - LIVE DEMO")
    print("=" * 60)
    
    show_project_structure()
    demo_backend_api()
    
    print("\n" + "="*60)
    print("🎉 Demo completed!")
    print("💡 Open http://localhost:4200 to interact with the full application")
    print("📚 Visit http://localhost:8000/docs for interactive API documentation")