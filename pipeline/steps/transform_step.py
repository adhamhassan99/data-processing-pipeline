"""Text transformation step implementation."""

import re
import string
import spacy
from typing import Dict, Any
from ..core.base_step import BaseStep


class TransformStep(BaseStep):
    """Step for transforming text (case, punctuation, etc.)."""

    def __init__(self, params: Dict[str, Any]):
        """Initialize the transform step with spaCy model."""
        super().__init__(params)
        # Load spaCy model for tokenization
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback to basic English model if en_core_web_sm is not available
            try:
                self.nlp = spacy.load("en_core_web_lg")
            except OSError:
                # If no spaCy model is available, we'll handle it gracefully
                self.nlp = None

    def validate_params(self) -> None:
        """Validate transform step parameters."""
        required_params = ['remove_numbers',
                           'remove_special_chars', 'apply_stemming']
        for param in required_params:
            if param not in self.params:
                raise ValueError(f"Missing required parameter: {param}")

    def process(self, text: str) -> str:
        """Transform the input text according to parameters."""
        # Use spaCy tokenization if available, otherwise fall back to regex
        if self.nlp is not None:
            return self._apply_spacy_processing(text)
        else:
            return self._apply_regex_processing(text)

    def _apply_spacy_processing(self, text: str) -> str:
        """Apply spaCy-based tokenization for text transformation."""
        doc = self.nlp(text)
        processed_tokens = []

        for token in doc:
            # Skip if it's a number and we want to remove numbers
            if self.params['remove_numbers'] and token.like_num:
                continue

            # Skip if it's a special character and we want to remove special chars
            if self.params['remove_special_chars'] and not token.is_alpha and not token.is_space:
                continue

            # Apply stemming/lemmatization if requested
            if self.params['apply_stemming'] and token.is_alpha:
                # Use spaCy's lemmatization (more sophisticated than stemming)
                processed_tokens.append(token.lemma_.lower())
            else:
                # Keep the original token
                processed_tokens.append(token.text)

        # Join tokens back into text
        result = ' '.join(processed_tokens)

        return result

    def _apply_regex_processing(self, text: str) -> str:
        """Fallback regex-based processing when spaCy is not available."""
        result = text

        if self.params['remove_numbers']:
            result = re.sub(r'\d+', '', result)

        if self.params['remove_special_chars']:
            # Remove non-alphanumeric characters (except spaces)
            result = re.sub(r'[^a-zA-Z0-9\s]', '', result)

        if self.params['apply_stemming']:
            result = self._simple_stemming(result)

        return result

    def _simple_stemming(self, text: str) -> str:
        """Simple stemming implementation for fallback when spaCy is not available."""
        # Basic Porter-like stemming rules
        words = text.split()
        stemmed_words = []

        for word in words:
            word_lower = word.lower()

            # Simple stemming rules
            if word_lower.endswith('ing') and len(word_lower) > 5:
                word_lower = word_lower[:-3]
            elif word_lower.endswith('ed') and len(word_lower) > 4:
                word_lower = word_lower[:-2]
            elif word_lower.endswith('ly') and len(word_lower) > 4:
                word_lower = word_lower[:-2]
            elif word_lower.endswith('er') and len(word_lower) > 4:
                word_lower = word_lower[:-2]
            elif word_lower.endswith('est') and len(word_lower) > 5:
                word_lower = word_lower[:-3]
            elif word_lower.endswith('s') and len(word_lower) > 3 and not word_lower.endswith('ss'):
                word_lower = word_lower[:-1]

            stemmed_words.append(word_lower)

        return ' '.join(stemmed_words)
