// Interfaces for the Numerology Chat Application

export interface UserInput {
  full_name: string;
  birth_date: string;
}

export interface ChatMessage {
  message: string;
  timestamp?: Date;
  sender: 'user' | 'bot';
  message_type?: string;
  suggestions?: string[];
  type?: string;
  data?: any;
}

export interface NumerologyResponse {
  success: boolean;
  data?: NumerologyResults;
  error?: string;
  timestamp?: Date;
}

export interface NumerologyResults {
  life_path: NumerologyNumber;
  destiny: NumerologyNumber;
  soul_urge: NumerologyNumber;
  personality: NumerologyNumber;
  birth_day: NumerologyNumber;
  balance_number: NumerologyNumber;
  hidden_passion: NumerologyNumber;
  challenge_numbers: ChallengeNumbers;
  pinnacle_numbers: PinnacleNumbers;
  personal_year: PersonalYear;
  lucky_numbers: number[];
  karmic_lessons: KarmicLessons;
  name_analysis: NameAnalysis;
}

export interface NumerologyNumber {
  number: number | number[];
  calculation?: string;
  interpretation?: string;
  is_master?: boolean;
  is_karmic_debt?: boolean;
  karmic_debt_number?: number;
  vowels_used?: string[];
  consonants_used?: string[];
  initials?: string;
  frequency_map?: { [key: number]: number };
  letter_breakdown?: { [key: string]: { value: number; count: number } };
}

export interface ChallengeNumbers {
  first: number;
  second: number;
  third: number;
  fourth: number;
  calculation: string;
}

export interface PinnacleNumbers {
  first: number;
  second: number;
  third: number;
  fourth: number;
  calculation: string;
}

export interface PersonalYear {
  number: number;
  calculation: string;
  year: number;
}

export interface KarmicLessons {
  missing_numbers: number[];
  present_numbers: number[];
  calculation: string;
}

export interface NameAnalysis {
  word_count: number;
  total_letters: number;
  vowel_count: number;
  consonant_count: number;
  words: WordAnalysis[];
}

export interface WordAnalysis {
  word: string;
  position: number;
  value: number;
  reduced: number;
  is_master: boolean;
}

export interface FeedbackRequest {
  feedback_type: 'up' | 'down';
  target_type: string;
  target_id?: string;
  additional_data?: any;
}

export interface TabClickEvent {
  tab_name: string;
  tab_category: string;
  previous_tab?: string;
}

export interface UserEvent {
  event_type: EventType;
  event_data?: any;
  timestamp?: Date;
  session_id?: string;
  user_ip?: string;
}

export enum EventType {
  CHAT_MESSAGE = 'chat_message',
  THUMBS_UP = 'thumbs_up',
  THUMBS_DOWN = 'thumbs_down',
  TAB_CLICK = 'tab_click',
  NUMEROLOGY_CALCULATION = 'numerology_calculation',
  SESSION_START = 'session_start',
  SESSION_END = 'session_end'
}

export interface APIResponse<T = any> {
  status: string;
  message: string;
  data?: T;
  timestamp: Date;
}

export interface SessionInfo {
  session_id: string;
  start_time: Date;
  user_agent?: string;
  ip_address?: string;
}

export interface NumerologyCategory {
  name: string;
  icon: string;
  description: string;
  numbers: { [key: string]: NumerologyNumber };
}

export interface ChatResponse {
  message: string;
  type: string;
  suggestions?: string[];
  data?: any;
}