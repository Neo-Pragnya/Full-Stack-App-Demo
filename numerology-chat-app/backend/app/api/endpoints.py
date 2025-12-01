"""
FastAPI endpoints for the Numerology Chat Application.
Handles numerology calculations, chat interactions, and event tracking.
"""

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import time
from datetime import datetime

from app.models.schemas import (
    UserInput, ChatMessage, UserEvent, NumerologyResponse, 
    FeedbackRequest, TabClickEvent, APIResponse
)
from app.services.numerology_calculator import NumerologyCalculator
from app.services.chat_service import chat_service
from app.services.event_tracker import event_tracker, EventType


# Create router
router = APIRouter()

# Initialize calculator
calculator = NumerologyCalculator()


def get_client_ip(request: Request) -> str:
    """Extract client IP address from request."""
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.client.host


def get_session_id(request: Request) -> Optional[str]:
    """Extract session ID from request headers."""
    return request.headers.get('X-Session-ID')


@router.post("/calculate", response_model=NumerologyResponse)
async def calculate_numerology(
    user_input: UserInput,
    request: Request
) -> NumerologyResponse:
    """Calculate numerology numbers for given name and birth date."""
    
    session_id = get_session_id(request)
    user_ip = get_client_ip(request)
    start_time = time.time()
    
    try:
        # Validate input
        if not user_input.full_name or not user_input.birth_date:
            raise HTTPException(status_code=400, detail="Name and birth date are required")
        
        # Calculate numerology
        results = calculator.calculate_all_numbers(
            user_input.full_name, 
            user_input.birth_date
        )
        
        calculation_time = time.time() - start_time
        
        if 'error' in results:
            # Track failed calculation
            if session_id:
                event_tracker.track_numerology_calculation(
                    user_input.full_name,
                    user_input.birth_date,
                    False,
                    calculation_time,
                    session_id=session_id,
                    user_ip=user_ip
                )
            
            return NumerologyResponse(
                success=False,
                error=results['error']
            )
        
        # Track successful calculation
        if session_id:
            event_tracker.track_numerology_calculation(
                user_input.full_name,
                user_input.birth_date,
                True,
                calculation_time,
                session_id=session_id,
                user_ip=user_ip
            )
        
        return NumerologyResponse(
            success=True,
            data=results
        )
        
    except Exception as e:
        calculation_time = time.time() - start_time
        
        # Track failed calculation
        if session_id:
            event_tracker.track_numerology_calculation(
                user_input.full_name,
                user_input.birth_date,
                False,
                calculation_time,
                session_id=session_id,
                user_ip=user_ip
            )
        
        raise HTTPException(
            status_code=500, 
            detail=f"Error calculating numerology: {str(e)}"
        )


@router.post("/chat", response_model=APIResponse)
async def chat_message(
    chat_msg: ChatMessage,
    request: Request
) -> APIResponse:
    """Process a chat message and return bot response."""
    
    session_id = get_session_id(request)
    user_ip = get_client_ip(request)
    
    try:
        # Process message through chat service
        response = chat_service.process_message(
            chat_msg.message,
            session_id=session_id,
            user_ip=user_ip
        )
        
        return APIResponse(
            status="success",
            message="Message processed successfully",
            data=response
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )


@router.post("/events/session", response_model=APIResponse)
async def create_session(request: Request) -> APIResponse:
    """Create a new user session."""
    
    user_agent = request.headers.get('User-Agent')
    user_ip = get_client_ip(request)
    
    try:
        session_id = event_tracker.create_session(
            user_agent=user_agent,
            ip_address=user_ip
        )
        
        return APIResponse(
            status="success",
            message="Session created successfully",
            data={"session_id": session_id}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating session: {str(e)}"
        )


@router.post("/events/feedback", response_model=APIResponse)
async def submit_feedback(
    feedback: FeedbackRequest,
    request: Request
) -> APIResponse:
    """Submit user feedback (thumbs up/down)."""
    
    session_id = get_session_id(request)
    user_ip = get_client_ip(request)
    
    try:
        event_id = event_tracker.track_feedback(
            feedback.feedback_type,
            feedback.target_type,
            feedback.target_id,
            feedback.additional_data,
            session_id=session_id,
            user_ip=user_ip
        )
        
        return APIResponse(
            status="success",
            message="Feedback submitted successfully",
            data={"event_id": event_id}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error submitting feedback: {str(e)}"
        )


@router.post("/events/tab-click", response_model=APIResponse)
async def track_tab_click(
    tab_event: TabClickEvent,
    request: Request
) -> APIResponse:
    """Track tab click events."""
    
    session_id = get_session_id(request)
    user_ip = get_client_ip(request)
    
    try:
        event_id = event_tracker.track_tab_click(
            tab_event.tab_name,
            tab_event.tab_category,
            tab_event.previous_tab,
            session_id=session_id,
            user_ip=user_ip
        )
        
        return APIResponse(
            status="success",
            message="Tab click tracked successfully",
            data={"event_id": event_id}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error tracking tab click: {str(e)}"
        )


@router.post("/events/custom", response_model=APIResponse)
async def track_custom_event(
    event: UserEvent,
    request: Request
) -> APIResponse:
    """Track a custom user event."""
    
    session_id = get_session_id(request)
    user_ip = get_client_ip(request)
    
    try:
        event_id = event_tracker.track_event(
            event.event_type,
            event.event_data,
            session_id=session_id or event.session_id,
            user_ip=user_ip or event.user_ip
        )
        
        return APIResponse(
            status="success",
            message="Custom event tracked successfully",
            data={"event_id": event_id}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error tracking custom event: {str(e)}"
        )


@router.get("/events/session/{session_id}", response_model=APIResponse)
async def get_session_events(session_id: str) -> APIResponse:
    """Get all events for a specific session."""
    
    try:
        events = event_tracker.get_events(session_id=session_id)
        
        return APIResponse(
            status="success",
            message="Session events retrieved successfully",
            data={
                "session_id": session_id,
                "events": events,
                "event_count": len(events)
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving session events: {str(e)}"
        )


@router.get("/analytics/session/{session_id}", response_model=APIResponse)
async def get_session_analytics(session_id: str) -> APIResponse:
    """Get analytics for a specific session."""
    
    try:
        analytics = event_tracker.get_session_analytics(session_id)
        
        return APIResponse(
            status="success",
            message="Session analytics retrieved successfully",
            data=analytics
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving session analytics: {str(e)}"
        )


@router.get("/analytics/global", response_model=APIResponse)
async def get_global_analytics() -> APIResponse:
    """Get global analytics across all sessions."""
    
    try:
        analytics = event_tracker.get_global_analytics()
        
        return APIResponse(
            status="success",
            message="Global analytics retrieved successfully",
            data=analytics
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving global analytics: {str(e)}"
        )


@router.get("/conversation/{session_id}", response_model=APIResponse)
async def get_conversation_history(session_id: str) -> APIResponse:
    """Get conversation history for a session."""
    
    try:
        history = chat_service.get_conversation_history(session_id)
        
        return APIResponse(
            status="success",
            message="Conversation history retrieved successfully",
            data={
                "session_id": session_id,
                "conversation_history": history
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversation history: {str(e)}"
        )


@router.delete("/session/{session_id}", response_model=APIResponse)
async def end_session(session_id: str) -> APIResponse:
    """End a user session and cleanup data."""
    
    try:
        # End the session in event tracker
        event_tracker.end_session(session_id)
        
        # Clear chat service session
        chat_service.clear_session(session_id)
        
        return APIResponse(
            status="success",
            message="Session ended successfully",
            data={"session_id": session_id}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error ending session: {str(e)}"
        )


@router.get("/health", response_model=APIResponse)
async def health_check() -> APIResponse:
    """Health check endpoint."""
    
    return APIResponse(
        status="healthy",
        message="Numerology Chat API is running",
        data={
            "version": "1.0.0",
            "timestamp": datetime.now(),
            "services": {
                "numerology_calculator": "operational",
                "chat_service": "operational",
                "event_tracker": "operational"
            }
        }
    )