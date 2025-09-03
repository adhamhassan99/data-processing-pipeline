"""Data models for the text processing pipeline."""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime


class ProcessingResult(BaseModel):
    """Result of processing text through the pipeline."""
    processed_text: str
    tokenized_text: List[str]
    steps_applied: List[str]
    steps_skipped: List[str]
    processing_time: float
    analysis: Dict[str, Any]
    errors: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)


class StepMetadata(BaseModel):
    """Metadata for a single step execution."""
    step_name: str
    execution_time: float
    success: bool
    error_message: Optional[str] = None
    parameters: Dict[str, Any]
