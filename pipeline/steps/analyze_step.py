"""Text analysis step implementation."""

import re
from typing import Dict, Any
from ..core.base_step import BaseStep


class AnalyzeStep(BaseStep):
    """Step for analyzing text and generating statistics."""

    def validate_params(self) -> None:
        """Validate analyze step parameters."""
        required_params = [
            'count_words', 'count_characters', 'count_sentences',
            'count_paragraphs', 'average_word_length', 'reading_level'
        ]
        for param in required_params:
            if param not in self.params:
                raise ValueError(f"Missing required parameter: {param}")

    def process(self, text: str) -> str:
        """Analyze the text and return analysis results (text unchanged)."""
        # This step doesn't modify the text, just analyzes it
        # The analysis results are stored separately
        return text

    def analyze(self, text: str) -> Dict[str, Any]:
        """Perform text analysis and return statistics."""
        analysis = {}

        if self.params['count_characters']:
            analysis['character_count'] = len(text)
            analysis['character_count_no_spaces'] = len(text.replace(' ', ''))

        if self.params['count_words']:
            words = text.split()
            analysis['word_count'] = len(words)

            if self.params['average_word_length'] and words:
                total_length = sum(len(word) for word in words)
                analysis['average_word_length'] = round(
                    total_length / len(words), 2)

        if self.params['count_sentences']:
            # Simple sentence counting - split on sentence-ending punctuation
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            analysis['sentence_count'] = len(sentences)

        if self.params['count_paragraphs']:
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            analysis['paragraph_count'] = len(paragraphs)

        if self.params['reading_level'] and self.params['count_words'] and self.params['count_sentences']:
            # Simple Flesch Reading Ease approximation
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]

            if words and sentences:
                avg_sentence_length = len(words) / len(sentences)
                avg_syllables = sum(self._count_syllables(word)
                                    for word in words) / len(words)

                # Simplified Flesch Reading Ease formula
                flesch_score = 206.835 - \
                    (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
                analysis['reading_level'] = {
                    'flesch_score': round(flesch_score, 2),
                    'difficulty': self._get_difficulty_level(flesch_score)
                }

        return analysis

    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (approximation)."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False

        for char in word:
            if char in vowels:
                if not prev_was_vowel:
                    syllable_count += 1
                prev_was_vowel = True
            else:
                prev_was_vowel = False

        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1

        return max(1, syllable_count)

    def _get_difficulty_level(self, flesch_score: float) -> str:
        """Get difficulty level from Flesch score."""
        if flesch_score >= 90:
            return "Very Easy"
        elif flesch_score >= 80:
            return "Easy"
        elif flesch_score >= 70:
            return "Fairly Easy"
        elif flesch_score >= 60:
            return "Standard"
        elif flesch_score >= 50:
            return "Fairly Difficult"
        elif flesch_score >= 30:
            return "Difficult"
        else:
            return "Very Difficult"
