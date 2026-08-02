"""Immutable domain events used by both simulation and tests."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from math import isfinite


class Side(IntEnum):
    """Signed side makes position and cash arithmetic explicit."""

    SELL = -1
    BUY = 1


@dataclass(frozen=True, slots=True)
class MarketTick:
    timestamp_ns: int
    sequence: int
    symbol: str
    price: float

    def __post_init__(self) -> None:
        if self.timestamp_ns < 0 or self.sequence < 0:
            raise ValueError("timestamp and sequence must be non-negative")
        if not self.symbol:
            raise ValueError("symbol must not be empty")
        if not isfinite(self.price) or self.price <= 0:
            raise ValueError("price must be finite and positive")

    @property
    def sort_key(self) -> tuple[int, str, int]:
        return self.timestamp_ns, self.symbol, self.sequence


@dataclass(frozen=True, slots=True)
class Order:
    order_id: str
    timestamp_ns: int
    symbol: str
    side: Side
    quantity: int

    def __post_init__(self) -> None:
        if not self.order_id or not self.symbol:
            raise ValueError("order_id and symbol must not be empty")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")

    @property
    def signed_quantity(self) -> int:
        return int(self.side) * self.quantity


@dataclass(frozen=True, slots=True)
class Fill:
    fill_id: str
    order_id: str
    timestamp_ns: int
    symbol: str
    side: Side
    quantity: int
    price: float

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("fill quantity must be positive")
        if not isfinite(self.price) or self.price <= 0:
            raise ValueError("fill price must be finite and positive")

    @property
    def signed_quantity(self) -> int:
        return int(self.side) * self.quantity

    @property
    def cash_change(self) -> float:
        return -self.signed_quantity * self.price


@dataclass(frozen=True, slots=True)
class Decision:
    timestamp_ns: int
    symbol: str
    target_position: int
    reference_price: float
