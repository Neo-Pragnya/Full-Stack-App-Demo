# Data Models

This section describes all the data models used in the API requests and responses.

## 📊 Request Models

### CalculationRequest
Used for numerology calculation requests.

**Model Definition:**
```python
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class CalculationRequest(BaseModel):
    full_name: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="Full name as it appears on birth certificate"
    )
    birth_date: date = Field(
        ...,
        description="Birth date in YYYY-MM-DD format"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Michael Smith",
                "birth_date": "1990-01-15"
            }
        }
```

**Field Validation:**
- `full_name`: Must be 2-100 characters, only letters and spaces
- `birth_date`: Must be valid date, not in the future

**Example JSON:**
```json
{
  "full_name": "John Michael Smith",
  "birth_date": "1990-01-15"
}
```

### ChatRequest
Used for chat message requests.

**Model Definition:**
```python
class ChatRequest(BaseModel):
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="User's message to the chat assistant"
    )
    session_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique session identifier"
    )
    context: Optional[dict] = Field(
        None,
        description="Additional context for personalized responses"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What does my life path number mean?",
                "session_id": "user-session-12345",
                "context": {
                    "full_name": "John Smith",
                    "birth_date": "1990-01-15",
                    "previous_calculation": True
                }
            }
        }
```

### EventRequest
Used for tracking user events.

**Model Definition:**
```python
from enum import Enum

class EventType(str, Enum):
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    TAB_CLICK = "tab_click"
    CALCULATION_REQUEST = "calculation_request"
    CHAT_MESSAGE = "chat_message"
    SESSION_START = "session_start"
    SESSION_END = "session_end"

class EventRequest(BaseModel):
    event_type: EventType = Field(
        ...,
        description="Type of event being tracked"
    )
    session_id: str = Field(
        ...,
        description="Session identifier"
    )
    data: Optional[dict] = Field(
        None,
        description="Additional event data"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "thumbs_up",
                "session_id": "user-session-12345",
                "data": {
                    "message_id": "msg_67890",
                    "rating": "positive",
                    "feedback_text": "Very helpful explanation"
                }
            }
        }
```

---

## 📋 Response Models

### StandardResponse
Base response model for all API responses.

**Model Definition:**
```python
from typing import Any, Optional
from datetime import datetime

class StandardResponse(BaseModel):
    status: str = Field(
        ...,
        description="Response status: 'success' or 'error'"
    )
    data: Optional[Any] = Field(
        None,
        description="Response data (null on error)"
    )
    error: Optional[dict] = Field(
        None,
        description="Error details (null on success)"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": {...},
                "error": None,
                "timestamp": "2025-11-30T22:40:02.184375"
            }
        }
```

### HealthResponse
Health check response model.

**Model Definition:**
```python
class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Status message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(..., description="Application version")
    uptime: str = Field(..., description="Service uptime")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "Service is running",
                "timestamp": "2025-11-30T22:40:02.184375",
                "version": "1.0.0",
                "uptime": "2h 15m 30s"
            }
        }
```

---

## 🔢 Numerology Data Models

### LifePathNumber
Life Path calculation result.

**Model Definition:**
```python
class LifePathNumber(BaseModel):
    number: int = Field(..., description="Life Path number (1-9, 11, 22, 33)")
    calculation: str = Field(..., description="How the number was calculated")
    is_master: bool = Field(..., description="Whether this is a Master Number")
    interpretation: str = Field(..., description="Meaning and interpretation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "number": 5,
                "calculation": "1 + 5 + 1990 = 1996 → 5",
                "is_master": False,
                "interpretation": "You are adventurous and freedom-loving..."
            }
        }
```

### DestinyNumber
Destiny/Expression number result.

**Model Definition:**
```python
class DestinyNumber(BaseModel):
    number: int = Field(..., description="Destiny number")
    calculation: str = Field(..., description="Calculation method")
    is_master: bool = Field(..., description="Master number flag")
    letter_breakdown: dict = Field(..., description="Letter values used")
    interpretation: str = Field(..., description="Number meaning")
    
    class Config:
        json_schema_extra = {
            "example": {
                "number": 8,
                "calculation": "Sum of all letters = 89 → 8",
                "is_master": False,
                "letter_breakdown": {
                    "J": {"value": 1, "count": 1},
                    "O": {"value": 6, "count": 1}
                },
                "interpretation": "Your life purpose is material success..."
            }
        }
```

### SoulUrgeNumber
Soul Urge/Heart's Desire number result.

**Model Definition:**
```python
class SoulUrgeNumber(BaseModel):
    number: int = Field(..., description="Soul Urge number")
    calculation: str = Field(..., description="Vowel calculation")
    is_master: bool = Field(..., description="Master number flag")
    vowels_used: list[str] = Field(..., description="Vowels in the name")
    interpretation: str = Field(..., description="Inner desire meaning")
    
    class Config:
        json_schema_extra = {
            "example": {
                "number": 3,
                "calculation": "Vowels (O, I, A, E, I) = 21 → 3",
                "is_master": False,
                "vowels_used": ["O", "I", "A", "E", "I"],
                "interpretation": "You desire creative expression..."
            }
        }
```

### PersonalityNumber
Personality number result.

**Model Definition:**
```python
class PersonalityNumber(BaseModel):
    number: int = Field(..., description="Personality number")
    calculation: str = Field(..., description="Consonant calculation")
    is_master: bool = Field(..., description="Master number flag")
    consonants_used: list[str] = Field(..., description="Consonants in name")
    interpretation: str = Field(..., description="Outer personality meaning")
    
    class Config:
        json_schema_extra = {
            "example": {
                "number": 5,
                "calculation": "Consonants = 68 → 5",
                "is_master": False,
                "consonants_used": ["J", "H", "N", "M", "C", "H", "L"],
                "interpretation": "Others see you as dynamic..."
            }
        }
```

### PersonalYearNumber
Personal Year calculation.

**Model Definition:**
```python
class PersonalYearNumber(BaseModel):
    number: int = Field(..., description="Personal Year number")
    calculation: str = Field(..., description="Year calculation method")
    year: int = Field(..., description="Year this applies to")
    interpretation: str = Field(..., description="Year's influence")
    
    class Config:
        json_schema_extra = {
            "example": {
                "number": 8,
                "calculation": "1 + 5 + 2025 = 2031 → 8",
                "year": 2025,
                "interpretation": "Focus on business and achievement..."
            }
        }
```

### ChallengeNumbers
Life challenges calculation.

**Model Definition:**
```python
class ChallengeNumbers(BaseModel):
    first: int = Field(..., description="First challenge number")
    second: int = Field(..., description="Second challenge number")
    third: int = Field(..., description="Third challenge number")
    fourth: int = Field(..., description="Fourth challenge number")
    calculation: str = Field(..., description="How challenges were calculated")
    
    class Config:
        json_schema_extra = {
            "example": {
                "first": 4,
                "second": 4,
                "third": 0,
                "fourth": 0,
                "calculation": "Based on day(15), month(1), year(1990)"
            }
        }
```

### PinnacleNumbers
Life pinnacles calculation.

**Model Definition:**
```python
class PinnacleNumbers(BaseModel):
    first: int = Field(..., description="First pinnacle number")
    second: int = Field(..., description="Second pinnacle number")
    third: int = Field(..., description="Third pinnacle number")
    fourth: int = Field(..., description="Fourth pinnacle number")
    calculation: str = Field(..., description="Pinnacle calculation method")
    
    class Config:
        json_schema_extra = {
            "example": {
                "first": 6,
                "second": 1,
                "third": 7,
                "fourth": 2,
                "calculation": "Life periods based on birth date"
            }
        }
```

### KarmicLessons
Karmic lessons from name analysis.

**Model Definition:**
```python
class KarmicLessons(BaseModel):
    missing_numbers: list[int] = Field(..., description="Numbers not in name")
    present_numbers: list[int] = Field(..., description="Numbers present in name")
    calculation: str = Field(..., description="Analysis method")
    
    class Config:
        json_schema_extra = {
            "example": {
                "missing_numbers": [2, 7, 9],
                "present_numbers": [1, 3, 4, 5, 6, 8],
                "calculation": "Missing numbers from name analysis"
            }
        }
```

### HiddenPassion
Hidden passion number result.

**Model Definition:**
```python
class HiddenPassion(BaseModel):
    number: list[int] = Field(..., description="Most frequent number(s)")
    calculation: str = Field(..., description="Frequency analysis method")
    frequency_map: dict = Field(..., description="Number frequency breakdown")
    
    class Config:
        json_schema_extra = {
            "example": {
                "number": [1, 8],
                "calculation": "Most frequent letters in name",
                "frequency_map": {"1": 3, "8": 3, "5": 2}
            }
        }
```

### CalculationResult
Complete numerology calculation result.

**Model Definition:**
```python
class CalculationResult(BaseModel):
    life_path: LifePathNumber
    destiny: DestinyNumber
    soul_urge: SoulUrgeNumber
    personality: PersonalityNumber
    birth_day: BirthDayNumber
    personal_year: PersonalYearNumber
    challenge_numbers: ChallengeNumbers
    pinnacle_numbers: PinnacleNumbers
    karmic_lessons: KarmicLessons
    master_numbers: list[int] = Field(..., description="Master numbers present")
    lucky_numbers: list[int] = Field(..., description="Derived lucky numbers")
    hidden_passion: HiddenPassion
    
    class Config:
        json_schema_extra = {
            "example": {
                "life_path": {...},
                "destiny": {...},
                "soul_urge": {...},
                "personality": {...},
                "birth_day": {...},
                "personal_year": {...},
                "challenge_numbers": {...},
                "pinnacle_numbers": {...},
                "karmic_lessons": {...},
                "master_numbers": [11, 22],
                "lucky_numbers": [1, 5, 8, 15, 24],
                "hidden_passion": {...}
            }
        }
```

---

## 💬 Chat Models

### ChatMessage
Individual chat message model.

**Model Definition:**
```python
class ChatMessage(BaseModel):
    id: str = Field(..., description="Unique message ID")
    type: str = Field(..., description="Message type: user or assistant")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Message timestamp")
    rating: Optional[str] = Field(None, description="User rating if available")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "msg_123",
                "type": "user",
                "content": "Hello",
                "timestamp": "2025-11-30T22:30:00Z",
                "rating": None
            }
        }
```

### ChatResponse
Chat assistant response model.

**Model Definition:**
```python
class ChatResponse(BaseModel):
    message: str = Field(..., description="Assistant's response message")
    type: str = Field(..., description="Response type")
    message_id: str = Field(..., description="Unique message identifier")
    suggestions: list[str] = Field(..., description="Suggested follow-up questions")
    context_used: bool = Field(..., description="Whether context was utilized")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Your Life Path number 5 indicates...",
                "type": "numerology_explanation",
                "message_id": "msg_67890",
                "suggestions": [
                    "Tell me about my destiny number",
                    "How do my numbers work together?"
                ],
                "context_used": True
            }
        }
```

---

## 📊 Analytics Models

### EventData
Event tracking data model.

**Model Definition:**
```python
class EventData(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")
    recorded: bool = Field(..., description="Whether event was recorded")
    
    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "evt_456789",
                "recorded": True
            }
        }
```

### SessionAnalytics
Session analytics data model.

**Model Definition:**
```python
class FeedbackStats(BaseModel):
    positive: int = Field(..., description="Positive feedback count")
    negative: int = Field(..., description="Negative feedback count")
    total: int = Field(..., description="Total feedback received")
    satisfaction_rate: float = Field(..., description="Satisfaction percentage")

class TabView(BaseModel):
    tab: str = Field(..., description="Tab name")
    views: int = Field(..., description="Number of views")

class SessionAnalytics(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    session_duration: int = Field(..., description="Duration in seconds")
    total_interactions: int = Field(..., description="Total user interactions")
    calculations_performed: int = Field(..., description="Calculations done")
    messages_sent: int = Field(..., description="Messages sent")
    feedback_stats: FeedbackStats = Field(..., description="Feedback statistics")
    most_viewed_tabs: list[TabView] = Field(..., description="Tab view statistics")
    engagement_score: float = Field(..., description="Overall engagement score")
    
    class Config:
        json_schema_extra = {
            "example": {
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
                    {"tab": "destiny", "views": 3}
                ],
                "engagement_score": 8.5
            }
        }
```

---

## ❌ Error Models

### ValidationError
Input validation error details.

**Model Definition:**
```python
class ValidationError(BaseModel):
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: dict = Field(..., description="Error details")
    
    class Config:
        json_schema_extra = {
            "example": {
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

### ErrorResponse
Standard error response format.

**Model Definition:**
```python
class ErrorResponse(BaseModel):
    status: str = Field("error", description="Always 'error'")
    error: ValidationError = Field(..., description="Error details")
    data: None = Field(None, description="Always null for errors")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid input data",
                    "details": {...}
                },
                "data": None,
                "timestamp": "2025-11-30T22:40:02.184375"
            }
        }
```

---

## 🔧 Model Utilities

### Field Validation
Common validation patterns used across models:

```python
# Name validation
name_field = Field(
    ..., 
    min_length=2, 
    max_length=100,
    regex=r"^[a-zA-Z\s]+$",
    description="Full name with letters and spaces only"
)

# Date validation
date_field = Field(
    ...,
    description="Date in YYYY-MM-DD format",
    example="1990-01-15"
)

# Session ID validation
session_field = Field(
    ...,
    min_length=1,
    max_length=100,
    regex=r"^[a-zA-Z0-9\-_]+$",
    description="Alphanumeric session identifier"
)
```

### Example Generators
```python
def generate_calculation_example():
    """Generate example calculation request"""
    return {
        "full_name": "John Michael Smith",
        "birth_date": "1990-01-15"
    }

def generate_chat_example():
    """Generate example chat request"""
    return {
        "message": "What does my life path number mean?",
        "session_id": "user-session-12345",
        "context": {
            "full_name": "John Smith",
            "previous_calculation": True
        }
    }
```

All models include comprehensive validation, examples, and documentation to ensure proper API usage and clear error messages.