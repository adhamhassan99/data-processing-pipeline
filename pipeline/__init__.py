"""Text Processing Pipeline - A configurable text processing system."""

from .core.pipeline import TextPipeline
from .models.config import PipelineConfig
from .models.data import ProcessingResult

__version__ = "1.0.0"
__all__ = ["TextPipeline", "PipelineConfig", "ProcessingResult"]
