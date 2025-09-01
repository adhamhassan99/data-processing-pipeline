"""Text cleaning step implementation."""

import re
from typing import Dict, Any
from ..core.base_step import BaseStep


class CleanStep(BaseStep):
    """Step for cleaning and normalizing text."""

    def validate_params(self) -> None:
        """Validate clean step parameters."""
        required_params = ['remove_extra_spaces',
                           'preserve_newlines', 'trim_edges']
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

        return result
