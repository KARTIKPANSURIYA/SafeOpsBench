"""Canonical tool registry and metadata."""

from safeopsbench.tools.base import RiskLevel, ToolMetadata


def m(
    name: str,
    permission: str,
    read_only: bool = True,
    risk: RiskLevel = RiskLevel.LOW,
    idem: bool = False,
) -> ToolMetadata:
    return ToolMetadata(
        name=name,
        description=name.replace("_", " ").capitalize(),
        required_permission=permission,
        read_only=read_only,
        reversible=not read_only,
        risk_level=risk,
        supports_idempotency=idem,
    )


TOOL_REGISTRY = {
    x.name: x
    for x in [
        m("get_customer", "customer.read"),
        m("search_customer", "customer.read"),
        m("get_customer_balance", "customer.balance.read"),
        m("get_credit_limit", "customer.read"),
        m("get_customer_notes", "customer.read"),
        m("get_inventory", "inventory.read"),
        m("reserve_inventory", "inventory.reserve", False, RiskLevel.HIGH),
        m("release_inventory", "inventory.release", False, RiskLevel.MEDIUM),
        m("get_price", "pricing.read"),
        m("apply_discount", "pricing.read", False, RiskLevel.HIGH),
        m("create_sales_order", "order.create", False, RiskLevel.MEDIUM, True),
        m("get_sales_order", "order.read"),
        m("update_sales_order", "order.create", False, RiskLevel.MEDIUM),
        m("cancel_sales_order", "order.create", False, RiskLevel.HIGH),
        m("create_invoice", "invoice.create", False, RiskLevel.HIGH, True),
        m("void_invoice", "invoice.void", False, RiskLevel.HIGH),
        m("request_manager_approval", "approval.request", False, RiskLevel.MEDIUM),
        m("get_approval_status", "approval.request"),
        m("create_shipment", "shipment.create", False, RiskLevel.CRITICAL, True),
        m("schedule_delivery", "delivery.schedule", False, RiskLevel.CRITICAL),
        m("get_audit_history", "customer.read"),
    ]
}
