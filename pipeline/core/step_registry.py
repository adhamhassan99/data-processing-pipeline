"""Step registry for managing available processing steps."""

from typing import Dict, Type, List
from .base_step import BaseStep


class StepRegistry:
    """Registry for managing available text processing steps."""

    def __init__(self):
        """Initialize the step registry."""
        self._steps: Dict[str, Type[BaseStep]] = {}
        self._register_default_steps()

    def _register_default_steps(self) -> None:
        """Register the default processing steps."""
        # Import here to avoid circular imports
        from ..steps.clean_step import CleanStep
        from ..steps.transform_step import TransformStep
        from ..steps.analyze_step import AnalyzeStep

        self.register_step('clean', CleanStep)
        self.register_step('transform', TransformStep)
        self.register_step('analyze', AnalyzeStep)

    def register_step(self, name: str, step_class: Type[BaseStep]) -> None:
        """Register a new step class."""
        if not issubclass(step_class, BaseStep):
            raise ValueError(
                f"Step class {step_class} must inherit from BaseStep")

        self._steps[name] = step_class

    def get_step_class(self, name: str) -> Type[BaseStep]:
        """Get a step class by name."""
        if name not in self._steps:
            raise ValueError(
                f"Unknown step '{name}'. Available steps: {list(self._steps.keys())}")

        return self._steps[name]

    def list_steps(self) -> List[str]:
        """List all available step names."""
        return list(self._steps.keys())

    def create_step(self, name: str, params: Dict) -> BaseStep:
        """Create a step instance with the given parameters."""
        step_class = self.get_step_class(name)
        return step_class(params)
