import { Component, OnInit, OnDestroy, ViewChild, ElementRef } from '@angular/core';
import { Subscription } from 'rxjs';
import { ApiService } from '../../services/api.service';
import { NumerologyService } from '../../services/numerology.service';
import { 
  ChatMessage, 
  FeedbackRequest, 
  ChatResponse,
  APIResponse
} from '../../models/interfaces';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit, OnDestroy {
  @ViewChild('chatContainer') chatContainer!: ElementRef;
  @ViewChild('messageInput') messageInput!: ElementRef;

  messages: ChatMessage[] = [];
  currentMessage: string = '';
  isLoading: boolean = false;
  sessionId: string = '';
  private subscriptions: Subscription[] = [];

  constructor(
    private apiService: ApiService,
    private numerologyService: NumerologyService
  ) {}

  ngOnInit(): void {
    this.initializeChat();
    this.subscribeToSession();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private initializeChat(): void {
    // Add welcome message
    this.messages = [{
      message: "👋 Welcome to the Numerology Chat! I'm here to help you discover your numerology profile. Let's start by getting to know you!",
      sender: 'bot',
      timestamp: new Date(),
      suggestions: ['Hello!', 'Hi there!', 'Let\'s begin!']
    }];
  }

  private subscribeToSession(): void {
    const sessionSub = this.apiService.sessionId$.subscribe(sessionId => {
      this.sessionId = sessionId;
    });
    this.subscriptions.push(sessionSub);
  }

  sendMessage(): void {
    if (!this.currentMessage.trim() || this.isLoading) return;

    const userMessage: ChatMessage = {
      message: this.currentMessage.trim(),
      sender: 'user',
      timestamp: new Date()
    };

    this.messages.push(userMessage);
    this.currentMessage = '';
    this.isLoading = true;
    this.scrollToBottom();

    // Send message to backend
    const chatSub = this.apiService.sendChatMessage(userMessage).subscribe({
      next: (response: APIResponse<ChatResponse>) => {
        this.isLoading = false;
        
        if (response.status === 'success' && response.data) {
          const botMessage: ChatMessage = {
            message: response.data.message,
            sender: 'bot',
            timestamp: new Date(),
            type: response.data.type,
            suggestions: response.data.suggestions,
            data: response.data.data
          };

          this.messages.push(botMessage);

          // If we received numerology data, update the service
          if (response.data.data && response.data.type === 'calculation_complete') {
            this.numerologyService.setNumerologyResults(response.data.data);
          }

          this.scrollToBottom();
        }
      },
      error: (error) => {
        this.isLoading = false;
        console.error('Chat error:', error);
        
        const errorMessage: ChatMessage = {
          message: "I'm sorry, I encountered an error. Please try again.",
          sender: 'bot',
          timestamp: new Date()
        };
        
        this.messages.push(errorMessage);
        this.scrollToBottom();
      }
    });

    this.subscriptions.push(chatSub);
  }

  useSuggestion(suggestion: string): void {
    this.currentMessage = suggestion;
    this.sendMessage();
  }

  submitFeedback(message: ChatMessage, feedbackType: 'up' | 'down'): void {
    const feedback: FeedbackRequest = {
      feedback_type: feedbackType,
      target_type: 'chat_message',
      target_id: message.timestamp?.getTime().toString(),
      additional_data: {
        message_content: message.message,
        message_type: message.type
      }
    };

    const feedbackSub = this.apiService.submitFeedback(feedback).subscribe({
      next: (response) => {
        console.log('Feedback submitted:', response);
        // Optionally show a toast notification
      },
      error: (error) => {
        console.error('Feedback error:', error);
      }
    });

    this.subscriptions.push(feedbackSub);
  }

  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      if (this.chatContainer) {
        const element = this.chatContainer.nativeElement;
        element.scrollTop = element.scrollHeight;
      }
    }, 100);
  }

  clearChat(): void {
    this.messages = [];
    this.initializeChat();
  }

  exportChat(): void {
    const chatData = {
      session_id: this.sessionId,
      messages: this.messages,
      exported_at: new Date()
    };

    const dataStr = JSON.stringify(chatData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `chat_export_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  }

  getMessageClasses(message: ChatMessage): string {
    const baseClasses = 'message-bubble';
    return `${baseClasses} ${message.sender === 'user' ? 'user-message' : 'bot-message'}`;
  }

  formatTimestamp(timestamp?: Date): string {
    if (!timestamp) return '';
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
}