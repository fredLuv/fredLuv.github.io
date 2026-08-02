# 5. Errors, Testing, and Observability

## Interview outcome

Design explicit failure contracts, test invariants and temporal behavior, and
leave enough evidence to support a running strategy.

## Exceptions are part of the API

Use specific exceptions and preserve causal context:

```python
class MarketDataError(RuntimeError):
    pass

def load_snapshot(path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise MarketDataError(f"cannot read snapshot: {path.name}") from exc
```

Distinguish programmer errors/invariant violations from expected operational
failures. Retrying an invalid symbol is pointless; retrying a transient connection
failure may be reasonable if the operation is idempotent and the retry is bounded.

Never catch broadly only to continue. At a process boundary, a broad catch can log
and convert to a controlled exit, but internal code should catch only failures it
can handle.

## Test the contract, not the implementation

A compact hierarchy:

1. pure unit tests for math, states, and policy;
2. component tests for database/broker adapters;
3. replay tests using representative event streams;
4. a small end-to-end smoke test;
5. production canary and runtime invariants.

For quant systems, test properties:

- position after fills equals prior position plus signed fills;
- risk rejection never submits an order;
- cumulative fill quantity never decreases;
- replaying the same ordered events yields the same result;
- cash plus marked holdings reconciles within a defined tolerance;
- cancel/fill races resolve to a legal final state.

## Arrange, act, assert — with explicit clocks

Do not sleep in unit tests. Inject a clock or drive an event loop with controlled
events. A deterministic fake should behave like the port, not expose internals.

```python
from datetime import datetime, timezone

class FixedClock:
    def __init__(self, value: datetime) -> None:
        self.value = value

    def now(self) -> datetime:
        return self.value

clock = FixedClock(datetime(2026, 1, 2, tzinfo=timezone.utc))
```

## Logging versus metrics versus traces

- **Logs:** discrete evidence with fields. Include event/order/strategy correlation
  IDs, version, outcome, and actionable context. Do not leak secrets.
- **Metrics:** aggregated health and performance. Rate, errors, duration, saturation;
  add market-data freshness, queue depth, rejects, position mismatch, and P&L sanity.
- **Traces:** causal path across stages/services; useful for tail-latency attribution.

Avoid high-cardinality metric labels such as raw order IDs. Put them in logs/traces.

## Assertions and validation

`assert` is for programmer assumptions and may be disabled. Do not use it to
validate user input, authorization, or risk limits. Raise a real exception for a
runtime contract.

## Timeouts, retries, and idempotency

Every remote call needs a time budget. A timeout means the outcome may be unknown,
not necessarily failed. Retries require:

- a retry-safe/idempotent operation or stable idempotency key;
- bounded attempts and overall deadline;
- exponential backoff with jitter where appropriate;
- observability and a terminal recovery path;
- no amplification across multiple layers all retrying.

## Drill

Write tests for an order risk policy with max absolute position and max order size.
Cover the boundary value, negative/sell quantity, current short position, zero,
and non-finite price. Then state which checks belong before submission and which
must also exist independently downstream.

## Answer frame

> I make failure behavior part of the contract. Tests focus on invariants and
> deterministic replay, with I/O tested at adapters. In production I combine
> structured logs for evidence, bounded-cardinality metrics for detection, and
> traces for causal latency. A timeout creates uncertainty, so retry policy must
> account for idempotency and reconciliation.
