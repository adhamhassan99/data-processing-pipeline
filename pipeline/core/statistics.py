"""Statistics collection for the text processing pipeline."""

from typing import List, Dict, Any
from ..models.data import StepMetadata


class StatisticsCollector:
    """Collects and manages processing statistics."""

    def __init__(self):
        """Initialize the statistics collector."""
        self.steps_applied: List[str] = []
        self.steps_skipped: List[str] = []
        self.errors: List[str] = []
        self.step_metadata: List[StepMetadata] = []
        self.analysis_results: Dict[str, Any] = {}

    def record_step_success(self, step_name: str, execution_time: float, parameters: Dict[str, Any]) -> None:
        """Record a successful step execution."""
        self.steps_applied.append(step_name)
        metadata = StepMetadata(
            step_name=step_name,
            execution_time=execution_time,
            success=True,
            parameters=parameters
        )
        self.step_metadata.append(metadata)

    def record_step_failure(self, step_name: str, execution_time: float, error_message: str, parameters: Dict[str, Any]) -> None:
        """Record a failed step execution."""
        self.steps_skipped.append(step_name)
        self.errors.append(f"{step_name}: {error_message}")
        metadata = StepMetadata(
            step_name=step_name,
            execution_time=execution_time,
            success=False,
            error_message=error_message,
            parameters=parameters
        )
        self.step_metadata.append(metadata)

    def record_analysis(self, analysis_results: Dict[str, Any]) -> None:
        """Record analysis results."""
        self.analysis_results.update(analysis_results)

    def reset(self) -> None:
        """Reset all statistics."""
        self.steps_applied.clear()
        self.steps_skipped.clear()
        self.errors.clear()
        self.step_metadata.clear()
        self.analysis_results.clear()

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all statistics."""
        total_execution_time = sum(
            meta.execution_time for meta in self.step_metadata)

        return {
            'steps_applied': self.steps_applied.copy(),
            'steps_skipped': self.steps_skipped.copy(),
            'errors': self.errors.copy(),
            'total_execution_time': total_execution_time,
            'step_count': len(self.step_metadata),
            'success_rate': len(self.steps_applied) / max(len(self.step_metadata), 1),
            'analysis_results': self.analysis_results.copy()
        }
