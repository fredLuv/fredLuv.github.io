"""Pre-trade policies independent from strategy and execution adapters."""

from __future__ import annotations

from dataclasses import dataclass

from .events import Order


class RiskRejected(ValueError):
    """Raised when an order violates a declared risk contract."""


@dataclass(frozen=True, slots=True)
class PositionLimitRisk:
    max_absolute_position: int
    max_order_quantity: int

    def __post_init__(self) -> None:
        if self.max_absolute_position <= 0 or self.max_order_quantity <= 0:
            raise ValueError("risk limits must be positive")

    def check(self, order: Order, current_position: int) -> None:
        if order.quantity > self.max_order_quantity:
            raise RiskRejected(
                f"quantity {order.quantity} exceeds {self.max_order_quantity}"
            )
        projected = current_position + order.signed_quantity
        if abs(projected) > self.max_absolute_position:
            raise RiskRejected(
                f"projected position {projected} exceeds "
                f"+/-{self.max_absolute_position}"
            )
