# 20-Minute Diagnostic

Answer without running code. Give yourself one point per correct answer and one
point per clear explanation.

## Questions

1. What is printed, and why?

   ```python
   rows = [[0]] * 3
   rows[0].append(1)
   print(rows)
   ```

2. Why is `def add(x, items=[]): ...` usually a bug? Give a correct alternative.
3. When can `a == b` be true while `a is b` is false?
4. Why can `(1, [2])` not be a dictionary key even though it is a tuple?
5. What does a generator save compared with a list, and what does it cost?
6. What is the difference between an iterable and an iterator?
7. Does a type annotation reject the wrong type at runtime?
8. When would a `Protocol` be preferable to an abstract base class?
9. What work is suitable for threads, processes, and `asyncio` respectively?
10. Does the GIL make race conditions impossible?
11. Name three measurements needed before calling code “fast.”
12. Why is average latency insufficient for a trading system?
13. What should happen when a market-data consumer cannot keep up?
14. Name four forms of look-ahead or survivorship bias.
15. What makes a backtest replay deterministic?
16. Distinguish event time, ingestion time, and processing time.
17. How would you make order submission retry-safe?
18. What would you log/measure around a live strategy?
19. Sketch a safe schema migration for a shared event.
20. State one production incident as: symptom, impact, evidence, action, prevention.

## Scoring

- **32–40:** compress the early chapters; spend time on design and mocks.
- **22–31:** follow the three-day plan as written.
- **12–21:** prioritize Chapters 1–8 and one backtesting chapter.
- **0–11:** three days is a crash course; focus on correctness and honest reasoning.

## Answer checkpoints

1. All three rows reference the same inner list: `[[0, 1], [0, 1], [0, 1]]`.
2. The default is created once. Use `None`, then allocate inside.
3. Equality compares value by a type-defined rule; identity compares object identity.
4. Hashability is recursive: the nested list is mutable and unhashable.
5. Lazy iteration saves peak memory and can reduce latency-to-first-result; it is
   single-pass unless recreated and may defer exceptions.
6. An iterable can produce an iterator; an iterator also carries traversal state.
7. No. Annotations are metadata used by tools unless code explicitly enforces them.
8. When consumers need structural typing without inheritance or runtime coupling.
9. Usually: threads for blocking I/O or C extensions releasing the GIL; processes
   for isolated CPU-bound Python; asyncio for many cooperatively scheduled I/O tasks.
10. No. Operations can interleave, extension code may release it, and compound
    invariants still require synchronization.
11. Workload, baseline, and distribution (including p95/p99), plus CPU/memory/allocations.
12. A small set of slow events can dominate risk while barely moving the mean.
13. Apply a declared policy: block/backpressure, coalesce, shed, spill, or fail closed.
14. Future prices, revised fundamentals, today’s universe, delisted-name exclusion,
    future-aware normalization, or impossible fills.
15. Stable inputs, total event ordering, explicit seeds, deterministic clocks, and
    recorded configuration/code version.
16. When the source says it happened; when the platform received it; when this stage
    handled it.
17. Stable client order ID plus deduplication and query/reconcile after ambiguity.
18. Inputs, decisions, orders, acknowledgements/fills, positions, risk, errors,
    queue depth, freshness, latency percentiles, version, and correlation IDs.
19. Additive compatible change, dual read/write if needed, backfill, measure, switch,
    then remove only after all consumers migrate.
20. A strong answer separates facts from guesses and ends with a system improvement.
