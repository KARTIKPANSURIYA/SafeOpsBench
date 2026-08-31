"""Benchmark-specific exceptions."""
class SafeOpsBenchError(RuntimeError):
    """Base benchmark error."""
class ToolExecutionError(SafeOpsBenchError):
    """A safe, expected tool rejection."""
class TaskValidationError(SafeOpsBenchError):
    """A task specification is invalid."""
