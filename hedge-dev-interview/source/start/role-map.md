# Role-to-Competency Map

## What the posting actually asks for

The supplied QRT posting describes a developer who builds and enhances core
components, works across electronic and algorithmic trading, backtesting, and
data management, partners with traders and quants, supports running strategies,
and brings new technology into a mature engineering process.

| Posting signal | Interview evidence to prepare | Book location | Priority |
|---|---|---|---|
| Strong Python | Idioms, object model, typing, testing, concurrency, profiling | Chapters 1–7 | Critical |
| Backtesting | Event ordering, fills, costs, bias, deterministic replay | Chapter 10 + lab | Critical |
| Data management | Temporal correctness, schemas, validation, lineage | Chapter 11 | High |
| Real-time systems | Bounded queues, backpressure, latency, recovery | Chapters 7–8 | High |
| High performance | Measurement, allocation, vectorization, native boundaries | Chapter 6 | High |
| Clean architecture | Domain boundaries, protocols, dependency direction | Chapters 4 and 13 | High |
| Run/support strategies | Observability, safe deploys, incident reasoning | Chapters 5 and 13 | High |
| Work with traders/quants | Requirement discovery and explainable trade-offs | Behavioral pack | High |
| CI/CD and DevOps | Test pyramid, artifact promotion, rollback, controls | Chapter 13 | Medium-high |
| C++ or C# useful | Know when Python should delegate to native code | Chapter 6 | Bonus |

## The likely evaluation surface

The job description does not publish an interview sequence. Prepare for the
capabilities rather than guessing exact rounds:

1. **Python coding:** collections, iterators, object design, edge cases,
   complexity, tests, and readable code.
2. **Python depth:** mutability, equality/hash contract, decorators, generators,
   context managers, typing, GIL, async, multiprocessing, and profiling.
3. **Systems design:** a market-data pipeline, backtester, execution/risk service,
   or research data platform.
4. **Production judgment:** incident handling, release safety, observability,
   schema evolution, and stakeholder communication.
5. **Experience:** examples where you owned a component, improved quality or
   latency, supported users, and changed your mind after evidence.

## What transfers from Java

Your advantages are architecture, concurrency vocabulary, testing discipline,
production operations, complexity reasoning, and the ability to make invariants
explicit. The main risks are writing Java-shaped Python, assuming static types
change runtime behavior, overusing classes, misunderstanding Python object
identity and mutability, and making incorrect claims about the GIL.

## Evidence ladder

A claim becomes credible in this order:

```text
"I know X" < explanation < working code < measured result < production story
```

For each critical row above, prepare at least one explanation and one concrete
example. For Python, also prepare working code. For operations and collaboration,
prepare a production story with a measurable result.

## Scope boundaries

The QRT role is quantitative development, not a pure quant-research role. Learn enough
market mechanics and backtest correctness to engineer the platform. Do not spend
your three days deriving stochastic calculus unless an interviewer or a newer
role description explicitly asks for it.

For the separate Jump middle/back-office track, use the
[Jump role pack](../roles/jump-middle-back-office.md). Its critical path is Python,
SQL, Kafka, transactional workflows, and business-facing delivery—not alpha research.
