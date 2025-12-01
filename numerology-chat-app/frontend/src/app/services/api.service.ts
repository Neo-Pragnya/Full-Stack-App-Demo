import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { 
  UserInput, 
  ChatMessage, 
  NumerologyResponse, 
  FeedbackRequest, 
  TabClickEvent, 
  APIResponse,
  SessionInfo,
  ChatResponse
} from '../models/interfaces';
import { v4 as uuidv4 } from 'uuid';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api/v1';
  private sessionId: string = '';
  private sessionSubject = new BehaviorSubject<string>('');
  
  constructor(private http: HttpClient) {
    // Initialize session on service creation
    this.initializeSession();
  }

  get sessionId$(): Observable<string> {
    return this.sessionSubject.asObservable();
  }

  get currentSessionId(): string {
    return this.sessionId;
  }

  private getHeaders(): HttpHeaders {
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    });

    if (this.sessionId) {
      headers = headers.set('X-Session-ID', this.sessionId);
    }

    return headers;
  }

  async initializeSession(): Promise<string> {
    try {
      const response = await this.http.post<APIResponse<{session_id: string}>>(
        `${this.baseUrl}/events/session`,
        {},
        { headers: this.getHeaders() }
      ).toPromise();

      if (response && response.data) {
        this.sessionId = response.data.session_id;
        this.sessionSubject.next(this.sessionId);
        console.log('Session initialized:', this.sessionId);
        return this.sessionId;
      }
    } catch (error) {
      console.error('Failed to initialize session:', error);
      // Fallback to local session ID
      this.sessionId = uuidv4();
      this.sessionSubject.next(this.sessionId);
    }
    
    return this.sessionId;
  }

  calculateNumerology(userInput: UserInput): Observable<NumerologyResponse> {
    return this.http.post<NumerologyResponse>(
      `${this.baseUrl}/calculate`,
      userInput,
      { headers: this.getHeaders() }
    );
  }

  sendChatMessage(message: ChatMessage): Observable<APIResponse<ChatResponse>> {
    return this.http.post<APIResponse<ChatResponse>>(
      `${this.baseUrl}/chat`,
      message,
      { headers: this.getHeaders() }
    );
  }

  submitFeedback(feedback: FeedbackRequest): Observable<APIResponse> {
    return this.http.post<APIResponse>(
      `${this.baseUrl}/events/feedback`,
      feedback,
      { headers: this.getHeaders() }
    );
  }

  trackTabClick(tabEvent: TabClickEvent): Observable<APIResponse> {
    return this.http.post<APIResponse>(
      `${this.baseUrl}/events/tab-click`,
      tabEvent,
      { headers: this.getHeaders() }
    );
  }

  getSessionEvents(sessionId?: string): Observable<APIResponse> {
    const id = sessionId || this.sessionId;
    return this.http.get<APIResponse>(
      `${this.baseUrl}/events/session/${id}`,
      { headers: this.getHeaders() }
    );
  }

  getSessionAnalytics(sessionId?: string): Observable<APIResponse> {
    const id = sessionId || this.sessionId;
    return this.http.get<APIResponse>(
      `${this.baseUrl}/analytics/session/${id}`,
      { headers: this.getHeaders() }
    );
  }

  getGlobalAnalytics(): Observable<APIResponse> {
    return this.http.get<APIResponse>(
      `${this.baseUrl}/analytics/global`,
      { headers: this.getHeaders() }
    );
  }

  getConversationHistory(sessionId?: string): Observable<APIResponse> {
    const id = sessionId || this.sessionId;
    return this.http.get<APIResponse>(
      `${this.baseUrl}/conversation/${id}`,
      { headers: this.getHeaders() }
    );
  }

  endSession(sessionId?: string): Observable<APIResponse> {
    const id = sessionId || this.sessionId;
    return this.http.delete<APIResponse>(
      `${this.baseUrl}/session/${id}`,
      { headers: this.getHeaders() }
    );
  }

  checkHealth(): Observable<APIResponse> {
    return this.http.get<APIResponse>(
      `${this.baseUrl}/health`,
      { headers: this.getHeaders() }
    );
  }
}