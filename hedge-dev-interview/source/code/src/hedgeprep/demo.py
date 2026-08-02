"""Run a reproducible example from the command line."""

from __future__ import annotations

from .engine import BacktestEngine
from .events import MarketTick
from .risk import PositionLimitRisk
from .strategy import MovingAverageStrategy


def main() -> int:
    prices = [100.0, 101.0, 102.0, 99.0, 98.0, 101.0]
    ticks = [
        MarketTick(timestamp_ns=i, sequence=i, symbol="XYZ", price=price)
        for i, price in enumerate(prices, start=1)
    ]
    engine = BacktestEngine(
        MovingAverageStrategy(window=3, lot=10, threshold=0.005),
        PositionLimitRisk(max_absolute_position=10, max_order_quantity=20),
    )
    result = engine.run(ticks)
    print(
        f"orders={len(result.orders)} fills={len(result.fills)} "
        f"position={result.final_position} cash={result.final_cash:.2f}"
    )
    for fill in result.fills:
        print(fill)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
