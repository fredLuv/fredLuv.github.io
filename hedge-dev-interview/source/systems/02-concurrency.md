# 7. Threads, Processes, and Asyncio

## Interview outcome

Choose a concurrency model from workload and failure boundaries, explain the GIL
accurately, and design cancellation and backpressure rather than only a happy path.

## Decision table

| Workload | First candidate | Why | Main costs |
|---|---|---|---|
| many network/file waits | `asyncio` | many tasks on few threads | cooperative blocking, cancellation complexity |
| blocking I/O libraries | threads | simple integration | shared-state races, thread/stack overhead |
| Python CPU-bound work | processes | separate interpreters/cores | serialization, startup, memory, failure handling |
| native numeric kernel | library/thread model | native code may release GIL | oversubscription, data copies |
| ultra-low-latency hot path | native/compiled component | tighter control and predictable memory | engineering/operational complexity |

Concurrency overlaps work. Parallelism executes work simultaneously. Async is not
automatically parallel and not automatically faster.

## Threads and invariants

A lock protects an invariant, not a line of code. Define what must change together.

```python
from threading import Lock

class Position:
    def __init__(self) -> None:
        self._quantity = 0
        self._version = 0
        self._lock = Lock()

    def apply_fill(self, signed_quantity: int) -> tuple[int, int]:
        with self._lock:
            self._quantity += signed_quantity
            self._version += 1
            return self._quantity, self._version
```

Minimize shared mutable state. Passing immutable messages through bounded queues
is often easier to reason about. Avoid holding a lock across network I/O.

## Processes

Processes provide isolation and true CPU parallelism for Python code, but inputs
and outputs cross a serialization boundary. Large arrays may need shared memory or
partitioning. Initialize workers deliberately, bound task sizes, propagate errors,
and avoid forking a process that already owns threads/network connections.

## Asyncio mental model

An event loop runs one task until it awaits something not ready, then runs another.
Calling blocking code inside an async task blocks every task on that loop.

```python
import asyncio

async def enrich(symbol: str) -> tuple[str, float]:
    async with asyncio.timeout(0.5):
        price = await fetch_price(symbol)
    return symbol, price

async def main(symbols: list[str]) -> list[tuple[str, float]]:
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(enrich(s)) for s in symbols]
    return [task.result() for task in tasks]
```

Structured task ownership makes failure and cleanup visible. Cancellation is a
request delivered at an await point. Use `try/finally` or async context managers
for cleanup, and do not casually swallow cancellation.

## Backpressure is part of correctness

An unbounded queue converts overload into delayed failure and stale decisions.

```python
queue: asyncio.Queue[Tick] = asyncio.Queue(maxsize=1_000)
await queue.put(tick)  # producer waits when full: explicit backpressure
```

Waiting is only one policy. Depending on semantics you may coalesce updates by
symbol, drop old derived snapshots, spill to durable storage, reject new work, or
fail closed. Never silently drop orders or fills.

## Common failures

- task created and forgotten; exceptions become orphaned;
- blocking database/client call on the event loop;
- no timeout or total deadline;
- unbounded fan-out with `gather`;
- cancellation leaves a partial side effect;
- thread pool larger than a downstream service can handle;
- process-pool serialization costs more than computation;
- multiple layers retry and create a retry storm.

## Drill

For each case, pick a model and defend it:

1. 5,000 mostly idle WebSocket market-data connections.
2. CPU-heavy pure-Python calibration across 32 independent parameter sets.
3. Batch NumPy calculation whose kernels release the GIL.
4. One blocking vendor SDK used by an async service.

Expected first answers: asyncio; bounded process pool; benchmark library threads
and avoid oversubscription; bounded thread executor or isolate behind an adapter.

## Answer frame

> I choose concurrency from the wait/compute profile and ownership boundary.
> Threads integrate blocking I/O, processes parallelize isolated Python CPU work,
> and asyncio multiplexes cooperative I/O. In every model I make task ownership,
> queue bounds, timeouts, cancellation, and overload behavior explicit.
