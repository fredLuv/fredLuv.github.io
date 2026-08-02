# Python Question Bank

Use a timer. For coding questions: clarify, state examples/invariants, write the
simplest correct solution, test boundaries, then analyze complexity.

## Coding drills

### P1 — Deduplicate while preserving order

Return unique events by `event_id`, keeping first occurrence. What changes if the
stream is unbounded? Target: dict/set behavior, hashability, memory policy.

### P2 — Merge event streams

Merge k individually sorted iterables by `(timestamp, source, sequence)` lazily.
Target: iterators, heap, O(n log k), deterministic tie-break.

### P3 — Rolling statistics

Produce a rolling mean for window `w` in O(n) total time and O(w) space. Define
warm-up output and invalid inputs.

### P4 — LRU cache

Implement fixed-capacity get/put with O(1) average operations. Discuss why a
standard implementation is preferable in production and whether it is thread safe.

### P5 — Rate limiter

Implement a per-key sliding-window limiter. State clock choice, memory bounds,
concurrency, cleanup, and distributed limitations.

### P6 — Positions from fills

Aggregate signed positions while deduplicating fill IDs. Reject conflicting
duplicates. Target: domain invariants and error policy.

### P7 — Bounded async mapper

Apply an async function to inputs with at most `n` in flight, preserving result
order. Define cancellation and partial-failure semantics.

### P8 — Context-managed timer

Record success/failure count and elapsed time without suppressing exceptions.

### P9 — Top-k exposure

Return k largest absolute exposures from a stream. Compare sorting versus heap and
define ties.

### P10 — Point-in-time lookup

Given revisions sorted by publication time and decision timestamps, return the
latest record known at each decision without future leakage.

## Language-depth prompts

### P11 — `is` versus `==`

Identity versus type-defined equality. Use `is None`; do not rely on interning.

### P12 — Hashability

Equal implies equal hash; hash stable while stored. A tuple is hashable only when
its elements are. Mutable values should not normally be keys.

### P13 — Mutable defaults

Evaluated once at function definition. Use a sentinel/`None` then allocate.

### P14 — Iterator versus iterable

Iterable produces an iterator; iterator retains state and returns itself from
`__iter__`; generator is a concise suspended iterator. Mention one-shot behavior.

### P15 — Decorator mechanics

Decoration occurs at definition/import; function is replaced. Preserve metadata
with `wraps`, signature types with `ParamSpec`, exceptions/return value.

### P16 — Context manager mechanics

`__enter__`/`__exit__` guarantee scoped cleanup; `__exit__` can suppress only by
returning truthy. Discuss transaction commit/rollback and exception causality.

### P17 — Type hints

Gradual static metadata, not runtime enforcement. Use checker plus boundary
validation; distinguish `Protocol`, `TypedDict`, dataclass, and `NewType`.

### P18 — GIL

Traditional CPython serializes Python bytecode per interpreter but does not remove
races; threads help I/O/native releases, processes help CPU Python. Do not promise
implementation-specific atomicity.

### P19 — Async cancellation

Cancellation arrives at suspension points; use structured ownership and `finally`.
Shield only a tiny operation that truly must complete and still respect deadlines.

### P20 — Memory diagnosis

Measure RSS and allocations/retention; inspect unbounded caches/queues, global
registries, callbacks, tasks, and tracebacks. Reproduce with workload and compare
snapshots; do not assume garbage collection is the cause.

## Two-minute answer rubric

A strong answer includes:

1. a correct definition;
2. a minimal example or scenario;
3. one failure mode;
4. a decision rule or trade-off;
5. no invented certainty.
