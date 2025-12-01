# API Endpoints

Complete reference for all REST API endpoints in the Numerology Chat Application.

## 🏥 Health & Status

### Health Check
<div class="api-endpoint">
<span class="method get">GET</span> <code>/health</code>
</div>

Check if the application is running and healthy.

**Response Example:**
```json
{
  "status": "healthy",
  "message": "Service is running",
  "timestamp": "2025-11-30T22:40:02.184375",
  "version": "1.0.0",
  "uptime": "2h 15m 30s"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is down or unhealthy

---

## 🔢 Numerology Calculations

### Calculate Numerology Profile
<div class="api-endpoint">
<span class="method post">POST</span> <code>/api/v1/calculate</code>
</div>

Calculate a complete numerology profile for a person.

**Request Body:**
```json
{
  "full_name": "John Michael Smith",
  "birth_date": "1990-01-15"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `full_name` | string | Yes | Full name as on birth certificate |
| `birth_date` | string | Yes | Date in YYYY-MM-DD format |

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "life_path": {
      "number": 5,
      "calculation": "1 + 5 + 1990 = 1996 → 5",
      "is_master": false,
      "interpretation": "You are adventurous and freedom-loving..."
    },
    "destiny": {
      "number": 8,
      "calculation": "Sum of all letters = 89 → 8",
      "is_master": false,
      "letter_breakdown": {
        "J": {"value": 1, "count": 1},
        "O": {"value": 6, "count": 1}
      },
      "interpretation": "Your life purpose is material success..."
    },
    "soul_urge": {
      "number": 3,
      "calculation": "Vowels (O, I, A, E, I) = 21 → 3",
      "is_master": false,
      "vowels_used": ["O", "I", "A", "E", "I"],
      "interpretation": "You desire creative expression..."
    },
    "personality": {
      "number": 5,
      "calculation": "Consonants = 68 → 5",
      "is_master": false,
      "consonants_used": ["J", "H", "N", "M", "C", "H", "L"],
      "interpretation": "Others see you as dynamic..."
    },
    "birth_day": {
      "number": 6,
      "calculation": "Day of birth: 15 → 6",
      "is_master": false,
      "interpretation": "You are naturally nurturing..."
    },
    "personal_year": {
      "number": 8,
      "calculation": "1 + 5 + 2025 = 2031 → 8",
      "year": 2025,
      "interpretation": "Focus on business and achievement..."
    },
    "challenge_numbers": {
      "first": 4,
      "second": 4,
      "third": 0,
      "fourth": 0,
      "calculation": "Based on day(15), month(1), year(1990)"
    },
    "pinnacle_numbers": {
      "first": 6,
      "second": 1,
      "third": 7,
      "fourth": 2,
      "calculation": "Life periods based on birth date"
    },
    "karmic_lessons": {
      "missing_numbers": [2, 7, 9],
      "present_numbers": [1, 3, 4, 5, 6, 8],
      "calculation": "Missing numbers from name analysis"
    },
    "master_numbers": [11, 22],
    "lucky_numbers": [1, 5, 8, 15, 24],
    "hidden_passion": {
      "number": [1, 8],
      "calculation": "Most frequent letters in name",
      "frequency_map": {"1": 3, "8": 3, "5": 2}
    }
  },
  "timestamp": "2025-11-30T22:40:02.184375"
}
```

**Status Codes:**
- `200 OK` - Calculation successful
- `400 Bad Request` - Invalid input data
- `422 Unprocessable Entity` - Validation errors

**Error Example:**
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid birth date format",
    "details": {
      "field": "birth_date",
      "expected_format": "YYYY-MM-DD",
      "provided": "1990/01/15"
    }
  }
}
```

---

## 💬 Chat Interface

### Send Chat Message
<div class="api-endpoint">
<span class="method post">POST</span> <code>/api/v1/chat</code>
</div>

Send a message to the numerology chat assistant.

**Request Body:**
```json
{
  "message": "What does my life path number mean?",
  "session_id": "user-session-12345",
  "context": {
    "full_name": "John Smith",
    "birth_date": "1990-01-15",
    "previous_calculation": true
  }
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User's message to the assistant |
| `session_id` | string | Yes | Unique session identifier |
| `context` | object | No | Additional context for personalized responses |

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "message": "Your Life Path number 5 indicates a natural desire for freedom and adventure. This suggests you thrive in careers that offer variety, travel, or entrepreneurial opportunities...",
    "type": "numerology_explanation",
    "message_id": "msg_67890",
    "suggestions": [
      "Tell me about my destiny number",
      "How do my numbers work together?",
      "What about my personal year?"
    ],
    "context_used": true
  },
  "timestamp": "2025-11-30T22:40:05.123456"
}
```

**Message Types:**
- `greeting` - Welcome message
- `numerology_explanation` - Explanation of numbers
- `guidance` - Personal guidance
- `clarification` - Request for more info
- `error` - Error or misunderstanding

### Get Chat History
<div class="api-endpoint">
<span class="method get">GET</span> <code>/api/v1/chat/history/{session_id}</code>
</div>

Retrieve chat history for a session.

**Path Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Session ID to retrieve |

**Query Parameters:**
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | integer | 50 | Maximum messages to return |
| `offset` | integer | 0 | Number of messages to skip |

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "session_id": "user-session-12345",
    "messages": [
      {
        "id": "msg_123",
        "type": "user",
        "content": "Hello",
        "timestamp": "2025-11-30T22:30:00Z"
      },
      {
        "id": "msg_124",
        "type": "assistant",
        "content": "Welcome! I'm here to help...",
        "timestamp": "2025-11-30T22:30:01Z",
        "rating": "positive"
      }
    ],
    "total_messages": 12,
    "session_created": "2025-11-30T22:29:00Z"
  }
}
```

---

## 📊 Event Tracking

### Track User Event
<div class="api-endpoint">
<span class="method post">POST</span> <code>/api/v1/track-event</code>
</div>

Track user interactions and feedback.

**Request Body:**
```json
{
  "event_type": "thumbs_up",
  "session_id": "user-session-12345",
  "data": {
    "message_id": "msg_67890",
    "rating": "positive",
    "feedback_text": "Very helpful explanation"
  }
}
```

**Event Types:**
- `thumbs_up` - Positive feedback on response
- `thumbs_down` - Negative feedback on response
- `tab_click` - Navigation between tabs
- `calculation_request` - Numerology calculation performed
- `chat_message` - Message sent to assistant
- `session_start` - New session created
- `session_end` - Session terminated

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "event_id": "evt_456789",
    "recorded": true
  },
  "timestamp": "2025-11-30T22:40:07.987654"
}
```

### Get Session Analytics
<div class="api-endpoint">
<span class="method get">GET</span> <code>/api/v1/analytics/{session_id}</code>
</div>

Get analytics data for a specific session.

**Path Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Session ID to analyze |

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "session_id": "user-session-12345",
    "session_duration": 1847,
    "total_interactions": 15,
    "calculations_performed": 2,
    "messages_sent": 8,
    "feedback_stats": {
      "positive": 6,
      "negative": 1,
      "total": 7,
      "satisfaction_rate": 0.857
    },
    "most_viewed_tabs": [
      {"tab": "life_path", "views": 5},
      {"tab": "destiny", "views": 3},
      {"tab": "summary", "views": 2}
    ],
    "engagement_score": 8.5
  }
}
```

---

## 🔍 Query & Search

### Search Numerology Meanings
<div class="api-endpoint">
<span class="method get">GET</span> <code>/api/v1/search</code>
</div>

Search for numerology meanings and interpretations.

**Query Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `q` | string | Yes | Search query |
| `type` | string | No | Filter by number type |
| `number` | integer | No | Specific number to search |

**Example Request:**
```
GET /api/v1/search?q=career&type=life_path&number=5
```

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "number": 5,
        "type": "life_path",
        "title": "Life Path 5 Career Guidance",
        "content": "Individuals with Life Path 5 thrive in careers that offer...",
        "relevance_score": 0.95,
        "tags": ["career", "freedom", "adventure"]
      }
    ],
    "total_results": 1,
    "search_time": "12ms"
  }
}
```

---

## 🔐 Authentication (Future)

### Login
<div class="api-endpoint">
<span class="method post">POST</span> <code>/api/v1/auth/login</code>
</div>

*Coming in v1.1*

Authenticate a user and receive access tokens.

### Register
<div class="api-endpoint">
<span class="method post">POST</span> <code>/api/v1/auth/register</code>
</div>

*Coming in v1.1*

Register a new user account.

### Refresh Token
<div class="api-endpoint">
<span class="method post">POST</span> <code>/api/v1/auth/refresh</code>
</div>

*Coming in v1.1*

Refresh an expired access token.

---

## 📈 Rate Limiting

Current implementation uses session-based tracking. Future rate limits:

| Endpoint | Rate Limit | Window |
|----------|------------|--------|
| `/api/v1/calculate` | 100 requests | 1 hour |
| `/api/v1/chat` | 50 requests | 1 minute |
| `/api/v1/track-event` | 500 requests | 1 hour |
| All endpoints | 1000 requests | 1 hour |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1701386400
```

---

## 🛠️ Testing Endpoints

You can test all endpoints using the interactive documentation at:
- **Development**: http://localhost:8000/docs
- **Production**: https://your-domain.com/docs

Or use curl commands provided in each endpoint's documentation.