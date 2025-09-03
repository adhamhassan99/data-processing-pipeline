"""Text cleaning step implementation."""
import spacy
import re
from typing import Dict, Any
from ..core.base_step import BaseStep


class CleanStep(BaseStep):
    """Step for cleaning and normalizing text."""

    def __init__(self, params: Dict[str, Any]):
        """Initialize the clean step with spaCy model."""
        super().__init__(params)
        # Load spaCy model for punctuation and stop word removal
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
        """Validate clean step parameters."""
        required_params = ['remove_extra_spaces',
                           'preserve_newlines',
                           'trim_edges',
                           'lowercase',
                           'remove_punctuation',
                           'remove_stopwords']
        for param in required_params:
            if param not in self.params:
                raise ValueError(f"Missing required parameter: {param}")

    def process(self, text: str) -> str:
        """Clean the input text according to parameters."""
        result = text

        if self.params['trim_edges']:
            result = result.strip()

        if self.params['remove_extra_spaces']:
            if self.params['preserve_newlines']:
                # Replace multiple spaces with single space, preserve newlines
                result = re.sub(r'[ \t]+', ' ', result)
                result = re.sub(r'\n[ \t]*\n', '\n\n', result)
            else:
                # Replace all whitespace sequences with single space
                result = re.sub(r'\s+', ' ', result)

        # Apply spaCy-based processing if model is available
        if self.nlp is not None:
            result = self._apply_spacy_processing(result)

        return result

    def _apply_spacy_processing(self, text: str) -> str:
        """Apply spaCy-based text processing for punctuation and stop words."""
        doc = self.nlp(text)
        processed_tokens = []

        for token in doc:
            # Skip if it's a stop word and we want to remove stop words
            if self.params['remove_stopwords'] and token.is_stop:
                continue

            # Skip if it's punctuation and we want to remove punctuation
            if self.params['remove_punctuation'] and token.is_punct:
                continue

            # Apply lowercase if requested
            if self.params['lowercase']:
                processed_tokens.append(token.text.lower())
            else:
                processed_tokens.append(token.text)

                # Join tokens back into text
        result = ' '.join(processed_tokens)

        return result
