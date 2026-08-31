"""Structured safety violations."""

from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ViolationCategory(StrEnum):
    POLICY = "POLICY"
    AUTHORIZATION = "AUTHORIZATION"
    INVARIANT = "INVARIANT"
    SECURITY = "SECURITY"
    STATE = "STATE"
    DUPLICATION = "DUPLICATION"
    RECOVERY = "RECOVERY"


class Violation(BaseModel):
    violation_id: str
    policy_id: str | None = None
    category: ViolationCategory
    severity: Severity
    description: str
    step_number: int
    tool_name: str | None = None
    entity_ids: list[str] = Field(default_factory=list)
    remediation: str | None = None
