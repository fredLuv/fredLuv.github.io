from __future__ import annotations

import asyncio
import unittest

from hedgeprep.async_pipeline import run_pipeline
from hedgeprep.events import MarketTick


class PipelineTests(unittest.TestCase):
    def test_pipeline_processes_in_order_and_stays_bounded(self) -> None:
        data = [MarketTick(i, i, "XYZ", 100.0 + i) for i in range(12)]
        result = asyncio.run(run_pipeline(data, capacity=2, consumer_delay=0.0001))
        self.assertEqual(result.processed, len(data))
        self.assertEqual(result.last_sequence, data[-1].sequence)
        self.assertLessEqual(result.maximum_queue_depth, 2)
        self.assertGreater(result.maximum_queue_depth, 0)


if __name__ == "__main__":
    unittest.main()
