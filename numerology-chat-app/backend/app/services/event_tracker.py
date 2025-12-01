"""
Event tracking service for capturing user interactions.
Stores events in memory and can be extended to use a database.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models.schemas import UserEvent, EventType
import uuid
import json


class EventTracker:
    """Service for tracking and storing user events."""
    
    def __init__(self):
        # In-memory storage for events (in production, use a database)
        self.events: List[Dict[str, Any]] = []
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, user_agent: Optional[str] = None, ip_address: Optional[str] = None) -> str:
        """Create a new user session."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'session_id': session_id,
            'start_time': datetime.now(),
            'user_agent': user_agent,
            'ip_address': ip_address,
            'events_count': 0,
            'last_activity': datetime.now()
        }
        
        # Track session start event
        self.track_event(
            EventType.SESSION_START,
            {'session_id': session_id, 'user_agent': user_agent, 'ip_address': ip_address},
            session_id=session_id,
            user_ip=ip_address
        )
        
        return session_id
    
    def track_event(
        self,
        event_type: EventType,
        event_data: Dict[str, Any] = None,
        session_id: Optional[str] = None,
        user_ip: Optional[str] = None
    ) -> str:
        """Track a user event."""
        if event_data is None:
            event_data = {}
        
        event_id = str(uuid.uuid4())
        event = {
            'event_id': event_id,
            'event_type': event_type.value,
            'event_data': event_data,
            'timestamp': datetime.now(),
            'session_id': session_id,
            'user_ip': user_ip
        }
        
        self.events.append(event)
        
        # Update session info
        if session_id and session_id in self.sessions:
            self.sessions[session_id]['events_count'] += 1
            self.sessions[session_id]['last_activity'] = datetime.now()
        
        return event_id
    
    def track_chat_message(
        self,
        message: str,
        sender: str = "user",
        message_type: str = "text",
        session_id: Optional[str] = None,
        user_ip: Optional[str] = None
    ) -> str:
        """Track a chat message event."""
        return self.track_event(
            EventType.CHAT_MESSAGE,
            {
                'message': message,
                'sender': sender,
                'message_type': message_type,
                'message_length': len(message)
            },
            session_id=session_id,
            user_ip=user_ip
        )
    
    def track_feedback(
        self,
        feedback_type: str,
        target_type: str,
        target_id: Optional[str] = None,
        additional_data: Dict[str, Any] = None,
        session_id: Optional[str] = None,
        user_ip: Optional[str] = None
    ) -> str:
        """Track a feedback event (thumbs up/down)."""
        event_type = EventType.THUMBS_UP if feedback_type == "up" else EventType.THUMBS_DOWN
        
        event_data = {
            'feedback_type': feedback_type,
            'target_type': target_type,
            'target_id': target_id
        }
        
        if additional_data:
            event_data.update(additional_data)
        
        return self.track_event(
            event_type,
            event_data,
            session_id=session_id,
            user_ip=user_ip
        )
    
    def track_tab_click(
        self,
        tab_name: str,
        tab_category: str,
        previous_tab: Optional[str] = None,
        session_id: Optional[str] = None,
        user_ip: Optional[str] = None
    ) -> str:
        """Track a tab click event."""
        return self.track_event(
            EventType.TAB_CLICK,
            {
                'tab_name': tab_name,
                'tab_category': tab_category,
                'previous_tab': previous_tab
            },
            session_id=session_id,
            user_ip=user_ip
        )
    
    def track_numerology_calculation(
        self,
        full_name: str,
        birth_date: str,
        calculation_success: bool,
        calculation_time: float,
        session_id: Optional[str] = None,
        user_ip: Optional[str] = None
    ) -> str:
        """Track a numerology calculation event."""
        return self.track_event(
            EventType.NUMEROLOGY_CALCULATION,
            {
                'full_name_length': len(full_name),
                'birth_date': birth_date,
                'calculation_success': calculation_success,
                'calculation_time_ms': calculation_time * 1000,
                'word_count': len(full_name.split())
            },
            session_id=session_id,
            user_ip=user_ip
        )
    
    def end_session(self, session_id: str) -> None:
        """End a user session."""
        if session_id in self.sessions:
            self.sessions[session_id]['end_time'] = datetime.now()
            duration = (self.sessions[session_id]['end_time'] - 
                       self.sessions[session_id]['start_time']).total_seconds()
            
            self.track_event(
                EventType.SESSION_END,
                {
                    'session_id': session_id,
                    'session_duration_seconds': duration,
                    'total_events': self.sessions[session_id]['events_count']
                },
                session_id=session_id
            )
    
    def get_events(
        self,
        session_id: Optional[str] = None,
        event_type: Optional[EventType] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get events with optional filtering."""
        filtered_events = self.events
        
        if session_id:
            filtered_events = [e for e in filtered_events if e.get('session_id') == session_id]
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.get('event_type') == event_type.value]
        
        # Return latest events first
        filtered_events.sort(key=lambda x: x['timestamp'], reverse=True)
        return filtered_events[:limit]
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific session."""
        return self.sessions.get(session_id)
    
    def get_session_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get analytics for a specific session."""
        session_events = self.get_events(session_id=session_id)
        
        event_counts = {}
        for event in session_events:
            event_type = event['event_type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        session_info = self.get_session_info(session_id)
        
        analytics = {
            'session_id': session_id,
            'total_events': len(session_events),
            'event_counts_by_type': event_counts,
            'session_info': session_info
        }
        
        if session_info:
            if 'end_time' in session_info:
                duration = (session_info['end_time'] - session_info['start_time']).total_seconds()
                analytics['session_duration_seconds'] = duration
            else:
                duration = (datetime.now() - session_info['start_time']).total_seconds()
                analytics['current_session_duration_seconds'] = duration
        
        return analytics
    
    def get_global_analytics(self) -> Dict[str, Any]:
        """Get global analytics across all sessions."""
        total_events = len(self.events)
        total_sessions = len(self.sessions)
        
        event_counts = {}
        for event in self.events:
            event_type = event['event_type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Calculate average session duration for completed sessions
        completed_sessions = [s for s in self.sessions.values() if 'end_time' in s]
        avg_session_duration = 0
        if completed_sessions:
            total_duration = sum(
                (s['end_time'] - s['start_time']).total_seconds() 
                for s in completed_sessions
            )
            avg_session_duration = total_duration / len(completed_sessions)
        
        return {
            'total_events': total_events,
            'total_sessions': total_sessions,
            'completed_sessions': len(completed_sessions),
            'active_sessions': total_sessions - len(completed_sessions),
            'event_counts_by_type': event_counts,
            'average_session_duration_seconds': avg_session_duration
        }
    
    def export_events_json(self, session_id: Optional[str] = None) -> str:
        """Export events as JSON string."""
        events_to_export = self.get_events(session_id=session_id, limit=None)
        
        # Convert datetime objects to ISO format for JSON serialization
        for event in events_to_export:
            if 'timestamp' in event and isinstance(event['timestamp'], datetime):
                event['timestamp'] = event['timestamp'].isoformat()
        
        return json.dumps(events_to_export, indent=2, default=str)


# Global instance of the event tracker
event_tracker = EventTracker()