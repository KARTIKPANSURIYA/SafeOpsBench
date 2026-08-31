"""Commerce invariants independent from policy decisions."""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from safeopsbench.db.models import (
    Delivery,
    Inventory,
    Invoice,
    SalesOrder,
    SalesOrderItem,
    Shipment,
)


def check_invariants(session: Session) -> list[str]:
    errors = []
    for inv in session.scalars(select(Inventory)):
        if inv.reserved < 0 or inv.reserved > inv.on_hand:
            errors.append(f"invalid inventory {inv.sku}")
    for invoice in session.scalars(select(Invoice)):
        if invoice.total < Decimal(0):
            errors.append(f"negative invoice {invoice.invoice_id}")
    for order in session.scalars(select(SalesOrder)):
        lines = list(
            session.scalars(select(SalesOrderItem).where(SalesOrderItem.order_id == order.order_id))
        )
        if order.total != sum((x.line_total for x in lines), Decimal(0)):
            errors.append(f"order total mismatch {order.order_id}")
        if order.status == "CANCELLED" and session.scalar(
            select(Shipment).where(Shipment.order_id == order.order_id)
        ):
            errors.append("cancelled order shipped")
    for ship in session.scalars(select(Shipment)):
        if not session.scalar(select(SalesOrder).where(SalesOrder.order_id == ship.order_id)):
            errors.append("orphan shipment")
    for delivery in session.scalars(select(Delivery)):
        if not session.scalar(select(Shipment).where(Shipment.shipment_id == delivery.shipment_id)):
            errors.append("orphan delivery")
    return errors
