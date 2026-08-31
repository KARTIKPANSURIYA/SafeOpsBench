"""Deterministic engineering verifier foundation (not an ML contribution)."""

from enum import StrEnum
from typing import Any, Protocol

from pydantic import BaseModel

from safeopsbench.core.policies import Decision, authorize
from safeopsbench.tools.base import ToolMetadata


class VerifierDecision(StrEnum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REQUIRE_HUMAN_APPROVAL = "REQUIRE_HUMAN_APPROVAL"


class VerifierResult(BaseModel):
    decision: VerifierDecision
    reason: str


class Verifier(Protocol):
    def verify(
        self, tool: ToolMetadata, arguments: dict[str, Any], state: dict[str, Any], agent_role: str
    ) -> VerifierResult: ...


class DeterministicPolicyVerifier:
    def verify(
        self, tool: ToolMetadata, arguments: dict[str, Any], state: dict[str, Any], agent_role: str
    ) -> VerifierResult:
        decision = authorize(agent_role, tool.required_permission)
        return VerifierResult(
            decision=VerifierDecision.ALLOW
            if decision.decision is Decision.ALLOW
            else VerifierDecision.BLOCK,
            reason=decision.reason,
        )
