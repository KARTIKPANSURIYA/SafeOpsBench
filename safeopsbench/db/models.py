"""Persistent commerce and audit entities."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from safeopsbench.db.base import Base


def now() -> datetime:
    return datetime.now(UTC)


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str]
    role: Mapped[str]


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str]
    status: Mapped[str] = mapped_column(default="active")
    credit_limit: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    outstanding_balance: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    payment_terms: Mapped[str] = mapped_column(default="NET30")
    pricing_tier: Mapped[str] = mapped_column(default="B")
    tax_exempt: Mapped[bool] = mapped_column(Boolean, default=False)
    account_hold: Mapped[bool] = mapped_column(Boolean, default=False)
    assigned_sales_rep: Mapped[str]
    notes: Mapped[str] = mapped_column(Text, default="")
    notes_trust_level: Mapped[str] = mapped_column(default="UNTRUSTED_DATA")


class CustomerAddress(Base):
    __tablename__ = "customer_addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.customer_id"))
    line1: Mapped[str]
    city: Mapped[str]
    region: Mapped[str]
    postal_code: Mapped[str]


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)


class Warehouse(Base):
    __tablename__ = "warehouses"
    id: Mapped[int] = mapped_column(primary_key=True)
    warehouse_id: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str]


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (UniqueConstraint("sku", "warehouse_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(ForeignKey("products.sku"))
    warehouse_id: Mapped[str] = mapped_column(ForeignKey("warehouses.warehouse_id"))
    on_hand: Mapped[int]
    reserved: Mapped[int] = mapped_column(default=0)

    @property
    def available(self) -> int:
        return self.on_hand - self.reserved


class InventoryReservation(Base):
    __tablename__ = "inventory_reservations"
    id: Mapped[int] = mapped_column(primary_key=True)
    reservation_id: Mapped[str] = mapped_column(unique=True)
    order_id: Mapped[str]
    sku: Mapped[str]
    warehouse_id: Mapped[str]
    quantity: Mapped[int]
    active: Mapped[bool] = mapped_column(default=True)


class PriceList(Base):
    __tablename__ = "price_lists"
    id: Mapped[int] = mapped_column(primary_key=True)
    price_list_id: Mapped[str] = mapped_column(unique=True)
    tier: Mapped[str]


class PriceListItem(Base):
    __tablename__ = "price_list_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    price_list_id: Mapped[str]
    sku: Mapped[str]
    unit_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))


class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[str] = mapped_column(unique=True)
    customer_id: Mapped[str]
    status: Mapped[str] = mapped_column(default="CREATED")
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)


class SalesOrderItem(Base):
    __tablename__ = "sales_order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[str] = mapped_column(ForeignKey("sales_orders.order_id"))
    sku: Mapped[str]
    quantity: Mapped[int]
    unit_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    line_total: Mapped[Decimal] = mapped_column(Numeric(14, 2))


class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[str] = mapped_column(unique=True)
    order_id: Mapped[str]
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    status: Mapped[str] = mapped_column(default="ACTIVE")


class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[int] = mapped_column(primary_key=True)
    approval_id: Mapped[str] = mapped_column(unique=True)
    type: Mapped[str]
    order_id: Mapped[str | None]
    requested_by: Mapped[str]
    required_role: Mapped[str]
    status: Mapped[str] = mapped_column(default="PENDING")
    reason: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Shipment(Base):
    __tablename__ = "shipments"
    id: Mapped[int] = mapped_column(primary_key=True)
    shipment_id: Mapped[str] = mapped_column(unique=True)
    order_id: Mapped[str]
    status: Mapped[str] = mapped_column(default="CREATED")


class Delivery(Base):
    __tablename__ = "deliveries"
    id: Mapped[int] = mapped_column(primary_key=True)
    delivery_id: Mapped[str] = mapped_column(unique=True)
    shipment_id: Mapped[str]
    scheduled_date: Mapped[str]
    status: Mapped[str] = mapped_column(default="SCHEDULED")


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    task_run_id: Mapped[str]
    agent_id: Mapped[str]
    user_id: Mapped[str | None]
    tool_name: Mapped[str]
    arguments: Mapped[dict[str, Any]] = mapped_column(JSON)
    result_summary: Mapped[str]
    success: Mapped[bool]
    state_changing: Mapped[bool]
    risk_level: Mapped[str]
    policy_decision: Mapped[str]
    policy_id: Mapped[str | None]
    attempted: Mapped[bool] = mapped_column(default=True)
    executed: Mapped[bool] = mapped_column(default=False)
    blocked: Mapped[bool] = mapped_column(default=False)
    state_changed: Mapped[bool] = mapped_column(default=False)
    unsafe_attempt: Mapped[bool] = mapped_column(default=False)
    realized_violation: Mapped[bool] = mapped_column(default=False)
    violation_ids: Mapped[list[str]] = mapped_column(JSON, default=list)


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"
    __table_args__ = (UniqueConstraint("operation", "idempotency_key"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    operation: Mapped[str]
    idempotency_key: Mapped[str]
    object_id: Mapped[str]
