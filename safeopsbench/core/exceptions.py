"""Benchmark-specific exceptions."""

from safeopsbench.core.policies import PolicyDecision


class SafeOpsBenchError(RuntimeError):
    """Base benchmark error."""


class ToolExecutionError(SafeOpsBenchError):
    """A safe, expected tool rejection."""


class TaskValidationError(SafeOpsBenchError):
    """A task specification is invalid."""


class PolicyBlocked(ToolExecutionError):
    """An authoritative policy prevented a tool effect."""

    def __init__(self, decision: PolicyDecision) -> None:
        super().__init__(decision.reason)
        self.decision = decision
