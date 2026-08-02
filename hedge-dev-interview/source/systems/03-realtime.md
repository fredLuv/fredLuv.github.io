# 8. Real-Time Pipeline Design

## Interview outcome

Design an event pipeline that stays correct under bursts, duplicates, gaps,
restarts, and partial failure.

## A reference flow

```text
feed → decode → validate/sequence → normalize → publish → strategy → risk → orders
          │             │               │          │          │
       metrics       gap repair       journal    state      audit
```

Keep raw ingress recoverable when possible. Normalization creates a stable internal
schema. Every stage has a bounded capacity, owner, error policy, and health signal.

## Ordering is a domain question

Wall-clock timestamps rarely provide a total order. Prefer source sequence numbers.
For multiple sources, define a deterministic merge key such as `(event_time,
source_priority, source_sequence)` and document what that ordering means.

Handle:

- duplicate sequence → ignore idempotently or verify same payload;
- forward gap → pause affected stream, request snapshot/replay, then resume;
- late event → correct state, route to revision, or reject by declared policy;
- restart → restore snapshot plus journal and reconcile with external truth.

## Three clocks

- **Event time:** source says the event occurred.
- **Ingestion time:** your boundary received it.
- **Processing time:** a stage handled it.

Record all relevant clocks plus monotonic durations. Freshness is “now minus latest
valid event time/ingestion time” according to an explicit definition.

## Overload policies

| Data | Usually acceptable | Usually dangerous |
|---|---|---|
| top-of-book snapshot | coalesce superseded updates | process hours-old snapshots |
| incremental book delta | backpressure, replay, resync | drop one delta silently |
| signal/analytics refresh | shed/coalesce with freshness mark | claim fresh when stale |
| order/fill/risk event | durable journal and fail closed | loss, duplicate side effect |

Overload behavior must preserve business semantics, not just process uptime.

## Idempotency and reconciliation

“Exactly once” across networks is generally a system claim built from durable
identity, deduplication, transactional boundaries, and reconciliation—not a magic
transport flag. Use stable event/order IDs and make consumers idempotent.

After an ambiguous side effect:

1. retain the intent and idempotency key;
2. mark local state `UNKNOWN`, not `FAILED`;
3. query the authoritative external system;
4. reconcile and emit an auditable state transition;
5. alert if uncertainty exceeds a time/risk threshold.

## Latency budget

Split the end-to-end objective into receive, decode, queue, compute, risk, encode,
and send. Measure queue wait separately from service time. Watch coordinated
omission in benchmarks: a blocked load generator can undercount requests that
would have arrived during a stall.

## Operational controls

- stale-data gate and kill switch;
- position/notional/rate limits independent of strategy logic;
- dead-letter or quarantine for malformed non-critical data;
- snapshot/checkpoint plus journal retention;
- source and consumer lag metrics;
- versioned configuration and reproducible deployment;
- reconciliation against venue/broker and accounting sources.

## Design drill

Design a service consuming 100k ticks/second with 10× bursts. Strategies need the
latest price per symbol within 50 ms; every raw tick must remain available for
replay. Your answer should separate the durable raw path from the coalesced live
view, state partitioning key, queue bounds, freshness policy, recovery, and p99
measurement.

## Answer frame

> I start by identifying which events are state transitions versus replaceable
> views. I define ordering, identity, queue bounds, and overload semantics per
> stream. I preserve raw input for deterministic replay, make side effects
> idempotent, recover from snapshot plus journal, reconcile with external truth,
> and measure end-to-end tail latency and freshness.
