"""Text transformation step implementation."""

import re
import string
from typing import Dict, Any
from ..core.base_step import BaseStep


class TransformStep(BaseStep):
    """Step for transforming text (case, punctuation, etc.)."""

    def validate_params(self) -> None:
        """Validate transform step parameters."""
        required_params = ['to_lowercase', 'remove_punctuation',
                           'remove_numbers', 'remove_special_chars']
        for param in required_params:
            if param not in self.params:
                raise ValueError(f"Missing required parameter: {param}")

    def process(self, text: str) -> str:
        """Transform the input text according to parameters."""
        result = text

        if self.params['to_lowercase']:
            result = result.lower()

        if self.params['remove_punctuation']:
            result = result.translate(
                str.maketrans('', '', string.punctuation))

        if self.params['remove_numbers']:
            result = re.sub(r'\d+', '', result)

        if self.params['remove_special_chars']:
            # Remove non-alphanumeric characters (except spaces)
            result = re.sub(r'[^a-zA-Z0-9\s]', '', result)

        return result
