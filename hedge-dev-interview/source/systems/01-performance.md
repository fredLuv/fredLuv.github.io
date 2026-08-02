# 6. Measure and Optimize Python

## Interview outcome

Diagnose performance with evidence, choose the right level of optimization, and
avoid false claims about “Python being slow.”

## Start with a performance contract

Ask before tuning:

- What workload and data distribution are representative?
- Is the target throughput, end-to-end latency, jitter, memory, startup, or cost?
- Which percentile and time window matter?
- What correctness and freshness constraints cannot change?
- Where is time actually spent: CPU, I/O, lock/queue wait, serialization, GC, or
  downstream service?

For real-time systems, record p50, p95, p99, maximum/sample count, queue depth,
and drops. An average can conceal rare delays that dominate trading risk.

## Complexity still wins first

Changing O(n²) to O(n log n) beats syntax tricks. Choose the data structure that
matches the operation: set/dict for membership, deque for FIFO, heap for top-k,
bisect or indexed storage for ordered search.

Then reduce work:

- compute once, not in an inner loop;
- batch calls across an expensive boundary;
- stream instead of materializing unnecessary intermediates;
- push filtering near storage when semantically safe;
- cache only with bounded size and explicit invalidation.

## Measure at three scales

1. **Micro:** `timeit` for a small, isolated operation. Warm up and run many times.
2. **Function/program:** `cProfile` for call time/count; a sampling or line profiler
   when call aggregation is insufficient.
3. **System:** monotonic timing and production telemetry across queues, network,
   serialization, and downstream dependencies.

Use `time.perf_counter_ns()` for elapsed time. Wall-clock timestamps can jump and
should not measure durations.

## CPython and the GIL

In the traditional CPython build, a global interpreter lock means only one thread
executes Python bytecode at a time within an interpreter. That does **not** mean:

- threads are useless (they overlap blocking I/O);
- compound operations are automatically safe;
- code cannot interleave between logical steps;
- native libraries cannot run in parallel (many release the GIL);
- all Python implementations/builds have identical behavior.

Free-threaded CPython builds are emerging, but code should not depend on accidental
atomicity. Protect invariants and benchmark the actual deployment runtime.

## The optimization ladder

Use the lowest rung that meets the contract:

1. better algorithm/data structure;
2. built-ins and standard-library operations implemented efficiently;
3. reduce allocation, copying, conversions, and boundary crossings;
4. vectorized/columnar libraries for numerical bulk work;
5. parallelism or partitioning when the workload supports it;
6. JIT/compiled extension/native service for a proven hot path.

Native boundaries add build, portability, debugging, memory-safety, and deployment
cost. Isolate them behind a stable interface and keep a correctness reference path.

## Vectorization is not magic

Vectorized numerical operations can move loops into optimized native code, improve
memory locality, and release the GIL. They can also create large temporaries,
inflate memory, and make irregular branching worse. Profile with realistic shapes.

## Memory and allocation

- A generator avoids materializing all results but does not make retained source
  data disappear.
- `slots` can reduce per-instance overhead for many small objects; measure.
- columnar arrays are often denser than millions of Python objects.
- unbounded dictionaries, queues, caches, and retained tracebacks are common leaks.
- object pooling in Python is often counterproductive; measure lifecycle and GC.

## Performance answer example

> I would first define the p99 latency and throughput target using a representative
> replay. I would instrument stage latency and queue wait, then profile the CPU-hot
> stage. If parsing dominates, I would test batching and a faster/native parser;
> if queue wait dominates, CPU tuning is irrelevant. I would compare distributions,
> verify outputs bit-for-bit or within an explicit tolerance, and retain a rollback.

## Drill

Given code that recomputes a 100-point moving average with `sum(window) / 100` for
every tick, implement an O(1)-update rolling sum with a `deque`. Benchmark both on
the same seeded input, verify identical outputs within a declared tolerance, and
report p50/p99 if timing individual updates.
