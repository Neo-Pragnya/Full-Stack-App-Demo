import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { ApiService } from '../../services/api.service';
import { NumerologyService } from '../../services/numerology.service';
import { 
  NumerologyResults, 
  NumerologyCategory,
  TabClickEvent
} from '../../models/interfaces';

@Component({
  selector: 'app-numerology-tabs',
  templateUrl: './numerology-tabs.component.html',
  styleUrls: ['./numerology-tabs.component.scss']
})
export class NumerologyTabsComponent implements OnInit, OnDestroy {
  results: NumerologyResults | null = null;
  categories: NumerologyCategory[] = [];
  activeTab: string = 'summary';
  
  private subscriptions: Subscription[] = [];

  tabs = [
    { id: 'summary', name: 'Summary', icon: '🌟', category: 'overview' },
    { id: 'core', name: 'Core Numbers', icon: '🎯', category: 'core_numbers' },
    { id: 'advanced', name: 'Advanced', icon: '🔬', category: 'advanced_numbers' },
    { id: 'cycles', name: 'Life Cycles', icon: '🔄', category: 'life_cycles' },
    { id: 'spiritual', name: 'Spiritual', icon: '🕉️', category: 'spiritual_aspects' },
    { id: 'timing', name: 'Timing', icon: '⏰', category: 'timing_analysis' }
  ];

  constructor(
    public numerologyService: NumerologyService,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.subscribeToResults();
    this.subscribeToActiveTab();
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

  private subscribeToResults(): void {
    const resultsSub = this.numerologyService.numerologyResults$.subscribe(results => {
      this.results = results;
      if (results) {
        this.categories = this.numerologyService.getNumerologyCategories(results);
      }
    });
    this.subscriptions.push(resultsSub);
  }

  private subscribeToActiveTab(): void {
    const tabSub = this.numerologyService.activeTab$.subscribe(tab => {
      this.activeTab = tab;
    });
    this.subscriptions.push(tabSub);
  }

  selectTab(tabId: string): void {
    const previousTab = this.activeTab;
    this.activeTab = tabId;
    this.numerologyService.setActiveTab(tabId);

    // Track tab click event
    const tab = this.tabs.find(t => t.id === tabId);
    if (tab) {
      const tabEvent: TabClickEvent = {
        tab_name: tab.name,
        tab_category: tab.category,
        previous_tab: previousTab
      };

      const trackSub = this.apiService.trackTabClick(tabEvent).subscribe({
        next: (response) => {
          console.log('Tab click tracked:', response);
        },
        error: (error) => {
          console.error('Error tracking tab click:', error);
        }
      });
      this.subscriptions.push(trackSub);
    }
  }

  getCoreNumbers() {
    if (!this.results) return {};
    return {
      'Life Path': this.results.life_path,
      'Destiny': this.results.destiny,
      'Soul Urge': this.results.soul_urge,
      'Personality': this.results.personality
    };
  }

  getAdvancedNumbers() {
    if (!this.results) return {};
    return {
      'Birth Day': this.results.birth_day,
      'Balance': this.results.balance_number,
      'Hidden Passion': this.results.hidden_passion
    };
  }

  getLifeCycles() {
    if (!this.results) return {};
    return {
      'Personal Year': this.results.personal_year,
      'Challenges': this.results.challenge_numbers,
      'Pinnacles': this.results.pinnacle_numbers
    };
  }

  getSpiritualAspects() {
    if (!this.results) return {};
    return {
      'Karmic Lessons': this.results.karmic_lessons
    };
  }

  getMasterNumbers() {
    if (!this.results) return [];
    
    const masterNumbers = [];
    const numbersToCheck = [
      { name: 'Life Path', data: this.results.life_path },
      { name: 'Destiny', data: this.results.destiny },
      { name: 'Soul Urge', data: this.results.soul_urge },
      { name: 'Personality', data: this.results.personality },
      { name: 'Birth Day', data: this.results.birth_day },
      { name: 'Balance', data: this.results.balance_number }
    ];

    for (const numberInfo of numbersToCheck) {
      if (numberInfo.data.is_master) {
        masterNumbers.push({
          name: numberInfo.name,
          number: numberInfo.data.number,
          interpretation: numberInfo.data.interpretation
        });
      }
    }

    return masterNumbers;
  }

  getSummaryData() {
    if (!this.results) return null;
    
    const coreNumbers = this.getCoreNumbers();
    const masterNumbers = this.getMasterNumbers();
    
    return {
      core: coreNumbers,
      master: masterNumbers,
      personalYear: this.results.personal_year,
      luckyNumbers: this.results.lucky_numbers
    };
  }

  formatNumber(value: any): string {
    if (Array.isArray(value)) {
      return value.join(', ');
    }
    return String(value);
  }

  isNumberMaster(number: any): boolean {
    if (typeof number === 'object' && number.is_master) {
      return true;
    }
    const numValue = typeof number === 'object' ? number.number : number;
    return this.numerologyService.isMasterNumber(numValue);
  }
}