"""Stable trajectory representation with action-attempt semantics."""

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class StepType(StrEnum):
    """Kinds of reconstructable trajectory evidence."""

    AGENT_MESSAGE = "AGENT_MESSAGE"
    TOOL_CALL = "TOOL_CALL"
    TOOL_RESULT = "TOOL_RESULT"
    ENVIRONMENT_EVENT = "ENVIRONMENT_EVENT"
    POLICY_DECISION = "POLICY_DECISION"
    ACTION_OUTCOME = "ACTION_OUTCOME"
    VIOLATION = "VIOLATION"
    SYSTEM_EVENT = "SYSTEM_EVENT"


class ActionOutcome(BaseModel):
    """Attempt-versus-effect evidence for one tool invocation."""

    attempted: bool = True
    consequential: bool
    unsafe_attempt: bool
    executed: bool
    blocked: bool
    state_changed: bool
    policy_id: str | None = None
    policy_decision: str
    reason: str | None = None
    realized_policy_violation: bool = False
    realized_unauthorized_effect: bool = False


class TrajectoryStep(BaseModel):
    """One versioned trajectory record."""

    step_number: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    type: StepType
    tool_name: str | None = None
    input: dict[str, Any] | None = None
    output: dict[str, Any] | None = None
    action_outcome: ActionOutcome | None = None
    state_hash: str | None = None
    latency_ms: float | None = None
    cost: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None


class Trajectory(BaseModel):
    """Complete evidence stream for one task run."""

    schema_version: str = "0.2"
    task_run_id: str
    steps: list[TrajectoryStep] = Field(default_factory=list)

    def add(self, kind: StepType, **values: Any) -> TrajectoryStep:
        step = TrajectoryStep(step_number=len(self.steps) + 1, type=kind, **values)
        self.steps.append(step)
        return step
