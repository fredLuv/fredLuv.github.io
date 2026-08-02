"""A stateful but deterministic rolling mean-reversion example."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from math import isfinite

from .events import MarketTick


@dataclass(slots=True)
class MovingAverageStrategy:
    window: int
    lot: int
    threshold: float = 0.0
    _prices: deque[float] = field(init=False, repr=False)
    _sum: float = field(init=False, default=0.0, repr=False)

    def __post_init__(self) -> None:
        if (
            self.window <= 1
            or self.lot <= 0
            or not isfinite(self.threshold)
            or self.threshold < 0
        ):
            raise ValueError("window > 1, lot > 0, and threshold >= 0 required")
        self._prices = deque(maxlen=self.window)

    def on_tick(self, tick: MarketTick) -> int | None:
        """Return target position, or None while the rolling window warms up."""
        if len(self._prices) == self.window:
            self._sum -= self._prices[0]
        self._prices.append(tick.price)
        self._sum += tick.price

        if len(self._prices) < self.window:
            return None

        mean = self._sum / self.window
        if tick.price > mean * (1.0 + self.threshold):
            return -self.lot
        if tick.price < mean * (1.0 - self.threshold):
            return self.lot
        return 0
