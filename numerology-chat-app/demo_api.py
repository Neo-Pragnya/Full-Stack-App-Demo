#!/usr/bin/env python3
"""
Quick demo script for Numerology Chat Application API
"""
import requests
import json
import time
import subprocess
import os

def start_backend():
    """Start the backend server"""
    os.chdir('/Users/abhikanap/Documents/Repositories/Full-Stack-App-Demo/numerology-chat-app/backend')
    cmd = ['./venv/bin/python', '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000']
    return subprocess.Popen(cmd)

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Numerology Chat Application API")
    print("=" * 50)
    
    # Wait for server to start
    time.sleep(2)
    
    try:
        # Test 1: Health Check
        print("\n1. Testing Health Endpoint...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test 2: Numerology Calculation
        print("\n2. Testing Numerology Calculation...")
        person_data = {
            "name": "John Doe",
            "birth_date": "1990-01-01"
        }
        response = requests.post(f"{base_url}/calculate", json=person_data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        
        print(f"   Life Path: {result.get('life_path', {}).get('number')} - {result.get('life_path', {}).get('interpretation', '')[:50]}...")
        print(f"   Destiny: {result.get('destiny', {}).get('number')} - {result.get('destiny', {}).get('interpretation', '')[:50]}...")
        print(f"   Soul Urge: {result.get('soul_urge', {}).get('number')} - {result.get('soul_urge', {}).get('interpretation', '')[:50]}...")
        
        # Test 3: Chat Message
        print("\n3. Testing Chat Interface...")
        chat_data = {
            "message": "Tell me about my life path number",
            "session_id": "demo-session-123",
            "context": person_data
        }
        response = requests.post(f"{base_url}/chat", json=chat_data)
        print(f"   Status: {response.status_code}")
        chat_result = response.json()
        print(f"   Response: {chat_result.get('response', '')[:100]}...")
        
        # Test 4: Event Tracking
        print("\n4. Testing Event Tracking...")
        event_data = {
            "event_type": "thumbs_up",
            "session_id": "demo-session-123",
            "data": {
                "message_id": chat_result.get('message_id'),
                "rating": "positive"
            }
        }
        response = requests.post(f"{base_url}/track-event", json=event_data)
        print(f"   Status: {response.status_code}")
        print(f"   Event ID: {response.json().get('event_id')}")
        
        print("\n✅ All API tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend. Make sure it's running on port 8000.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    # Start backend
    print("🚀 Starting backend server...")
    backend_process = start_backend()
    
    try:
        test_api()
    finally:
        # Clean up
        print("\n🛑 Stopping backend server...")
        backend_process.terminate()
        backend_process.wait()