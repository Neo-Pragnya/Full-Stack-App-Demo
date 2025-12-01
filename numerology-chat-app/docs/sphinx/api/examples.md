# API Examples

Practical examples for using the Numerology Chat API with various programming languages and tools.

## 🚀 Quick Start Examples

### Basic Calculation Request

**Python with requests:**
```python
import requests
import json
from datetime import date

# API endpoint
api_base = "http://localhost:8000"

# Calculate numerology profile
def calculate_numerology(name: str, birth_date: str):
    url = f"{api_base}/api/v1/calculate"
    payload = {
        "full_name": name,
        "birth_date": birth_date
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result['data']
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

# Example usage
profile = calculate_numerology("John Michael Smith", "1990-01-15")
if profile:
    print(f"Life Path: {profile['life_path']['number']}")
    print(f"Destiny: {profile['destiny']['number']}")
    print(f"Soul Urge: {profile['soul_urge']['number']}")
```

**JavaScript with fetch:**
```javascript
// Calculate numerology profile
async function calculateNumerology(fullName, birthDate) {
    const apiBase = 'http://localhost:8000';
    const url = `${apiBase}/api/v1/calculate`;
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                full_name: fullName,
                birth_date: birthDate
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        return result.data;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Example usage
calculateNumerology('John Michael Smith', '1990-01-15')
    .then(profile => {
        if (profile) {
            console.log(`Life Path: ${profile.life_path.number}`);
            console.log(`Destiny: ${profile.destiny.number}`);
            console.log(`Soul Urge: ${profile.soul_urge.number}`);
        }
    });
```

**cURL:**
```bash
# Calculate numerology profile
curl -X POST "http://localhost:8000/api/v1/calculate" \
     -H "Content-Type: application/json" \
     -d '{
       "full_name": "John Michael Smith",
       "birth_date": "1990-01-15"
     }'
```

---

## 💬 Chat Examples

### Simple Chat Interaction

**Python:**
```python
import uuid
import requests

class NumerologyChat:
    def __init__(self, api_base="http://localhost:8000"):
        self.api_base = api_base
        self.session_id = str(uuid.uuid4())
        
    def send_message(self, message: str, context: dict = None):
        url = f"{self.api_base}/api/v1/chat"
        payload = {
            "message": message,
            "session_id": self.session_id,
            "context": context
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result['data']
        else:
            return {"error": "Failed to get response"}
    
    def get_history(self, limit=10):
        url = f"{self.api_base}/api/v1/chat/history/{self.session_id}"
        params = {"limit": limit}
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()['data']
        return None

# Example usage
chat = NumerologyChat()

# Send first message
response1 = chat.send_message("Hello! I want to learn about numerology.")
print("Assistant:", response1['message'])

# Send message with context
context = {
    "full_name": "John Smith",
    "birth_date": "1990-01-15",
    "previous_calculation": True
}

response2 = chat.send_message("What does my life path number mean?", context)
print("Assistant:", response2['message'])
print("Suggestions:", response2['suggestions'])

# Get chat history
history = chat.get_history()
print(f"Total messages: {history['total_messages']}")
```

**JavaScript (Node.js):**
```javascript
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

class NumerologyChat {
    constructor(apiBase = 'http://localhost:8000') {
        this.apiBase = apiBase;
        this.sessionId = uuidv4();
    }
    
    async sendMessage(message, context = null) {
        try {
            const response = await axios.post(`${this.apiBase}/api/v1/chat`, {
                message: message,
                session_id: this.sessionId,
                context: context
            });
            
            return response.data.data;
        } catch (error) {
            console.error('Error sending message:', error.response?.data || error.message);
            return { error: 'Failed to get response' };
        }
    }
    
    async getHistory(limit = 10) {
        try {
            const response = await axios.get(
                `${this.apiBase}/api/v1/chat/history/${this.sessionId}`,
                { params: { limit } }
            );
            
            return response.data.data;
        } catch (error) {
            console.error('Error getting history:', error.response?.data || error.message);
            return null;
        }
    }
}

// Example usage
async function example() {
    const chat = new NumerologyChat();
    
    // Send first message
    const response1 = await chat.sendMessage("Hello! I want to learn about numerology.");
    console.log("Assistant:", response1.message);
    
    // Send message with context
    const context = {
        full_name: "John Smith",
        birth_date: "1990-01-15",
        previous_calculation: true
    };
    
    const response2 = await chat.sendMessage("What does my life path number mean?", context);
    console.log("Assistant:", response2.message);
    console.log("Suggestions:", response2.suggestions);
    
    // Get chat history
    const history = await chat.getHistory();
    console.log(`Total messages: ${history.total_messages}`);
}

example();
```

---

## 📊 Event Tracking Examples

### Track User Interactions

**Python:**
```python
def track_user_event(session_id: str, event_type: str, data: dict = None):
    url = f"{api_base}/api/v1/track-event"
    payload = {
        "event_type": event_type,
        "session_id": session_id,
        "data": data or {}
    }
    
    response = requests.post(url, json=payload)
    return response.status_code == 200

# Example usage
session_id = "user-session-12345"

# Track calculation request
track_user_event(session_id, "calculation_request", {
    "name_length": len("John Michael Smith"),
    "has_middle_name": True
})

# Track positive feedback
track_user_event(session_id, "thumbs_up", {
    "message_id": "msg_67890",
    "rating": "positive",
    "feedback_text": "Very helpful explanation"
})

# Track tab navigation
track_user_event(session_id, "tab_click", {
    "tab_name": "life_path",
    "previous_tab": "summary"
})

# Track session end
track_user_event(session_id, "session_end", {
    "duration": 1847,
    "interactions": 15
})
```

**JavaScript:**
```javascript
async function trackEvent(sessionId, eventType, data = {}) {
    try {
        const response = await fetch(`${apiBase}/api/v1/track-event`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                event_type: eventType,
                session_id: sessionId,
                data: data
            })
        });
        
        return response.ok;
    } catch (error) {
        console.error('Error tracking event:', error);
        return false;
    }
}

// Example usage
const sessionId = 'user-session-12345';

// Track different events
await trackEvent(sessionId, 'calculation_request', {
    name_length: 'John Michael Smith'.length,
    has_middle_name: true
});

await trackEvent(sessionId, 'thumbs_up', {
    message_id: 'msg_67890',
    rating: 'positive'
});
```

---

## 🔍 Analytics Examples

### Get Session Analytics

**Python:**
```python
def get_session_analytics(session_id: str):
    url = f"{api_base}/api/v1/analytics/{session_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['data']
    return None

# Example usage
analytics = get_session_analytics("user-session-12345")

if analytics:
    print(f"Session Duration: {analytics['session_duration']} seconds")
    print(f"Total Interactions: {analytics['total_interactions']}")
    print(f"Calculations: {analytics['calculations_performed']}")
    print(f"Messages: {analytics['messages_sent']}")
    print(f"Satisfaction Rate: {analytics['feedback_stats']['satisfaction_rate']:.1%}")
    print(f"Engagement Score: {analytics['engagement_score']}/10")
    
    print("\nMost Viewed Tabs:")
    for tab in analytics['most_viewed_tabs']:
        print(f"  {tab['tab']}: {tab['views']} views")
```

---

## 🛠️ Error Handling Examples

### Robust Error Handling

**Python:**
```python
import requests
from typing import Optional, Dict, Any

class NumerologyAPIError(Exception):
    """Custom exception for API errors"""
    def __init__(self, status_code: int, error_data: dict):
        self.status_code = status_code
        self.error_data = error_data
        super().__init__(f"API Error {status_code}: {error_data.get('message', 'Unknown error')}")

class NumerologyAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(method, url, **kwargs)
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return data['data']
                else:
                    raise NumerologyAPIError(response.status_code, data['error'])
            else:
                # Handle HTTP errors
                try:
                    error_data = response.json()
                    raise NumerologyAPIError(response.status_code, error_data.get('error', {}))
                except ValueError:
                    # Response is not JSON
                    raise NumerologyAPIError(response.status_code, {
                        'message': f'HTTP {response.status_code}',
                        'details': response.text
                    })
                    
        except requests.exceptions.ConnectionError:
            raise NumerologyAPIError(0, {
                'message': 'Connection failed',
                'details': 'Could not connect to API server'
            })
        except requests.exceptions.Timeout:
            raise NumerologyAPIError(0, {
                'message': 'Request timeout',
                'details': 'API request took too long'
            })
    
    def calculate_numerology(self, full_name: str, birth_date: str) -> Optional[Dict[Any, Any]]:
        try:
            return self._make_request(
                'POST',
                '/api/v1/calculate',
                json={'full_name': full_name, 'birth_date': birth_date}
            )
        except NumerologyAPIError as e:
            print(f"Calculation failed: {e}")
            if e.error_data.get('details'):
                print(f"Details: {e.error_data['details']}")
            return None
    
    def send_chat_message(self, message: str, session_id: str, context: dict = None) -> Optional[Dict[Any, Any]]:
        try:
            payload = {
                'message': message,
                'session_id': session_id
            }
            if context:
                payload['context'] = context
                
            return self._make_request('POST', '/api/v1/chat', json=payload)
        except NumerologyAPIError as e:
            print(f"Chat message failed: {e}")
            return None

# Example usage with error handling
api = NumerologyAPI()

# Test calculation with error handling
result = api.calculate_numerology("", "invalid-date")  # This will fail
if result:
    print("Calculation successful:", result['life_path']['number'])
else:
    print("Calculation failed - check your input")

# Valid calculation
result = api.calculate_numerology("John Smith", "1990-01-15")
if result:
    print("Life Path Number:", result['life_path']['number'])
```

**JavaScript with comprehensive error handling:**
```javascript
class NumerologyAPIError extends Error {
    constructor(statusCode, errorData) {
        super(`API Error ${statusCode}: ${errorData.message || 'Unknown error'}`);
        this.statusCode = statusCode;
        this.errorData = errorData;
    }
}

class NumerologyAPI {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async makeRequest(method, endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            const data = await response.json();
            
            if (response.ok && data.status === 'success') {
                return data.data;
            } else {
                throw new NumerologyAPIError(response.status, data.error || {});
            }
            
        } catch (error) {
            if (error instanceof NumerologyAPIError) {
                throw error;
            }
            
            // Network or other errors
            throw new NumerologyAPIError(0, {
                message: 'Network error',
                details: error.message
            });
        }
    }
    
    async calculateNumerology(fullName, birthDate) {
        try {
            return await this.makeRequest('POST', '/api/v1/calculate', {
                body: JSON.stringify({
                    full_name: fullName,
                    birth_date: birthDate
                })
            });
        } catch (error) {
            console.error('Calculation failed:', error.message);
            if (error.errorData.details) {
                console.error('Details:', error.errorData.details);
            }
            return null;
        }
    }
    
    async sendChatMessage(message, sessionId, context = null) {
        try {
            const payload = { message, session_id: sessionId };
            if (context) payload.context = context;
            
            return await this.makeRequest('POST', '/api/v1/chat', {
                body: JSON.stringify(payload)
            });
        } catch (error) {
            console.error('Chat message failed:', error.message);
            return null;
        }
    }
}

// Example usage
const api = new NumerologyAPI();

// Test with error handling
api.calculateNumerology('', 'invalid-date')
    .then(result => {
        if (result) {
            console.log('Calculation successful:', result.life_path.number);
        } else {
            console.log('Calculation failed - check your input');
        }
    });

// Valid calculation
api.calculateNumerology('John Smith', '1990-01-15')
    .then(result => {
        if (result) {
            console.log('Life Path Number:', result.life_path.number);
        }
    });
```

---

## 🧪 Testing Examples

### Unit Tests with pytest

**test_api.py:**
```python
import pytest
import requests
from datetime import date

API_BASE = "http://localhost:8000"

class TestNumerologyAPI:
    
    def test_health_check(self):
        response = requests.get(f"{API_BASE}/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'version' in data
    
    def test_valid_calculation(self):
        payload = {
            "full_name": "John Michael Smith",
            "birth_date": "1990-01-15"
        }
        response = requests.post(f"{API_BASE}/api/v1/calculate", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'success'
        assert 'life_path' in data['data']
        assert 'destiny' in data['data']
        assert 'soul_urge' in data['data']
    
    def test_invalid_name(self):
        payload = {
            "full_name": "",
            "birth_date": "1990-01-15"
        }
        response = requests.post(f"{API_BASE}/api/v1/calculate", json=payload)
        assert response.status_code == 400
        
        data = response.json()
        assert data['status'] == 'error'
        assert 'full_name' in data['error']['details']['field']
    
    def test_invalid_date(self):
        payload = {
            "full_name": "John Smith",
            "birth_date": "invalid-date"
        }
        response = requests.post(f"{API_BASE}/api/v1/calculate", json=payload)
        assert response.status_code == 400
        
        data = response.json()
        assert data['status'] == 'error'
    
    def test_chat_message(self):
        payload = {
            "message": "Hello",
            "session_id": "test-session-123"
        }
        response = requests.post(f"{API_BASE}/api/v1/chat", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'success'
        assert 'message' in data['data']
        assert 'message_id' in data['data']
    
    def test_event_tracking(self):
        payload = {
            "event_type": "thumbs_up",
            "session_id": "test-session-123",
            "data": {"message_id": "msg_123"}
        }
        response = requests.post(f"{API_BASE}/api/v1/track-event", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'success'
        assert data['data']['recorded'] is True

# Run tests
if __name__ == "__main__":
    pytest.main([__file__])
```

### Integration Tests with Jest

**api.test.js:**
```javascript
const axios = require('axios');

const API_BASE = 'http://localhost:8000';

describe('Numerology API', () => {
    
    test('health check returns healthy status', async () => {
        const response = await axios.get(`${API_BASE}/health`);
        expect(response.status).toBe(200);
        expect(response.data.status).toBe('healthy');
        expect(response.data.version).toBeDefined();
    });
    
    test('valid calculation returns numerology data', async () => {
        const payload = {
            full_name: 'John Michael Smith',
            birth_date: '1990-01-15'
        };
        
        const response = await axios.post(`${API_BASE}/api/v1/calculate`, payload);
        expect(response.status).toBe(200);
        expect(response.data.status).toBe('success');
        expect(response.data.data.life_path).toBeDefined();
        expect(response.data.data.destiny).toBeDefined();
        expect(response.data.data.soul_urge).toBeDefined();
    });
    
    test('invalid name returns validation error', async () => {
        const payload = {
            full_name: '',
            birth_date: '1990-01-15'
        };
        
        try {
            await axios.post(`${API_BASE}/api/v1/calculate`, payload);
        } catch (error) {
            expect(error.response.status).toBe(400);
            expect(error.response.data.status).toBe('error');
        }
    });
    
    test('chat message returns response', async () => {
        const payload = {
            message: 'Hello',
            session_id: 'test-session-123'
        };
        
        const response = await axios.post(`${API_BASE}/api/v1/chat`, payload);
        expect(response.status).toBe(200);
        expect(response.data.status).toBe('success');
        expect(response.data.data.message).toBeDefined();
        expect(response.data.data.message_id).toBeDefined();
    });
    
    test('event tracking records successfully', async () => {
        const payload = {
            event_type: 'thumbs_up',
            session_id: 'test-session-123',
            data: { message_id: 'msg_123' }
        };
        
        const response = await axios.post(`${API_BASE}/api/v1/track-event`, payload);
        expect(response.status).toBe(200);
        expect(response.data.status).toBe('success');
        expect(response.data.data.recorded).toBe(true);
    });
});
```

---

## 📱 Frontend Integration Examples

### Angular Service Example

**numerology.service.ts:**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

export interface CalculationRequest {
  full_name: string;
  birth_date: string;
}

export interface ApiResponse<T> {
  status: string;
  data: T;
  error?: any;
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class NumerologyService {
  private apiBase = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  calculateNumerology(request: CalculationRequest): Observable<any> {
    return this.http.post<ApiResponse<any>>(`${this.apiBase}/api/v1/calculate`, request)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  sendChatMessage(message: string, sessionId: string, context?: any): Observable<any> {
    const payload = { message, session_id: sessionId, context };
    return this.http.post<ApiResponse<any>>(`${this.apiBase}/api/v1/chat`, payload)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  trackEvent(eventType: string, sessionId: string, data?: any): Observable<any> {
    const payload = { event_type: eventType, session_id: sessionId, data };
    return this.http.post<ApiResponse<any>>(`${this.apiBase}/api/v1/track-event`, payload)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An error occurred';
    
    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = error.error.message;
    } else {
      // Server-side error
      if (error.error && error.error.error) {
        errorMessage = error.error.error.message;
      }
    }
    
    return throwError(errorMessage);
  }
}
```

### React Hook Example

**useNumerology.js:**
```javascript
import { useState, useCallback } from 'react';

const API_BASE = 'http://localhost:8000';

export function useNumerology() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const makeRequest = useCallback(async (endpoint, options = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
        },
        ...options
      });
      
      const data = await response.json();
      
      if (!response.ok || data.status !== 'success') {
        throw new Error(data.error?.message || 'Request failed');
      }
      
      setLoading(false);
      return data.data;
    } catch (err) {
      setError(err.message);
      setLoading(false);
      throw err;
    }
  }, []);

  const calculateNumerology = useCallback(async (fullName, birthDate) => {
    return makeRequest('/api/v1/calculate', {
      method: 'POST',
      body: JSON.stringify({
        full_name: fullName,
        birth_date: birthDate
      })
    });
  }, [makeRequest]);

  const sendChatMessage = useCallback(async (message, sessionId, context) => {
    return makeRequest('/api/v1/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        session_id: sessionId,
        context
      })
    });
  }, [makeRequest]);

  const trackEvent = useCallback(async (eventType, sessionId, data) => {
    return makeRequest('/api/v1/track-event', {
      method: 'POST',
      body: JSON.stringify({
        event_type: eventType,
        session_id: sessionId,
        data
      })
    });
  }, [makeRequest]);

  return {
    loading,
    error,
    calculateNumerology,
    sendChatMessage,
    trackEvent
  };
}
```

These examples provide comprehensive guidance for integrating with the Numerology Chat API across different programming languages, frameworks, and use cases.