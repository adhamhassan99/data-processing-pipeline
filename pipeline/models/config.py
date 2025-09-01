"""Configuration models for the text processing pipeline."""

from pydantic import BaseModel, Field
from typing import List, Dict, Literal, Any


class CleanStepConfig(BaseModel):
    """Configuration for the clean step."""
    remove_extra_spaces: bool = True
    preserve_newlines: bool = False
    trim_edges: bool = True


class TransformStepConfig(BaseModel):
    """Configuration for the transform step."""
    to_lowercase: bool = True
    remove_punctuation: bool = True
    remove_numbers: bool = False
    remove_special_chars: bool = False


class AnalyzeStepConfig(BaseModel):
    """Configuration for the analyze step."""
    count_words: bool = True
    count_characters: bool = True
    count_sentences: bool = True
    count_paragraphs: bool = True
    average_word_length: bool = True
    reading_level: bool = True


class PipelineConfig(BaseModel):
    """Main pipeline configuration."""
    steps: List[str] = Field(default=['clean', 'transform', 'analyze'])
    error_handling: Literal['continue', 'stop'] = 'continue'
    logging_level: str = 'INFO'
    step_params: Dict[str, Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        extra = "forbid"  # Don't allow extra fields
