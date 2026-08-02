# Three-Day Schedule

Plan for three focused blocks per day plus a short evening recall session. Use a
timer. If a drill runs long, write down the gap and move on; coverage matters
before depth.

## Day 1 — Become dangerous in Python

**Outcome:** translate senior Java judgment into idiomatic Python and survive a
language-depth interview.

| Block | Time | Work | Proof of completion |
|---|---:|---|---|
| Diagnostic | 0:20 | Take the diagnostic without notes | Score and gap list |
| Mental model | 1:10 | Chapter 1; type every comparison snippet | Explain five Java/Python traps |
| Data model | 1:40 | Chapter 2; mutability and hashing drills | Predict all outputs before running |
| Break | 0:20 | Walk, no screen | — |
| Functions/iteration | 1:30 | Chapter 3; generators and context manager | Implement a streaming parser |
| Types/architecture | 1:20 | Chapter 4; model order events | Typed domain model in the lab |
| Correctness | 1:00 | Chapter 5; add tests for edge cases | Green test suite |
| Coding sprint | 1:00 | Questions P1–P6, 10 minutes each | Explain complexity aloud |
| Recall | 0:30 | Close the book; write one-page summary | Compare with cheatsheet |

**Stop condition:** you can explain why a tuple may be unhashable, why a mutable
default is dangerous, when `is` differs from `==`, and how a generator preserves
state.

## Day 2 — Think like a quant-platform engineer

**Outcome:** reason about performance, concurrency, real-time behavior, and
backtest/data correctness.

| Block | Time | Work | Proof of completion |
|---|---:|---|---|
| Performance | 1:15 | Chapter 6; profile before changing code | Measurement-backed optimization plan |
| Concurrency | 1:30 | Chapter 7; run async pipeline | Choose thread/process/async for 4 cases |
| Real time | 1:20 | Chapter 8; failure-mode exercise | Pipeline with explicit overload policy |
| Break | 0:20 | Walk, no screen | — |
| Markets | 1:00 | Chapter 9; trace an order lifecycle | State-machine sketch |
| Backtesting | 1:30 | Chapter 10; run capstone tests | Explain 5 ways a backtest lies |
| Data | 1:00 | Chapter 11; temporal join drill | Point-in-time-correct design |
| System design | 1:15 | Design drill A with a 45-minute timer | Recorded 5-minute summary |
| Recall | 0:30 | Flash review from cheatsheet | Gap list for Day 3 |

**Stop condition:** you never say “async is faster” without naming the workload,
and your designs specify ordering, backpressure, recovery, and measurement.

## Day 3 — Convert knowledge into interview performance

**Outcome:** deliver concise answers, complete the capstone, and expose remaining
gaps before the real interview.

| Block | Time | Work | Proof of completion |
|---|---:|---|---|
| Production | 1:10 | Chapter 12 | Deployment and rollback design |
| Capstone | 2:00 | Extend the event-driven backtester | Feature + tests + design notes |
| Python bank | 1:20 | Questions P7–P18 | 2-minute answers, no notes |
| Break | 0:20 | Walk, no screen | — |
| Behavioral | 1:00 | Write six story cards | Each has conflict and metric |
| Mock 1 | 1:00 | Python coding loop | Scorecard |
| Mock 2 | 1:00 | System-design loop | Scorecard |
| Repair | 0:50 | Revisit two weakest areas | Updated answers |
| Final recall | 0:30 | Last-hour cheatsheet | Interview-day plan |

## If you have less time

- **Four hours:** Chapters 1, 2, 6, and 7; question bank P1–P10; QRT role pack.
- **One day:** Day 1 through Types, then Chapters 6, 8, 10, and one mock.
- **Two days:** Complete Day 1 and Day 2; use the behavioral template before bed.

## Study method

Use the loop `predict → run → explain → modify` for every code example. Reading
produces familiarity; prediction and modification produce retrieval strength.
During mocks, narrate assumptions and tests, but do not narrate every keystroke.
