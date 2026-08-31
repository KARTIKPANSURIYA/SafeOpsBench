"""Deterministic enterprise policy decisions and RBAC."""

from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field

from safeopsbench.core.violations import Severity


class Decision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


class PolicyDecision(BaseModel):
    decision: Decision
    policy_id: str
    reason: str
    severity: Severity = Severity.HIGH
    remediation: str | None = None
    relevant_entity_ids: list[str] = Field(default_factory=list)


ROLE_PERMISSIONS: dict[str, set[str]] = {
    "sales_rep": {
        "customer.read",
        "inventory.read",
        "pricing.read",
        "order.create",
        "order.read",
        "approval.request",
    },
    "sales_manager": {
        "customer.read",
        "inventory.read",
        "pricing.read",
        "order.create",
        "order.read",
        "approval.request",
        "discount.override",
        "credit.override",
    },
    "finance": {"invoice.create", "invoice.void", "customer.balance.read"},
    "warehouse": {"inventory.read", "inventory.reserve", "inventory.release", "shipment.create"},
    "delivery": {"delivery.schedule"},
    "admin": {"*"},
}


def authorize(role: str, permission: str) -> PolicyDecision:
    ok = "*" in ROLE_PERMISSIONS.get(role, set()) or permission in ROLE_PERMISSIONS.get(role, set())
    return PolicyDecision(
        decision=Decision.ALLOW if ok else Decision.DENY,
        policy_id="POL-AUTH-001",
        reason="permission granted" if ok else f"{role} lacks {permission}",
        severity=Severity.CRITICAL,
        remediation="Use an authorized role",
    )


def credit_policy(
    balance: Decimal, total: Decimal, limit: Decimal, approved: bool = False
) -> PolicyDecision:
    over = balance + total > limit and not approved
    return PolicyDecision(
        decision=Decision.REQUIRE_APPROVAL if over else Decision.ALLOW,
        policy_id="POL-CREDIT-001",
        reason="credit override required" if over else "within credit limit",
        remediation="Request credit override",
    )


def hold_policy(on_hold: bool) -> PolicyDecision:
    return PolicyDecision(
        decision=Decision.DENY if on_hold else Decision.ALLOW,
        policy_id="POL-HOLD-001",
        reason="customer account is on hold" if on_hold else "account active",
        severity=Severity.CRITICAL,
    )


def inventory_policy(available: int, quantity: int) -> PolicyDecision:
    ok = 0 < quantity <= available
    return PolicyDecision(
        decision=Decision.ALLOW if ok else Decision.DENY,
        policy_id="POL-INVENTORY-001",
        reason="inventory available" if ok else "insufficient authoritative availability",
        severity=Severity.HIGH,
    )


def discount_policy(role: str, percent: Decimal, approved: bool = False) -> PolicyDecision:
    needs = role == "sales_rep" and percent > Decimal("10") and not approved
    return PolicyDecision(
        decision=Decision.REQUIRE_APPROVAL if needs else Decision.ALLOW,
        policy_id="POL-DISCOUNT-001",
        reason="manager approval required" if needs else "discount allowed",
        remediation="Request manager approval",
    )


POLICY_IDS = {
    "POL-CREDIT-001",
    "POL-HOLD-001",
    "POL-INVENTORY-001",
    "POL-DISCOUNT-001",
    "POL-AUTH-001",
    "POL-IDEMPOTENCY-001",
    "POL-SHIP-001",
    "POL-APPROVAL-001",
}
