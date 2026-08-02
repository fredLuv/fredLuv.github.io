from __future__ import annotations

import math
import unittest

from hedgeprep.engine import BacktestEngine
from hedgeprep.events import MarketTick, Order, Side
from hedgeprep.risk import PositionLimitRisk, RiskRejected
from hedgeprep.strategy import MovingAverageStrategy


def ticks(prices: list[float]) -> list[MarketTick]:
    return [
        MarketTick(timestamp_ns=i, sequence=i, symbol="XYZ", price=price)
        for i, price in enumerate(prices, start=1)
    ]


class EngineTests(unittest.TestCase):
    def make_engine(self) -> BacktestEngine:
        return BacktestEngine(
            MovingAverageStrategy(window=3, lot=10, threshold=0.0),
            PositionLimitRisk(max_absolute_position=10, max_order_quantity=20),
        )

    def test_replay_is_deterministic(self) -> None:
        data = ticks([100.0, 101.0, 102.0, 99.0, 98.0, 101.0])
        forward = self.make_engine().run(data)
        reversed_input = self.make_engine().run(list(reversed(data)))
        self.assertEqual(forward, reversed_input)
        self.assertEqual(forward.final_position, -10)
        self.assertTrue(forward.fills)

    def test_duplicate_tick_identity_is_rejected(self) -> None:
        tick = MarketTick(1, 1, "XYZ", 100.0)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.make_engine().run([tick, tick])

    def test_multi_symbol_scope_is_rejected_explicitly(self) -> None:
        data = [MarketTick(1, 1, "XYZ", 100.0), MarketTick(2, 1, "ABC", 50.0)]
        with self.assertRaisesRegex(ValueError, "one symbol"):
            self.make_engine().run(data)

    def test_risk_uses_projected_position_and_order_limit(self) -> None:
        risk = PositionLimitRisk(max_absolute_position=10, max_order_quantity=5)
        too_large = Order("O1", 1, "XYZ", Side.BUY, 6)
        with self.assertRaises(RiskRejected):
            risk.check(too_large, current_position=0)

        breaches_position = Order("O2", 1, "XYZ", Side.BUY, 5)
        with self.assertRaises(RiskRejected):
            risk.check(breaches_position, current_position=8)

    def test_strategy_warms_up_and_tracks_rolling_sum(self) -> None:
        strategy = MovingAverageStrategy(window=3, lot=5)
        outputs = [strategy.on_tick(tick) for tick in ticks([1.0, 2.0, 3.0, 1.0])]
        self.assertEqual(outputs, [None, None, -5, 5])

    def test_strategy_rejects_non_finite_threshold(self) -> None:
        with self.assertRaises(ValueError):
            MovingAverageStrategy(window=3, lot=5, threshold=math.nan)


if __name__ == "__main__":
    unittest.main()
