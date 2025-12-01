# API Documentation

## Numerology Chat Application API

Base URL: `http://localhost:8000`

### Authentication
Currently using session-based tracking. No authentication required.

---

## Endpoints

### Health Check

**GET** `/health`

Check application health status.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

### Calculate Numerology

**POST** `/calculate`

Calculate comprehensive numerology analysis for a person.

**Request Body:**
```json
{
  "name": "John Doe",
  "birth_date": "1990-01-01"
}
```

**Response:**
```json
{
  "life_path": {
    "number": 5,
    "interpretation": "You are adventurous and freedom-loving..."
  },
  "expression": {
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
  "master_numbers": ["11"],
  "summary": "Your numerology profile shows..."
}
```

---

### Chat Interface

**POST** `/chat`

Send a message and receive numerology-focused response.

**Request Body:**
```json
{
  "message": "Tell me about my life path number",
  "session_id": "unique-session-id",
  "context": {
    "name": "John Doe", 
    "birth_date": "1990-01-01"
  }
}
```

**Response:**
```json
{
  "response": "Based on your birth date...",
  "message_id": "msg-123",
  "timestamp": "2024-01-01T00:00:00Z",
  "context_used": true
}
```

---

### Event Tracking

**POST** `/track-event`

Track user interactions and feedback.

**Request Body:**
```json
{
  "event_type": "thumbs_up",
  "session_id": "unique-session-id",
  "data": {
    "message_id": "msg-123",
    "rating": "positive"
  }
}
```

**Response:**
```json
{
  "success": true,
  "event_id": "event-456"
}
```

---

### Get Analytics

**GET** `/analytics/{session_id}`

Retrieve analytics for a session.

**Response:**
```json
{
  "session_id": "unique-session-id",
  "total_interactions": 15,
  "positive_feedback": 12,
  "negative_feedback": 1,
  "calculations_performed": 3,
  "session_duration": 1800
}
```

---

### Get Session History

**GET** `/sessions/{session_id}/history`

Retrieve chat history for a session.

**Response:**
```json
{
  "messages": [
    {
      "id": "msg-1",
      "type": "user",
      "content": "Hello",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    {
      "id": "msg-2", 
      "type": "assistant",
      "content": "Hi! I'm here to help with numerology...",
      "timestamp": "2024-01-01T00:00:01Z",
      "rating": "positive"
    }
  ]
}
```

---

## Data Models

### PersonInput
```typescript
{
  name: string;        // Full name
  birth_date: string;  // Format: YYYY-MM-DD
}
```

### NumerologyResult
```typescript
{
  life_path: {
    number: number;
    interpretation: string;
  };
  expression: {
    number: number;
    interpretation: string;
  };
  soul_urge: {
    number: number;
    interpretation: string;
  };
  personality: {
    number: number;
    interpretation: string;
  };
  master_numbers: number[];
  summary: string;
}
```

### ChatMessage
```typescript
{
  message: string;
  session_id: string;
  context?: {
    name?: string;
    birth_date?: string;
  };
}
```

### Event
```typescript
{
  event_type: string;  // "thumbs_up", "thumbs_down", "calculation", "message"
  session_id: string;
  data: object;        // Event-specific data
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input: birth_date must be in YYYY-MM-DD format"
}
```

### 404 Not Found
```json
{
  "detail": "Session not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider:
- 100 requests per minute per IP
- 1000 calculations per hour per session
- Websocket connections limited to 10 per IP

---

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:4200` (Angular development)
- `http://localhost:80` (Production frontend)
- Custom origins can be added via environment variables

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger/OpenAPI documentation where you can test endpoints directly.