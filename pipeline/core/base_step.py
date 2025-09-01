"""Base step class for text processing pipeline."""

import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

from ..exceptions import StepError

logger = logging.getLogger(__name__)


class BaseStep(ABC):
    """Abstract base class for all text processing steps."""

    def __init__(self, params: Dict[str, Any]):
        """Initialize the step with parameters."""
        self.params = params
        self.validate_params()

    @abstractmethod
    def validate_params(self) -> None:
        """Validate the step parameters. Should raise ValueError for invalid params."""
        pass

    @abstractmethod
    def process(self, text: str) -> str:
        """Process the input text and return processed text."""
        pass

    def execute(self, text: str) -> Tuple[str, float]:
        """Execute the step with timing and error handling."""
        start_time = time.time()

        try:
            logger.debug(f"Executing step {self.__class__.__name__}")
            result = self.process(text)
            execution_time = time.time() - start_time
            logger.debug(
                f"Step {self.__class__.__name__} completed in {execution_time:.4f}s")
            return result, execution_time

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Step {self.__class__.__name__} failed after {execution_time:.4f}s: {e}")
            raise StepError(self.__class__.__name__, str(e), e)
