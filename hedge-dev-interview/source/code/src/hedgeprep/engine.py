"""Deterministic event orchestration for the teaching backtester."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .events import Decision, Fill, MarketTick, Order, Side
from .risk import PositionLimitRisk, RiskRejected


class Strategy(Protocol):
    def on_tick(self, tick: MarketTick) -> int | None: ...


@dataclass(frozen=True, slots=True)
class Rejection:
    order: Order
    reason: str


@dataclass(frozen=True, slots=True)
class BacktestResult:
    decisions: tuple[Decision, ...]
    orders: tuple[Order, ...]
    fills: tuple[Fill, ...]
    rejections: tuple[Rejection, ...]
    final_position: int
    final_cash: float


class BacktestEngine:
    def __init__(self, strategy: Strategy, risk: PositionLimitRisk) -> None:
        self._strategy = strategy
        self._risk = risk

    def run(self, ticks: list[MarketTick]) -> BacktestResult:
        ordered = sorted(ticks, key=lambda tick: tick.sort_key)
        symbols = {tick.symbol for tick in ordered}
        if len(symbols) > 1:
            raise ValueError("teaching engine supports one symbol per run")
        if len({tick.sort_key for tick in ordered}) != len(ordered):
            raise ValueError("duplicate tick identity")

        decisions: list[Decision] = []
        orders: list[Order] = []
        fills: list[Fill] = []
        rejections: list[Rejection] = []
        position = 0
        cash = 0.0

        for tick in ordered:
            target = self._strategy.on_tick(tick)
            if target is None or target == position:
                continue

            decisions.append(
                Decision(tick.timestamp_ns, tick.symbol, target, tick.price)
            )
            difference = target - position
            side = Side.BUY if difference > 0 else Side.SELL
            order = Order(
                order_id=f"ORD-{len(orders) + len(rejections) + 1:06d}",
                timestamp_ns=tick.timestamp_ns,
                symbol=tick.symbol,
                side=side,
                quantity=abs(difference),
            )

            try:
                self._risk.check(order, position)
            except RiskRejected as exc:
                rejections.append(Rejection(order, str(exc)))
                continue

            fill = Fill(
                fill_id=f"FILL-{len(fills) + 1:06d}",
                order_id=order.order_id,
                timestamp_ns=tick.timestamp_ns,
                symbol=tick.symbol,
                side=order.side,
                quantity=order.quantity,
                price=tick.price,
            )
            orders.append(order)
            fills.append(fill)
            position += fill.signed_quantity
            cash += fill.cash_change

        return BacktestResult(
            decisions=tuple(decisions),
            orders=tuple(orders),
            fills=tuple(fills),
            rejections=tuple(rejections),
            final_position=position,
            final_cash=cash,
        )
