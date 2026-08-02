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

## Relational databases and SQL

- Start from business identity and invariants; enforce `NOT NULL`, `CHECK`,
  `UNIQUE`, and foreign keys in the database.
- A surrogate ID does not replace the unique external/business key.
- Preserve immutable lifecycle history; build reconstructible current projections.
- Choose isolation from the anomaly. Read Committed can change snapshots between
  statements; Serializable may abort and requires whole-transaction retry.
- Keep transactions short. Never hold locks across remote calls or user waits.
- Use conditional updates/row locks for scarce resources such as locates.
- Design indexes from real predicates, joins, ordering, and cardinality; verify with
  `EXPLAIN (ANALYZE, BUFFERS)` in a safe environment.
- Latest-row query needs a deterministic tie-break (`ROW_NUMBER` is often useful).
- Parameterize SQL; bound pools; stream large results; evolve schemas expand/contract.
- SQL state + Kafka event: write an outbox row in the same transaction.

## Kafka

- Ordering is within one partition. Choose the key from the domain invariant.
- Consumer-group parallelism is bounded by partition count.
- At-least-once = side effect then offset commit; duplicates are expected.
- Database consumer: processed-event unique key and business write in one transaction.
- “Exactly once” for Kafka-to-Kafka does not cover arbitrary external side effects.
- Rebalance safely: finish/stop in-flight work and commit only completed offsets.
- Poison record policy needs quarantine, ownership, alert, evidence, and replay.
- Retry topics can reorder one key; decide whether ordering or availability wins.
- Measure time/freshness lag, not only offset count; zero lag does not prove correctness.
- Schema evolution: tolerant consumers first, additive fields, compatibility in CI.

## Middle and back office

- Execution → capture/enrich → allocate → confirm → clear → settle → reconcile.
- Track economic, allocation, confirmation, clearing, settlement, and reconciliation
  state separately.
- A timeout after external instruction is `UNKNOWN`; query and reconcile before retry.
- Ledger corrections are reversing/replacement entries, not deleted history.
- Reconciliation produces durable owned breaks with age, exposure, evidence, and resolution.
- Business dates, calendars, cutoffs, completeness, and correctness often matter
  more than microsecond latency.

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
