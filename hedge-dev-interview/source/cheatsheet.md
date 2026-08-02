# Last-Hour Cheatsheet

## Python

- Names bind to objects. Assignment rebinds; mutation changes the object.
- Parameters use call by sharing. Rebinding is local; mutation may be visible.
- `is` is identity; `==` is value equality. Use `is None`.
- Equal objects must have equal hashes; stored-key hash must remain stable.
- Mutable defaults are created once. Use `None`/sentinel and allocate inside.
- Shallow copy duplicates only the outer container.
- Iterable produces iterator; iterator carries state; generator suspends at `yield`.
- Generator benefits: lazy, O(1) auxiliary memory. Costs: one-shot, deferred work/errors.
- Decorator replaces a callable; preserve metadata/signature and return/exception.
- Context manager makes enter/cleanup or commit/rollback a scoped guarantee.
- Type hints are not general runtime enforcement. Validate untrusted boundaries.
- `Protocol` = structural contract; dataclass = data/value model; `TypedDict` = typed
  dictionary shape; `NewType` = static distinction with same runtime representation.
- Catch specific exceptions; preserve cause with `raise ... from exc`.
- Use monotonic/performance clock for duration, aware timestamps for domain time.

## Performance and concurrency

- Contract → representative benchmark → instrument/profile → change → prove output
  → compare distribution → ship gradually.
- Algorithm/data structure before micro-optimization.
- Report throughput, p50/p95/p99, queue wait, CPU, memory, allocations.
- Traditional CPython GIL serializes Python bytecode, not logical invariants.
- Threads: blocking I/O/native code; processes: CPU Python/isolation; asyncio: many
  cooperative I/O tasks. Benchmark actual runtime and libraries.
- Bounded queues force an overload decision. Unbounded queues hide it until stale/OOM.
- Cancellation/timeouts require cleanup. Timeout can mean unknown outcome.
- Stable idempotency key + dedupe + reconciliation for ambiguous side effects.

## Real-time and quant systems

- State event identity, event/ingestion/processing time, order, and late-data policy.
- Preserve raw input; normalize once; replay from snapshot + journal.
- Coalesce replaceable views; never silently drop state transitions such as fills.
- Backtest = causal model. Prevent look-ahead, survivorship, revisions, impossible
  fills, timestamp leakage, cost omission, and search overfitting.
- Reproducibility = data + universe + code + dependencies + config + seed + clock +
  event order + execution model.
- Market order chooses execution urgency; limit order chooses worst allowed price.
- Cancel and fill can race. Timeout after send is `UNKNOWN`, not proven failure.
- Critical risk checks live independently at the execution boundary.
- Point-in-time query uses what was published and observed by decision time.

## System design order

1. Requirements and scale.
2. Data/events, identity, clocks, invariants.
3. Main components and flow.
4. State, storage, partitioning.
5. Ordering, backpressure, idempotency, recovery.
6. Capacity/latency calculation.
7. Observability, rollout, security, trade-offs.

## Senior answer shape

> The contract is __. The invariant is __. I would use __ because __. The main
> failure modes are __, handled by __. I would measure __ and change course if __.

## Five phrases to avoid

- “Async is faster.”
- “The GIL makes it safe.”
- “Exactly once” without defining the side effect.
- “Microservices scale better” without workload and failure boundaries.
- “The strategy performed well” without bias, costs, and out-of-sample evidence.
