import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { 
  NumerologyResults, 
  NumerologyCategory,
  NumerologyNumber
} from '../models/interfaces';

@Injectable({
  providedIn: 'root'
})
export class NumerologyService {
  private numerologyResultsSubject = new BehaviorSubject<NumerologyResults | null>(null);
  private activeTabSubject = new BehaviorSubject<string>('summary');

  constructor() {}

  get numerologyResults$(): Observable<NumerologyResults | null> {
    return this.numerologyResultsSubject.asObservable();
  }

  get activeTab$(): Observable<string> {
    return this.activeTabSubject.asObservable();
  }

  setNumerologyResults(results: NumerologyResults): void {
    this.numerologyResultsSubject.next(results);
  }

  setActiveTab(tabName: string): void {
    this.activeTabSubject.next(tabName);
  }

  getNumerologyCategories(results: NumerologyResults): NumerologyCategory[] {
    if (!results) return [];

    return [
      {
        name: 'Core Numbers',
        icon: '🌟',
        description: 'Your fundamental numerology numbers',
        numbers: {
          'Life Path': results.life_path,
          'Destiny': results.destiny,
          'Soul Urge': results.soul_urge,
          'Personality': results.personality
        }
      },
      {
        name: 'Advanced Numbers',
        icon: '🔬',
        description: 'Deeper insights into your numerology profile',
        numbers: {
          'Birth Day': results.birth_day,
          'Balance': results.balance_number,
          'Hidden Passion': results.hidden_passion
        }
      },
      {
        name: 'Life Cycles',
        icon: '🔄',
        description: 'Your life phases and challenges',
        numbers: {
          'Personal Year': results.personal_year as any,
          'Challenges': results.challenge_numbers as any,
          'Pinnacles': results.pinnacle_numbers as any
        }
      },
      {
        name: 'Spiritual Aspects',
        icon: '🕉️',
        description: 'Karmic lessons and spiritual insights',
        numbers: {
          'Karmic Lessons': results.karmic_lessons as any
        }
      }
    ];
  }

  getNumberInterpretation(numberType: string, number: number): string {
    const interpretations: { [key: string]: { [key: number]: string } } = {
      'life_path': {
        1: "You are a natural leader with a pioneering spirit. Your path involves independence and innovation.",
        2: "You are diplomatic and cooperative. Your path involves bringing people together in harmony.",
        3: "You are creative and expressive. Your path involves inspiring others through artistic expression.",
        4: "You are practical and hardworking. Your path involves building solid foundations.",
        5: "You are adventurous and freedom-loving. Your path involves experiencing life and inspiring change.",
        6: "You are nurturing and responsible. Your path involves caring for others and creating harmony.",
        7: "You are analytical and spiritual. Your path involves seeking deeper truths and wisdom.",
        8: "You are ambitious and material-focused. Your path involves achieving success and recognition.",
        9: "You are humanitarian and generous. Your path involves serving humanity with wisdom.",
        11: "Master number of intuition and spiritual insight. You're meant to inspire and enlighten.",
        22: "Master number of building dreams into reality. You're meant to create lasting value.",
        33: "Master number of selfless service. You're meant to teach and heal with compassion."
      },
      'destiny': {
        1: "Your life purpose is to lead, innovate, and pioneer new paths for others.",
        2: "Your life purpose is to cooperate, mediate, and bring people together.",
        3: "Your life purpose is to create, communicate, and inspire through expression.",
        4: "Your life purpose is to build, organize, and create lasting foundations.",
        5: "Your life purpose is to experience freedom and inspire others to grow.",
        6: "Your life purpose is to nurture, heal, and create harmony in relationships.",
        7: "Your life purpose is to analyze, research, and uncover hidden truths.",
        8: "Your life purpose is to achieve material success and use power responsibly.",
        9: "Your life purpose is to serve humanity with wisdom and compassion."
      },
      'soul_urge': {
        1: "Deep desire for independence, leadership, and being first in everything.",
        2: "Deep desire for peace, cooperation, and meaningful relationships.",
        3: "Deep desire for creative expression and inspiring others with your talents.",
        4: "Deep desire for security, order, and building something lasting.",
        5: "Deep desire for freedom, adventure, and experiencing all life offers.",
        6: "Deep desire to nurture, protect, and care for family and community.",
        7: "Deep desire for knowledge, spiritual understanding, and inner wisdom.",
        8: "Deep desire for material success, recognition, and positions of authority.",
        9: "Deep desire to serve humanity and make the world a better place."
      },
      'personality': {
        1: "Others see you as confident, independent, and a natural leader.",
        2: "Others see you as gentle, cooperative, and easy to work with.",
        3: "Others see you as creative, optimistic, and entertaining.",
        4: "Others see you as reliable, practical, and hardworking.",
        5: "Others see you as dynamic, adventurous, and progressive.",
        6: "Others see you as caring, responsible, and family-oriented.",
        7: "Others see you as mysterious, intellectual, and spiritual.",
        8: "Others see you as successful, authoritative, and business-minded.",
        9: "Others see you as wise, generous, and humanitarian."
      }
    };

    return interpretations[numberType]?.[number] || `Interpretation for ${numberType} number ${number} not available.`;
  }

  isMasterNumber(number: number): boolean {
    return [11, 22, 33, 44, 55, 66, 77, 88, 99].includes(number);
  }

  formatCalculation(calculation: string): string {
    // Format calculation string for better display
    return calculation.replace(/→/g, '→').replace(/=/g, ' = ');
  }

  getPersonalYearMeaning(number: number): string {
    const meanings: { [key: number]: string } = {
      1: "A year of new beginnings, independence, and starting fresh projects.",
      2: "A year of cooperation, partnerships, and patience with slow progress.",
      3: "A year of creativity, self-expression, and social expansion.",
      4: "A year of hard work, building foundations, and practical matters.",
      5: "A year of change, freedom, and new opportunities.",
      6: "A year of responsibility, family matters, and service to others.",
      7: "A year of introspection, spiritual growth, and inner development.",
      8: "A year of material achievement, business success, and recognition.",
      9: "A year of completion, endings, and preparing for new cycles."
    };

    return meanings[number] || `Personal year ${number} interpretation not available.`;
  }

  getChallengeMeaning(challengeNumber: number): string {
    const meanings: { [key: number]: string } = {
      0: "No challenge - You have the gifts to handle this area naturally.",
      1: "Learn to be independent and develop leadership skills.",
      2: "Learn patience, cooperation, and how to work with others.",
      3: "Learn to express yourself creatively and communicate effectively.",
      4: "Learn discipline, organization, and practical application.",
      5: "Learn to use freedom constructively and avoid scattered energy.",
      6: "Learn responsibility and how to balance service to others with self-care.",
      7: "Learn to trust your intuition and develop spiritual understanding.",
      8: "Learn to handle material success and use power responsibly."
    };

    return meanings[challengeNumber] || `Challenge number ${challengeNumber} interpretation not available.`;
  }

  getLuckyNumbersDescription(numbers: number[]): string {
    return `Your lucky numbers ${numbers.join(', ')} are derived from your core numerology calculations and are considered particularly harmonious with your energy.`;
  }

  getKarmicLessonsDescription(missingNumbers: number[]): string {
    if (missingNumbers.length === 0) {
      return "Congratulations! You have no karmic lessons, meaning all numbers 1-9 are represented in your name.";
    }

    const lessons: { [key: number]: string } = {
      1: "Learn independence and leadership",
      2: "Learn cooperation and patience",
      3: "Learn creative expression and communication",
      4: "Learn discipline and practical application",
      5: "Learn freedom and constructive use of freedom",
      6: "Learn responsibility and nurturing",
      7: "Learn faith and spiritual understanding",
      8: "Learn material mastery and business sense",
      9: "Learn universal love and humanitarian service"
    };

    return `Areas for development: ${missingNumbers.map(n => `${n}: ${lessons[n]}`).join(', ')}`;
  }
}