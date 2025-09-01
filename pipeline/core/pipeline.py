"""Main text processing pipeline."""

import time
import logging
from typing import Union, List, Dict, Any

from rich.logging import RichHandler
from rich.console import Console
from rich.traceback import install

from ..exceptions import StepError, ConfigurationError
from ..models.config import PipelineConfig
from ..models.data import ProcessingResult
from .step_registry import StepRegistry
from .statistics import StatisticsCollector

# Setup rich logging
install()
console = Console()
rich_handler = RichHandler(console=console, show_time=True, show_path=True)
logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[rich_handler])
logger = logging.getLogger(__name__)


class TextPipeline:
    """Main text processing pipeline."""

    def __init__(self, config: Union[PipelineConfig, Dict[str, Any], List[str]]):
        """Initialize the pipeline with configuration."""
        if isinstance(config, list):
            # Handle the case where config is a list of step names
            self.config = PipelineConfig(steps=config)
        elif isinstance(config, dict):
            self.config = PipelineConfig(**config)
        else:
            self.config = config

        self.step_registry = StepRegistry()
        self.statistics = StatisticsCollector()
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate the pipeline configuration."""
        # Validate that all configured steps exist
        available_steps = self.step_registry.list_steps()
        for step in self.config.steps:
            if step not in available_steps:
                raise ConfigurationError(
                    f"Unknown step '{step}' in configuration. Available steps: {available_steps}")

    def _get_step_params(self, step_name: str) -> Dict[str, Any]:
        """Get parameters for a specific step."""
        # Get default parameters for the step
        default_params = self._get_default_params(step_name)

        # Override with user-provided parameters
        user_params = self.config.step_params.get(step_name, {})
        default_params.update(user_params)

        return default_params

    def _get_default_params(self, step_name: str) -> Dict[str, Any]:
        """Get default parameters for a step."""
        if step_name == 'clean':
            return {
                'remove_extra_spaces': True,
                'preserve_newlines': False,
                'trim_edges': True
            }
        elif step_name == 'transform':
            return {
                'to_lowercase': True,
                'remove_punctuation': True,
                'remove_numbers': False,
                'remove_special_chars': False
            }
        elif step_name == 'analyze':
            return {
                'count_words': True,
                'count_characters': True,
                'count_sentences': True,
                'count_paragraphs': True,
                'average_word_length': True,
                'reading_level': True
            }
        else:
            return {}

    def process(self, text: Union[str, List[str]]) -> Union[ProcessingResult, List[ProcessingResult]]:
        """Process text through the configured pipeline."""
        if isinstance(text, list):
            return [self._process_single(item) for item in text]
        else:
            return self._process_single(text)

    def _process_single(self, text: str) -> ProcessingResult:
        """Process a single text string through the pipeline."""
        logger.info(
            f"Starting text processing pipeline with {len(self.config.steps)} steps")

        start_time = time.time()
        self.statistics.reset()
        current_text = text
        analysis = {}

        try:
            for step_name in self.config.steps:
                logger.info(f"Executing step: {step_name}")

                try:
                    # Get step parameters
                    step_params = self._get_step_params(step_name)

                    # Create and execute step
                    step = self.step_registry.create_step(
                        step_name, step_params)
                    processed_text, execution_time = step.execute(current_text)

                    # Record successful execution
                    self.statistics.record_step_success(
                        step_name, execution_time, step_params)
                    current_text = processed_text

                    # If this is the analyze step, collect analysis results
                    if step_name == 'analyze' and hasattr(step, 'analyze'):
                        analysis = step.analyze(current_text)
                        self.statistics.record_analysis(analysis)

                    logger.info(f"Step '{step_name}' completed successfully")

                except StepError as e:
                    logger.error(f"Step '{step_name}' failed: {e.message}")
                    self.statistics.record_step_failure(
                        step_name, 0, e.message, {})

                    if self.config.error_handling == 'stop':
                        raise
                    # Continue with previous text output

                except Exception as e:
                    logger.error(
                        f"Unexpected error in step '{step_name}': {e}")
                    self.statistics.record_step_failure(
                        step_name, 0, str(e), {})

                    if self.config.error_handling == 'stop':
                        raise
                    # Continue with previous text output

        finally:
            processing_time = time.time() - start_time

        # Create and return result
        result = ProcessingResult(
            processed_text=current_text,
            steps_applied=self.statistics.steps_applied.copy(),
            steps_skipped=self.statistics.steps_skipped.copy(),
            processing_time=processing_time,
            analysis=analysis,
            errors=self.statistics.errors.copy()
        )

        logger.info(f"Pipeline completed. Applied {len(self.statistics.steps_applied)} steps, "
                    f"skipped {len(self.statistics.steps_skipped)} steps")

        return result

    def get_statistics(self) -> Dict[str, Any]:
        """Get current pipeline statistics."""
        return self.statistics.get_summary()
