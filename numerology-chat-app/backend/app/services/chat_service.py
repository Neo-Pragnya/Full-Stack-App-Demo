"""
Chat service for handling chat interactions and generating responses.
Provides conversational interface for numerology calculations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import re
from app.services.numerology_calculator import NumerologyCalculator
from app.services.event_tracker import event_tracker, EventType


class ChatService:
    """Service for handling chat interactions and generating responses."""
    
    def __init__(self):
        self.calculator = NumerologyCalculator()
        self.user_sessions = {}  # Store user conversation state
    
    def process_message(
        self, 
        message: str, 
        session_id: Optional[str] = None,
        user_ip: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a user message and generate appropriate response."""
        
        # Track the chat message
        if session_id:
            event_tracker.track_chat_message(
                message, 
                sender="user", 
                session_id=session_id,
                user_ip=user_ip
            )
        
        # Initialize session state if needed
        if session_id not in self.user_sessions:
            self.user_sessions[session_id] = {
                'state': 'greeting',
                'collected_data': {},
                'conversation_history': []
            }
        
        session_state = self.user_sessions[session_id]
        session_state['conversation_history'].append({
            'sender': 'user',
            'message': message,
            'timestamp': datetime.now()
        })
        
        # Generate response based on message content and session state
        response = self._generate_response(message, session_state)
        
        # Add bot response to history
        session_state['conversation_history'].append({
            'sender': 'bot',
            'message': response['message'],
            'timestamp': datetime.now()
        })
        
        # Track bot response
        if session_id:
            event_tracker.track_chat_message(
                response['message'],
                sender="bot",
                message_type=response.get('type', 'text'),
                session_id=session_id,
                user_ip=user_ip
            )
        
        return response
    
    def _generate_response(self, message: str, session_state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a response based on the user message and session state."""
        
        message_lower = message.lower().strip()
        current_state = session_state['state']
        collected_data = session_state['collected_data']
        
        # Handle greeting and initial interaction
        if current_state == 'greeting' or any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
            session_state['state'] = 'asking_name'
            return {
                'message': "👋 Hello! Welcome to the Numerology Chat Assistant! I'm here to help you discover your numerology profile through our conversation.\n\nTo get started, could you please tell me your full name (as it appears on your birth certificate)?",
                'type': 'greeting',
                'suggestions': ['My name is John Smith', 'John Michael Smith']
            }
        
        # Handle name collection
        elif current_state == 'asking_name':
            name = self._extract_name(message)
            if name:
                collected_data['name'] = name
                session_state['state'] = 'asking_birthdate'
                return {
                    'message': f"Nice to meet you, {name.split()[0]}! 😊\n\nNow I need your birth date to calculate your numerology numbers. Please provide it in the format YYYY-MM-DD (for example: 1990-05-15).",
                    'type': 'name_confirmed',
                    'suggestions': ['1990-05-15', '1985-12-25', '1995-07-03']
                }
            else:
                return {
                    'message': "I didn't quite catch your name. Could you please tell me your full name? For example, 'My name is John Smith' or just 'John Smith'.",
                    'type': 'name_clarification',
                    'suggestions': ['My name is John Smith', 'John Michael Smith']
                }
        
        # Handle birth date collection
        elif current_state == 'asking_birthdate':
            birth_date = self._extract_birth_date(message)
            if birth_date:
                collected_data['birth_date'] = birth_date
                session_state['state'] = 'ready_to_calculate'
                return {
                    'message': f"Perfect! I have your information:\n• Name: {collected_data['name']}\n• Birth Date: {birth_date}\n\n🔮 Would you like me to calculate your complete numerology profile now?",
                    'type': 'ready_to_calculate',
                    'suggestions': ['Yes, calculate my numerology!', 'Calculate my numbers', 'Let\'s do it!']
                }
            else:
                return {
                    'message': "I need your birth date in the format YYYY-MM-DD. For example: 1990-05-15 (May 15, 1990). Could you please provide your birth date?",
                    'type': 'birthdate_clarification',
                    'suggestions': ['1990-05-15', '1985-12-25', '1995-07-03']
                }
        
        # Handle calculation request
        elif current_state == 'ready_to_calculate':
            if any(word in message_lower for word in ['yes', 'calculate', 'do it', 'go', 'sure', 'ok']):
                # Perform the calculation
                try:
                    start_time = datetime.now()
                    results = self.calculator.calculate_all_numbers(
                        collected_data['name'], 
                        collected_data['birth_date']
                    )
                    calculation_time = (datetime.now() - start_time).total_seconds()
                    
                    if 'error' in results:
                        return {
                            'message': f"I encountered an error while calculating your numerology: {results['error']}\n\nWould you like to try again with different information?",
                            'type': 'calculation_error',
                            'suggestions': ['Try again', 'Start over']
                        }
                    
                    # Store results in session
                    collected_data['numerology_results'] = results
                    session_state['state'] = 'results_ready'
                    
                    # Track successful calculation
                    event_tracker.track_numerology_calculation(
                        collected_data['name'],
                        collected_data['birth_date'],
                        True,
                        calculation_time,
                        session_id=session_state.get('session_id')
                    )
                    
                    # Generate summary response
                    summary = self._create_results_summary(results)
                    
                    return {
                        'message': f"🌟 Your Numerology Profile is Ready! 🌟\n\n{summary}\n\n💡 You can now explore different tabs to see detailed information about each aspect of your numerology profile. Feel free to ask me about any specific numbers or their meanings!",
                        'type': 'calculation_complete',
                        'data': results,
                        'suggestions': [
                            'Tell me about my Life Path number',
                            'What does my Destiny number mean?',
                            'Explain my Soul Urge number',
                            'What are my lucky numbers?'
                        ]
                    }
                    
                except Exception as e:
                    return {
                        'message': f"I'm sorry, there was an error calculating your numerology: {str(e)}\n\nWould you like to try again?",
                        'type': 'calculation_error',
                        'suggestions': ['Try again', 'Start over']
                    }
            else:
                return {
                    'message': "No problem! When you're ready, just let me know and I'll calculate your numerology profile.",
                    'type': 'waiting_confirmation',
                    'suggestions': ['Calculate my numerology!', 'I\'m ready now']
                }
        
        # Handle questions about results
        elif current_state == 'results_ready':
            return self._handle_results_questions(message, collected_data)
        
        # Handle general conversation
        else:
            return self._handle_general_conversation(message)
    
    def _extract_name(self, message: str) -> Optional[str]:
        """Extract name from user message."""
        message = message.strip()
        
        # Remove common prefixes
        prefixes = ['my name is', 'i am', 'i\'m', 'call me', 'name is']
        message_lower = message.lower()
        
        for prefix in prefixes:
            if message_lower.startswith(prefix):
                name = message[len(prefix):].strip()
                # Remove quotes if present
                name = name.strip('\'"')
                if len(name) > 1:
                    return name
        
        # If no prefix found, assume the entire message is a name if it looks like one
        if re.match(r'^[A-Za-z\s\-\'\.]+$', message) and len(message.split()) >= 1:
            return message
        
        return None
    
    def _extract_birth_date(self, message: str) -> Optional[str]:
        """Extract birth date from user message."""
        # Look for YYYY-MM-DD pattern
        pattern = r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b'
        match = re.search(pattern, message)
        
        if match:
            year, month, day = match.groups()
            # Validate the date format
            try:
                formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                # Basic validation
                datetime.strptime(formatted_date, '%Y-%m-%d')
                return formatted_date
            except ValueError:
                pass
        
        return None
    
    def _create_results_summary(self, results: Dict[str, Any]) -> str:
        """Create a summary of the calculation results."""
        summary_parts = []
        
        # Core numbers
        if 'life_path' in results:
            summary_parts.append(f"🛤️ Life Path Number: {results['life_path']['number']}")
        
        if 'destiny' in results:
            summary_parts.append(f"⭐ Destiny Number: {results['destiny']['number']}")
        
        if 'soul_urge' in results:
            summary_parts.append(f"💫 Soul Urge Number: {results['soul_urge']['number']}")
        
        if 'personality' in results:
            summary_parts.append(f"🎭 Personality Number: {results['personality']['number']}")
        
        # Personal year
        if 'personal_year' in results:
            summary_parts.append(f"📅 Personal Year {results['personal_year']['year']}: {results['personal_year']['number']}")
        
        # Check for master numbers
        master_numbers = []
        for key, value in results.items():
            if isinstance(value, dict) and value.get('is_master'):
                master_numbers.append(f"{key.replace('_', ' ').title()}: {value['number']}")
        
        if master_numbers:
            summary_parts.append(f"🔮 Master Numbers: {', '.join(master_numbers)}")
        
        return '\n'.join(summary_parts)
    
    def _handle_results_questions(self, message: str, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle questions about numerology results."""
        message_lower = message.lower()
        results = collected_data.get('numerology_results', {})
        
        # Life Path questions
        if any(word in message_lower for word in ['life path', 'life number']):
            if 'life_path' in results:
                life_path = results['life_path']
                return {
                    'message': f"🛤️ Your Life Path Number is {life_path['number']}\n\n{life_path.get('interpretation', 'No interpretation available.')}\n\nThis number represents your life's journey and primary purpose. It's calculated from your birth date: {life_path.get('calculation', '')}",
                    'type': 'life_path_explanation',
                    'suggestions': ['Tell me about my Destiny number', 'What about my Soul Urge?', 'What are my challenges?']
                }
        
        # Destiny questions
        elif any(word in message_lower for word in ['destiny', 'expression']):
            if 'destiny' in results:
                destiny = results['destiny']
                return {
                    'message': f"⭐ Your Destiny Number is {destiny['number']}\n\n{destiny.get('interpretation', 'No interpretation available.')}\n\nThis number reveals your life's mission and what you're meant to accomplish. It's calculated from the letters in your full name.",
                    'type': 'destiny_explanation',
                    'suggestions': ['Tell me about my Soul Urge', 'What about my Personality number?', 'Show me my lucky numbers']
                }
        
        # Soul Urge questions
        elif any(word in message_lower for word in ['soul urge', 'heart', 'desire']):
            if 'soul_urge' in results:
                soul_urge = results['soul_urge']
                return {
                    'message': f"💫 Your Soul Urge Number is {soul_urge['number']}\n\n{soul_urge.get('interpretation', 'No interpretation available.')}\n\nThis number represents your inner desires and what truly motivates you. It's calculated from the vowels in your name.",
                    'type': 'soul_urge_explanation',
                    'suggestions': ['What about my Personality number?', 'Tell me about my challenges', 'What are my pinnacles?']
                }
        
        # Personality questions
        elif any(word in message_lower for word in ['personality', 'how others see']):
            if 'personality' in results:
                personality = results['personality']
                return {
                    'message': f"🎭 Your Personality Number is {personality['number']}\n\n{personality.get('interpretation', 'No interpretation available.')}\n\nThis number shows how others perceive you and the impression you make. It's calculated from the consonants in your name.",
                    'type': 'personality_explanation',
                    'suggestions': ['What are my lucky numbers?', 'Tell me about my challenges', 'What about karmic lessons?']
                }
        
        # Lucky numbers
        elif any(word in message_lower for word in ['lucky', 'fortune', 'lucky numbers']):
            if 'lucky_numbers' in results:
                lucky_numbers = results['lucky_numbers']
                return {
                    'message': f"🍀 Your Lucky Numbers are: {', '.join(map(str, lucky_numbers))}\n\nThese numbers are derived from your core numerology calculations and are considered particularly harmonious with your energy. You can use these numbers for important decisions, dates, or whenever you need some extra luck!",
                    'type': 'lucky_numbers_explanation',
                    'suggestions': ['Tell me about my challenges', 'What about my personal year?', 'Explain my karmic lessons']
                }
        
        # Challenge numbers
        elif any(word in message_lower for word in ['challenge', 'obstacles', 'lessons']):
            if 'challenge_numbers' in results:
                challenges = results['challenge_numbers']
                return {
                    'message': f"⚡ Your Challenge Numbers are:\n• First Challenge: {challenges['first']}\n• Second Challenge: {challenges['second']}\n• Third Challenge: {challenges['third']}\n• Fourth Challenge: {challenges['fourth']}\n\nThese numbers represent life lessons and obstacles you may need to overcome to reach your full potential.",
                    'type': 'challenge_explanation',
                    'suggestions': ['What are my pinnacles?', 'Tell me about my personal year', 'What about karmic lessons?']
                }
        
        # Personal year
        elif any(word in message_lower for word in ['personal year', 'current year', 'this year']):
            if 'personal_year' in results:
                personal_year = results['personal_year']
                return {
                    'message': f"📅 Your Personal Year for {personal_year['year']} is {personal_year['number']}\n\nThis indicates the theme and energy for your current year. Personal Year cycles help you understand what to focus on and what opportunities or challenges may arise.",
                    'type': 'personal_year_explanation',
                    'suggestions': ['What are my pinnacles?', 'Tell me about my challenges', 'Start over with new information']
                }
        
        # General help
        elif any(word in message_lower for word in ['help', 'what can', 'explain', 'more']):
            return {
                'message': "I can explain any aspect of your numerology profile! Here's what I can tell you about:\n\n🛤️ Life Path Number - Your life's journey\n⭐ Destiny Number - Your life's mission\n💫 Soul Urge Number - Your inner desires\n🎭 Personality Number - How others see you\n🍀 Lucky Numbers - Your fortunate numbers\n⚡ Challenge Numbers - Life lessons to learn\n📅 Personal Year - This year's theme\n🔮 Master Numbers - Special spiritual significance\n\nJust ask about any of these!",
                'type': 'help_menu',
                'suggestions': ['Tell me about my Life Path', 'Explain my Destiny number', 'What are my lucky numbers?', 'Show my challenges']
            }
        
        # Start over
        elif any(word in message_lower for word in ['start over', 'new calculation', 'different name']):
            # Reset session
            collected_data.clear()
            return {
                'message': "No problem! Let's start fresh. 🔄\n\nWhat's your full name?",
                'type': 'restart',
                'suggestions': ['My name is...', 'John Smith']
            }
        
        # Default response for unrecognized questions
        else:
            return {
                'message': "I'd be happy to help explain your numerology results! You can ask me about:\n• Your Life Path, Destiny, Soul Urge, or Personality numbers\n• Your lucky numbers\n• Your challenge numbers\n• Your personal year\n• Or say 'help' for more options",
                'type': 'clarification',
                'suggestions': ['Tell me about my Life Path', 'What are my lucky numbers?', 'Help', 'Explain my Soul Urge']
            }
    
    def _handle_general_conversation(self, message: str) -> Dict[str, Any]:
        """Handle general conversation outside of the main flow."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['help', 'what can you do', 'how does this work']):
            return {
                'message': "I'm your Numerology Chat Assistant! 🔮\n\nI can help you:\n• Calculate your complete numerology profile\n• Explain what each number means\n• Answer questions about numerology\n• Provide personalized insights\n\nTo get started, just say 'hello' or tell me your name!",
                'type': 'help',
                'suggestions': ['Hello', 'Calculate my numerology', 'My name is...']
            }
        
        elif any(word in message_lower for word in ['thanks', 'thank you', 'bye', 'goodbye']):
            return {
                'message': "You're very welcome! ✨ I hope your numerology insights serve you well on your journey. Feel free to come back anytime to explore more about your numbers!",
                'type': 'farewell',
                'suggestions': ['Calculate new numerology', 'Start over']
            }
        
        else:
            return {
                'message': "I'm here to help with numerology calculations and explanations! To get started, you can:\n• Tell me your name to begin a calculation\n• Ask questions about numerology\n• Say 'help' for more information",
                'type': 'general',
                'suggestions': ['Hello', 'Help', 'My name is...', 'What is numerology?']
            }
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
        if session_id in self.user_sessions:
            return self.user_sessions[session_id].get('conversation_history', [])
        return []
    
    def clear_session(self, session_id: str) -> None:
        """Clear a user session."""
        if session_id in self.user_sessions:
            del self.user_sessions[session_id]


# Global instance of the chat service
chat_service = ChatService()