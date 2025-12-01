import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { ApiService } from './services/api.service';
import { NumerologyService } from './services/numerology.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'Numerology Chat App';
  isLoading = true;
  sessionId: string = '';
  private subscriptions: Subscription[] = [];

  constructor(
    private apiService: ApiService,
    private numerologyService: NumerologyService
  ) {}

  async ngOnInit(): Promise<void> {
    await this.initializeApp();
    this.subscribeToSession();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
    if (this.sessionId) {
      this.apiService.endSession(this.sessionId).subscribe();
    }
  }

  private async initializeApp(): Promise<void> {
    try {
      // Check backend health
      this.apiService.checkHealth().subscribe({
        next: (response) => {
          console.log('Backend health check:', response);
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Backend health check failed:', error);
          this.isLoading = false;
        }
      });

      // Initialize session
      await this.apiService.initializeSession();
    } catch (error) {
      console.error('Failed to initialize app:', error);
      this.isLoading = false;
    }
  }

  private subscribeToSession(): void {
    const sessionSub = this.apiService.sessionId$.subscribe(sessionId => {
      this.sessionId = sessionId;
      console.log('App session ID:', sessionId);
    });
    this.subscriptions.push(sessionSub);
  }
}