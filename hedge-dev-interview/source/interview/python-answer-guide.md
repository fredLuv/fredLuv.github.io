# Python Answer Guide

Do not read this before attempting the question bank. These are reference shapes,
not scripts to memorize. In a real interview, a smaller correct solution with clear
tests beats a sophisticated solution you cannot explain.

## P1 — Deduplicate while preserving order

```python
from collections.abc import Iterable, Iterator
from typing import Protocol

class Event(Protocol):
    event_id: str

def unique(events: Iterable[Event]) -> Iterator[Event]:
    seen: set[str] = set()
    for event in events:
        if event.event_id not in seen:
            seen.add(event.event_id)
            yield event
```

Average O(n) time and O(u) memory for `u` unique IDs. An unbounded stream requires
a retention policy, partition lifetime, durable dedupe store, or probabilistic
structure; otherwise memory is unbounded. Conflicting duplicates should not be
silently accepted when payload identity matters.

## P2 — Merge event streams

```python
from collections.abc import Iterable, Iterator
from heapq import merge
from typing import TypeVar

T = TypeVar("T")

def merge_sorted(
    streams: Iterable[Iterable[T]], *, key
) -> Iterator[T]:
    return merge(*streams, key=key)
```

Each input must already be sorted by the same total key. Cost is O(n log k) time
and O(k) heap state for k streams. State whether duplicate identities are yielded,
deduplicated, or rejected. A manual heap solution is useful if the interviewer
wants dynamic sources or custom gap handling.

## P3 — Rolling mean

```python
from collections import deque
from collections.abc import Iterable, Iterator

def rolling_mean(values: Iterable[float], window: int) -> Iterator[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    items: deque[float] = deque()
    total = 0.0
    for value in values:
        items.append(value)
        total += value
        if len(items) > window:
            total -= items.popleft()
        if len(items) == window:
            yield total / window
```

O(n) total time, O(window) memory. Define whether warm-up yields nothing, partial
means, or missing values. For long numerical runs, floating-point drift may justify
periodic recomputation or a numeric-library implementation.

## P4 — LRU cache

In Python, `collections.OrderedDict` provides O(1)-average lookup, delete, insert,
and move-to-end:

```python
from collections import OrderedDict

class LRU:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._items: OrderedDict[str, object] = OrderedDict()

    def get(self, key: str) -> object:
        value = self._items[key]
        self._items.move_to_end(key)
        return value

    def put(self, key: str, value: object) -> None:
        self._items[key] = value
        self._items.move_to_end(key)
        if len(self._items) > self._capacity:
            self._items.popitem(last=False)
```

Clarify missing-key behavior and thread safety. `functools.lru_cache` is preferable
for memoizing function calls; cache invalidation, staleness, and key explosion are
the production questions.

## P5 — Sliding-window rate limiter

Store a deque of accepted monotonic timestamps per key. On each request, discard
timestamps `<= now - window`, then accept only if count is below limit. Complexity
is amortized O(1) per timestamp because each enters/exits once. Protect each key's
check-and-append invariant, remove inactive keys, inject a monotonic clock for tests,
and state that a local limiter is not a global distributed limit.

## P6 — Positions from fills

Maintain `seen: dict[fill_id, canonical_payload]` and `positions: dict[symbol, int]`.
On duplicate ID with identical payload, do nothing. On the same ID with a different
payload, quarantine/raise because upstream identity is corrupted. Otherwise add
`side * quantity`. This is O(n) average time and O(unique fills + symbols) memory.

## P7 — Bounded async mapper

Two good shapes are a semaphore around each call or a fixed worker pool consuming
a bounded queue. A semaphore limits in-flight calls but creating one task per item
can still be unbounded; for a stream, use fixed workers and a bounded queue.

Preserve order by assigning an input index and storing results by index. With
`TaskGroup`, one unexpected failure cancels siblings. Explicitly choose fail-fast,
per-item result/error, or retry semantics. Always bound downstream concurrency and
apply an overall timeout/cancellation contract.

## P8 — Context-managed timer

```python
from contextlib import contextmanager
from time import perf_counter

@contextmanager
def observed(name: str, sink):
    started = perf_counter()
    outcome = "success"
    try:
        yield
    except BaseException:
        outcome = "failure"
        raise
    finally:
        sink.record(name=name, outcome=outcome,
                    seconds=perf_counter() - started)
```

The broad catch exists only to label and re-raise every exit while `finally`
guarantees recording. Production metrics must keep labels bounded.

## P9 — Top-k exposure

If all inputs fit and simplicity matters, sort descending by `(abs(exposure),
tie_breaker)` for O(n log n). For a stream with small k, `heapq.nlargest` is O(n log
k) time and O(k) memory. Reject non-positive k or define it to return empty. State
the deterministic tie-break and whether duplicate symbols are aggregated/rejected.

## P10 — Point-in-time lookup

For decision times and publication revisions sorted ascending, sweep both lists.
Advance the revision pointer while `published_at <= decision_at`, retaining the
latest eligible revision, then emit it for the decision. This is O(d + r). Partition
by instrument and include ingestion time when “known to our system” is the contract.

## What to say after code works

- Time and auxiliary space complexity.
- Which input assumptions the solution relies on.
- Normal, empty, boundary, invalid, duplicate, and ordering tests.
- What becomes unbounded on a production stream.
- Which requirement change would force a different design.
