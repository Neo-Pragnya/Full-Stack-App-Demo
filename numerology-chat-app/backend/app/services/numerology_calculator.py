"""
Advanced Numerology Calculator
Implements comprehensive numerology calculations including all core numbers,
karmic debt numbers, master numbers, and detailed interpretations.
"""

from datetime import datetime
import re
from typing import Dict, List, Tuple, Optional


class NumerologyCalculator:
    """Advanced numerology calculator with comprehensive number interpretations."""
    
    # Master numbers that are not reduced
    MASTER_NUMBERS = {11, 22, 33, 44, 55, 66, 77, 88, 99}
    
    # Karmic debt numbers
    KARMIC_DEBT_NUMBERS = {13, 14, 16, 19}
    
    # Letter to number mapping (Pythagorean system)
    LETTER_VALUES = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    
    # Vowels for Soul Urge calculation
    VOWELS = set('AEIOU')
    
    # Consonants for Personality calculation
    CONSONANTS = set('BCDFGHJKLMNPQRSTVWXYZ')
    
    def __init__(self):
        self.interpretations = self._load_interpretations()
    
    def calculate_all_numbers(self, full_name: str, birth_date: str) -> Dict:
        """Calculate all numerology numbers for a person."""
        try:
            # Parse birth date
            birth_datetime = datetime.strptime(birth_date, "%Y-%m-%d")
            
            # Clean the name
            clean_name = self._clean_name(full_name)
            
            # Calculate all numbers
            results = {
                'life_path': self._calculate_life_path(birth_datetime),
                'destiny': self._calculate_destiny(clean_name),
                'soul_urge': self._calculate_soul_urge(clean_name),
                'personality': self._calculate_personality(clean_name),
                'maturity': self._calculate_maturity(),
                'birth_day': self._calculate_birth_day(birth_datetime),
                'expression': self._calculate_expression(clean_name),
                'hearts_desire': self._calculate_hearts_desire(clean_name),
                'hidden_passion': self._calculate_hidden_passion(clean_name),
                'karmic_lessons': self._calculate_karmic_lessons(clean_name),
                'balance_number': self._calculate_balance_number(clean_name),
                'challenge_numbers': self._calculate_challenge_numbers(birth_datetime),
                'pinnacle_numbers': self._calculate_pinnacle_numbers(birth_datetime),
                'personal_year': self._calculate_personal_year(birth_datetime),
                'lucky_numbers': self._calculate_lucky_numbers(clean_name, birth_datetime),
                'name_analysis': self._analyze_name_components(clean_name)
            }
            
            # Add interpretations
            for key, value in results.items():
                if isinstance(value, dict) and 'number' in value:
                    # Only add interpretation if number is an integer (not a list)
                    if isinstance(value['number'], int):
                        results[key]['interpretation'] = self._get_interpretation(key, value['number'])
                elif isinstance(value, int):
                    results[key] = {
                        'number': value,
                        'interpretation': self._get_interpretation(key, value)
                    }
            
            return results
            
        except Exception as e:
            return {'error': f"Calculation error: {str(e)}"}
    
    def _clean_name(self, name: str) -> str:
        """Clean name by removing non-alphabetic characters and converting to uppercase."""
        return re.sub(r'[^A-Za-z\s]', '', name).upper().strip()
    
    def _reduce_to_single_digit(self, number: int, preserve_master: bool = True) -> int:
        """Reduce a number to single digit, preserving master numbers if specified."""
        if preserve_master and number in self.MASTER_NUMBERS:
            return number
        
        while number > 9:
            if preserve_master and number in self.MASTER_NUMBERS:
                return number
            number = sum(int(digit) for digit in str(number))
        
        return number
    
    def _calculate_life_path(self, birth_date: datetime) -> Dict:
        """Calculate Life Path number - the most important number in numerology."""
        day = birth_date.day
        month = birth_date.month
        year = birth_date.year
        
        # Reduce each component separately first
        day_reduced = self._reduce_to_single_digit(day)
        month_reduced = self._reduce_to_single_digit(month)
        year_reduced = self._reduce_to_single_digit(year)
        
        # Add them together
        total = day_reduced + month_reduced + year_reduced
        life_path = self._reduce_to_single_digit(total)
        
        # Check for karmic debt
        is_karmic = total in self.KARMIC_DEBT_NUMBERS
        
        return {
            'number': life_path,
            'calculation': f"{day} + {month} + {year} = {day + month + year} → {life_path}",
            'is_master': life_path in self.MASTER_NUMBERS,
            'is_karmic_debt': is_karmic,
            'karmic_debt_number': total if is_karmic else None
        }
    
    def _calculate_destiny(self, name: str) -> Dict:
        """Calculate Destiny number (Expression number) from full name."""
        total = sum(self.LETTER_VALUES.get(char, 0) for char in name if char.isalpha())
        destiny = self._reduce_to_single_digit(total)
        
        return {
            'number': destiny,
            'calculation': f"Sum of all letters = {total} → {destiny}",
            'is_master': destiny in self.MASTER_NUMBERS,
            'letter_breakdown': self._get_letter_breakdown(name)
        }
    
    def _calculate_soul_urge(self, name: str) -> Dict:
        """Calculate Soul Urge number from vowels in the name."""
        vowel_sum = sum(self.LETTER_VALUES.get(char, 0) for char in name if char in self.VOWELS)
        soul_urge = self._reduce_to_single_digit(vowel_sum)
        
        vowels_found = [char for char in name if char in self.VOWELS]
        
        return {
            'number': soul_urge,
            'calculation': f"Vowels ({', '.join(vowels_found)}) = {vowel_sum} → {soul_urge}",
            'is_master': soul_urge in self.MASTER_NUMBERS,
            'vowels_used': vowels_found
        }
    
    def _calculate_personality(self, name: str) -> Dict:
        """Calculate Personality number from consonants in the name."""
        consonant_sum = sum(self.LETTER_VALUES.get(char, 0) for char in name if char in self.CONSONANTS)
        personality = self._reduce_to_single_digit(consonant_sum)
        
        consonants_found = [char for char in name if char in self.CONSONANTS]
        
        return {
            'number': personality,
            'calculation': f"Consonants = {consonant_sum} → {personality}",
            'is_master': personality in self.MASTER_NUMBERS,
            'consonants_used': consonants_found
        }
    
    def _calculate_maturity(self) -> Dict:
        """Calculate Maturity number (Life Path + Destiny)."""
        # This will be calculated after we have both numbers
        return {'number': 0, 'calculation': 'Life Path + Destiny'}
    
    def _calculate_birth_day(self, birth_date: datetime) -> Dict:
        """Calculate Birth Day number."""
        day = birth_date.day
        birth_day = self._reduce_to_single_digit(day)
        
        return {
            'number': birth_day,
            'calculation': f"Day of birth: {day} → {birth_day}",
            'is_master': birth_day in self.MASTER_NUMBERS
        }
    
    def _calculate_expression(self, name: str) -> Dict:
        """Calculate Expression number (same as Destiny but with different interpretation)."""
        return self._calculate_destiny(name)
    
    def _calculate_hearts_desire(self, name: str) -> Dict:
        """Calculate Heart's Desire number (same as Soul Urge)."""
        return self._calculate_soul_urge(name)
    
    def _calculate_hidden_passion(self, name: str) -> Dict:
        """Calculate Hidden Passion number (most frequent letter value)."""
        letter_counts = {}
        for char in name:
            if char.isalpha():
                value = self.LETTER_VALUES.get(char, 0)
                letter_counts[value] = letter_counts.get(value, 0) + 1
        
        if not letter_counts:
            return {'number': 0, 'calculation': 'No letters found'}
        
        max_count = max(letter_counts.values())
        most_frequent = [num for num, count in letter_counts.items() if count == max_count]
        
        return {
            'number': most_frequent[0] if len(most_frequent) == 1 else most_frequent,
            'calculation': f"Most frequent number(s): {most_frequent} (appears {max_count} times)",
            'frequency_map': letter_counts
        }
    
    def _calculate_karmic_lessons(self, name: str) -> Dict:
        """Calculate Karmic Lessons (missing numbers from name)."""
        present_numbers = set()
        for char in name:
            if char.isalpha():
                present_numbers.add(self.LETTER_VALUES.get(char, 0))
        
        all_numbers = set(range(1, 10))
        missing_numbers = all_numbers - present_numbers
        
        return {
            'missing_numbers': sorted(list(missing_numbers)),
            'present_numbers': sorted(list(present_numbers)),
            'calculation': f"Missing numbers from name: {sorted(list(missing_numbers))}"
        }
    
    def _calculate_balance_number(self, name: str) -> Dict:
        """Calculate Balance number from initials."""
        words = name.split()
        initials = ''.join(word[0] for word in words if word)
        
        total = sum(self.LETTER_VALUES.get(char, 0) for char in initials)
        balance = self._reduce_to_single_digit(total)
        
        return {
            'number': balance,
            'calculation': f"Initials ({initials}) = {total} → {balance}",
            'initials': initials
        }
    
    def _calculate_challenge_numbers(self, birth_date: datetime) -> Dict:
        """Calculate the four Challenge numbers."""
        day = self._reduce_to_single_digit(birth_date.day)
        month = self._reduce_to_single_digit(birth_date.month)
        year = self._reduce_to_single_digit(birth_date.year)
        
        first_challenge = abs(day - month)
        second_challenge = abs(day - year)
        third_challenge = abs(first_challenge - second_challenge)
        fourth_challenge = abs(month - year)
        
        return {
            'first': first_challenge,
            'second': second_challenge,
            'third': third_challenge,
            'fourth': fourth_challenge,
            'calculation': f"Based on day({day}), month({month}), year({year})"
        }
    
    def _calculate_pinnacle_numbers(self, birth_date: datetime) -> Dict:
        """Calculate the four Pinnacle numbers."""
        day = self._reduce_to_single_digit(birth_date.day)
        month = self._reduce_to_single_digit(birth_date.month)
        year = self._reduce_to_single_digit(birth_date.year)
        
        first_pinnacle = self._reduce_to_single_digit(day + month)
        second_pinnacle = self._reduce_to_single_digit(day + year)
        third_pinnacle = self._reduce_to_single_digit(first_pinnacle + second_pinnacle)
        fourth_pinnacle = self._reduce_to_single_digit(month + year)
        
        return {
            'first': first_pinnacle,
            'second': second_pinnacle,
            'third': third_pinnacle,
            'fourth': fourth_pinnacle,
            'calculation': f"Based on day({day}), month({month}), year({year})"
        }
    
    def _calculate_personal_year(self, birth_date: datetime) -> Dict:
        """Calculate Personal Year number for current year."""
        current_year = datetime.now().year
        birth_month = birth_date.month
        birth_day = birth_date.day
        
        total = birth_month + birth_day + current_year
        personal_year = self._reduce_to_single_digit(total)
        
        return {
            'number': personal_year,
            'calculation': f"{birth_month} + {birth_day} + {current_year} = {total} → {personal_year}",
            'year': current_year
        }
    
    def _calculate_lucky_numbers(self, name: str, birth_date: datetime) -> List[int]:
        """Calculate a set of lucky numbers based on various calculations."""
        lucky_numbers = set()
        
        # Add Life Path number
        life_path = self._calculate_life_path(birth_date)['number']
        lucky_numbers.add(life_path)
        
        # Add Destiny number
        destiny = self._calculate_destiny(name)['number']
        lucky_numbers.add(destiny)
        
        # Add Birth Day number
        birth_day = self._calculate_birth_day(birth_date)['number']
        lucky_numbers.add(birth_day)
        
        # Add some calculated combinations
        lucky_numbers.add((life_path + destiny) % 9 + 1)
        lucky_numbers.add((birth_date.day + birth_date.month) % 9 + 1)
        
        return sorted(list(lucky_numbers))
    
    def _analyze_name_components(self, name: str) -> Dict:
        """Analyze different components of the name."""
        words = name.split()
        
        analysis = {
            'word_count': len(words),
            'total_letters': len([c for c in name if c.isalpha()]),
            'vowel_count': len([c for c in name if c in self.VOWELS]),
            'consonant_count': len([c for c in name if c in self.CONSONANTS]),
            'words': []
        }
        
        for i, word in enumerate(words):
            word_value = sum(self.LETTER_VALUES.get(char, 0) for char in word)
            word_reduced = self._reduce_to_single_digit(word_value)
            
            analysis['words'].append({
                'word': word,
                'position': i + 1,
                'value': word_value,
                'reduced': word_reduced,
                'is_master': word_reduced in self.MASTER_NUMBERS
            })
        
        return analysis
    
    def _get_letter_breakdown(self, name: str) -> Dict:
        """Get detailed breakdown of letters and their values."""
        breakdown = {}
        for char in name:
            if char.isalpha():
                value = self.LETTER_VALUES.get(char, 0)
                if char not in breakdown:
                    breakdown[char] = {'value': value, 'count': 0}
                breakdown[char]['count'] += 1
        
        return breakdown
    
    def _load_interpretations(self) -> Dict:
        """Load detailed interpretations for all numbers and types."""
        return {
            'life_path': {
                1: "Natural leader, independent, pioneering spirit. You're meant to be a leader and innovator.",
                2: "Cooperative, diplomatic, sensitive. You're meant to be a peacemaker and work well with others.",
                3: "Creative, expressive, optimistic. You're meant to inspire and uplift others through creativity.",
                4: "Practical, hardworking, reliable. You're meant to build solid foundations and systems.",
                5: "Adventurous, freedom-loving, versatile. You're meant to experience life and inspire change.",
                6: "Nurturing, responsible, caring. You're meant to care for others and create harmony.",
                7: "Analytical, spiritual, introspective. You're meant to seek deeper truths and wisdom.",
                8: "Ambitious, material success, authority. You're meant to achieve material success and recognition.",
                9: "Humanitarian, generous, wise. You're meant to serve humanity and share your wisdom.",
                11: "Intuitive, inspirational, enlightened. Master number of intuition and spiritual insight.",
                22: "Master builder, practical visionary. Master number of building dreams into reality.",
                33: "Master teacher, compassionate service. Master number of selfless service to humanity."
            },
            'destiny': {
                1: "Your life purpose is to lead, innovate, and pioneer new paths for others to follow.",
                2: "Your life purpose is to cooperate, mediate, and bring people together in harmony.",
                3: "Your life purpose is to create, communicate, and inspire others through artistic expression.",
                4: "Your life purpose is to build, organize, and create lasting foundations for society.",
                5: "Your life purpose is to experience freedom, promote progress, and inspire others to grow.",
                6: "Your life purpose is to nurture, heal, and create harmony in family and community.",
                7: "Your life purpose is to analyze, research, and uncover hidden truths and wisdom.",
                8: "Your life purpose is to achieve material success and use power responsibly.",
                9: "Your life purpose is to serve humanity with wisdom, compassion, and generosity.",
                11: "Your life purpose is to inspire and enlighten others through intuitive wisdom.",
                22: "Your life purpose is to build something of lasting value that benefits humanity.",
                33: "Your life purpose is to teach and serve others with unconditional love and compassion."
            },
            'soul_urge': {
                1: "Deep desire for independence, leadership, and being first in everything you do.",
                2: "Deep desire for peace, cooperation, and meaningful relationships with others.",
                3: "Deep desire for creative expression, joy, and inspiring others through your talents.",
                4: "Deep desire for security, order, and building something solid and lasting.",
                5: "Deep desire for freedom, adventure, and experiencing all that life has to offer.",
                6: "Deep desire to nurture, protect, and care for family and community.",
                7: "Deep desire for knowledge, spiritual understanding, and inner wisdom.",
                8: "Deep desire for material success, recognition, and positions of authority.",
                9: "Deep desire to serve humanity and make the world a better place.",
                11: "Deep desire to inspire others and serve as a spiritual beacon of light.",
                22: "Deep desire to manifest grand visions that benefit all of humanity.",
                33: "Deep desire to heal and teach others through unconditional love and service."
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
                9: "Others see you as wise, generous, and humanitarian.",
                11: "Others see you as intuitive, inspiring, and spiritually aware.",
                22: "Others see you as a visionary with the ability to make dreams reality.",
                33: "Others see you as a natural healer and teacher with deep compassion."
            }
        }
    
    def _get_interpretation(self, number_type: str, number: int) -> str:
        """Get interpretation for a specific number type and value."""
        interpretations = self.interpretations.get(number_type, {})
        return interpretations.get(number, f"Interpretation for {number_type} number {number} not available.")