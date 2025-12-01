from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class EventType(str, Enum):
    """Types of events that can be tracked."""
    CHAT_MESSAGE = "chat_message"
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    TAB_CLICK = "tab_click"
    NUMEROLOGY_CALCULATION = "numerology_calculation"
    SESSION_START = "session_start"
    SESSION_END = "session_end"


class UserInput(BaseModel):
    """Model for user input containing name and birth date."""
    full_name: str = Field(..., min_length=1, max_length=200, description="User's full name")
    birth_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Birth date in YYYY-MM-DD format")


class ChatMessage(BaseModel):
    """Model for chat messages."""
    message: str = Field(..., min_length=1, max_length=1000, description="Chat message content")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Message timestamp")
    sender: str = Field(default="user", description="Message sender (user or bot)")
    message_type: str = Field(default="text", description="Type of message")


class UserEvent(BaseModel):
    """Model for tracking user events."""
    event_type: EventType = Field(..., description="Type of event")
    event_data: Dict[str, Any] = Field(default_factory=dict, description="Additional event data")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Event timestamp")
    session_id: Optional[str] = Field(None, description="Session identifier")
    user_ip: Optional[str] = Field(None, description="User IP address")


class NumerologyResponse(BaseModel):
    """Model for numerology calculation response."""
    success: bool = Field(..., description="Whether the calculation was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Numerology calculation results")
    error: Optional[str] = Field(None, description="Error message if calculation failed")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Response timestamp")


class FeedbackRequest(BaseModel):
    """Model for user feedback (thumbs up/down)."""
    feedback_type: str = Field(..., pattern="^(up|down)$", description="Type of feedback: 'up' or 'down'")
    target_type: str = Field(..., description="What the feedback is for (e.g., 'calculation', 'interpretation')")
    target_id: Optional[str] = Field(None, description="ID of the target item")
    additional_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional feedback data")


class TabClickEvent(BaseModel):
    """Model for tab click events."""
    tab_name: str = Field(..., description="Name of the clicked tab")
    tab_category: str = Field(..., description="Category of the tab (e.g., 'core_numbers', 'advanced_numbers')")
    previous_tab: Optional[str] = Field(None, description="Previously active tab")


class SessionInfo(BaseModel):
    """Model for session information."""
    session_id: str = Field(..., description="Unique session identifier")
    start_time: datetime = Field(default_factory=datetime.now, description="Session start time")
    user_agent: Optional[str] = Field(None, description="User agent string")
    ip_address: Optional[str] = Field(None, description="User IP address")


class APIResponse(BaseModel):
    """Generic API response model."""
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class HealthCheck(BaseModel):
    """Health check response model."""
    status: str = Field(default="healthy", description="Service health status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")
    version: str = Field(default="1.0.0", description="API version")
    uptime: Optional[float] = Field(None, description="Service uptime in seconds")


class NumberInterpretation(BaseModel):
    """Model for individual number interpretation."""
    number: int = Field(..., description="The numerology number")
    interpretation: str = Field(..., description="Interpretation of the number")
    is_master: bool = Field(default=False, description="Whether this is a master number")
    calculation: Optional[str] = Field(None, description="How the number was calculated")


class NumerologyCategories(BaseModel):
    """Model for organizing numerology results by categories."""
    core_numbers: Dict[str, NumberInterpretation] = Field(..., description="Core numerology numbers")
    advanced_numbers: Dict[str, NumberInterpretation] = Field(..., description="Advanced numerology numbers") 
    life_cycles: Dict[str, Any] = Field(..., description="Life cycle information")
    karmic_spiritual: Dict[str, Any] = Field(..., description="Karmic and spiritual aspects")
    timing_analysis: Dict[str, Any] = Field(..., description="Timing and current cycles")
    general_info: Dict[str, Any] = Field(..., description="General information and lucky numbers")