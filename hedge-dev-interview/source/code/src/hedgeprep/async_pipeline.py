"""Bounded producer/consumer example with measured queue saturation."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

from .events import MarketTick


@dataclass(frozen=True, slots=True)
class PipelineResult:
    processed: int
    maximum_queue_depth: int
    last_sequence: int


async def run_pipeline(
    ticks: list[MarketTick], *, capacity: int = 3, consumer_delay: float = 0.001
) -> PipelineResult:
    if capacity <= 0 or consumer_delay < 0:
        raise ValueError("capacity must be positive and delay non-negative")

    queue: asyncio.Queue[MarketTick | None] = asyncio.Queue(maxsize=capacity)
    maximum_depth = 0

    async def produce() -> None:
        nonlocal maximum_depth
        for tick in ticks:
            await queue.put(tick)
            maximum_depth = max(maximum_depth, queue.qsize())
        await queue.put(None)

    async def consume() -> tuple[int, int]:
        processed = 0
        last_sequence = -1
        while True:
            tick = await queue.get()
            try:
                if tick is None:
                    return processed, last_sequence
                await asyncio.sleep(consumer_delay)
                processed += 1
                last_sequence = tick.sequence
            finally:
                queue.task_done()

    async with asyncio.TaskGroup() as group:
        producer = group.create_task(produce())
        consumer = group.create_task(consume())

    producer.result()
    processed, last_sequence = consumer.result()
    return PipelineResult(processed, maximum_depth, last_sequence)


async def _main() -> None:
    ticks = [MarketTick(i, i, "XYZ", 100.0 + i) for i in range(20)]
    result = await run_pipeline(ticks)
    print(result)


if __name__ == "__main__":
    asyncio.run(_main())
