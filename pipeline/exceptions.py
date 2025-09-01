"""Custom exceptions for the text processing pipeline."""


class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass


class StepError(PipelineError):
    """Exception raised when a step fails."""

    def __init__(self, step_name: str, message: str, original_error: Exception = None):
        self.step_name = step_name
        self.message = message
        self.original_error = original_error
        super().__init__(f"Step '{step_name}' failed: {message}")


class ConfigurationError(PipelineError):
    """Exception raised for configuration errors."""
    pass


class ValidationError(PipelineError):
    """Exception raised for validation errors."""
    pass
