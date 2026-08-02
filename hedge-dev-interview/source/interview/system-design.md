# System-Design Drills

## The interview canvas

Use this order so your answer remains navigable:

1. requirements, scale, and success/failure semantics;
2. events/data model and time/identity;
3. high-level flow and component responsibilities;
4. state, partitioning, and storage;
5. ordering, backpressure, idempotency, and recovery;
6. latency/capacity calculation;
7. observability, deployment, security, and trade-offs.

## Drill A — Event-driven backtesting platform

Support 100 researchers, equities/futures, daily and tick data, reproducible runs,
parameter sweeps, cost/fill models, and promotion toward live strategies.

Must cover: immutable/versioned data, point-in-time universe, run manifest,
deterministic event order, compute scheduling and quotas, artifact/results store,
experiment metadata, failure isolation, cache correctness, and research/live parity.

Pressure questions:

- How do you prevent look-ahead centrally rather than by convention?
- What exactly makes a run reproducible six months later?
- How do you avoid one parameter sweep starving the cluster?
- Which results can safely be cached, and what is the cache key?
- How is a strategy promoted without copying its logic?

## Drill B — Real-time market-data distribution

Consume multiple feeds at 100k events/sec average and 1m peak. Thousands of
symbols; several strategies need sub-50-ms freshness; raw data must be replayable.

Must cover: adapters, source sequences, gap recovery, normalized schema, raw
journal, partitioning, bounded queues, per-data-type overload policy, snapshots,
consumer isolation, freshness and p99 telemetry, schema evolution.

Pressure questions:

- Can top-of-book updates be dropped? Can depth deltas?
- What happens when one consumer is slow?
- How does a restarted consumer rebuild state?
- How do you compare source event time to platform latency safely?

## Drill C — Order and pre-trade risk service

Accept orders from multiple strategies, enforce limits, route to brokers/venues,
track state, and remain safe through duplicate requests and ambiguous timeouts.

Must cover: client order IDs/idempotency, order state machine, independent risk
boundary, durable intent, venue adapters, cancel/fill races, reconciliation,
kill switch, audit, permissions, and controlled degradation.

Pressure questions:

- The send timed out. Do you retry?
- Risk state is stale. Fail open or closed?
- How do limits update without inconsistent partial rollout?
- What is the source of truth for position after restart?

## Lightweight capacity math

State assumptions and calculate orders of magnitude:

```text
events/day = events/sec × active seconds
raw bytes/day = events/day × encoded bytes/event
required workers ≈ arrival rate × service time / target utilization
```

At 1,000,000 events/sec and 100 bytes/event, raw payload alone is about 100 MB/sec
before replication, indexes, metadata, and compression. Numbers expose design
constraints; precision theatre does not.

## Self-score (0–2 each)

- clarified functional and non-functional requirements;
- defined event identity, time, ordering, and state;
- addressed overload and recovery before prompting;
- connected storage/partitioning to access pattern;
- quantified throughput/latency/storage;
- covered observability and business invariants;
- explained alternatives and why one was chosen;
- gave a concise final summary.

Target: 12/16 before the interview.
