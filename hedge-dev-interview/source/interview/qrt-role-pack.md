# QRT Hong Kong Interview Strategy

This role pack is derived from the supplied **QRT – Quant Dev QP (HK)** posting.
It is preparation guidance, not a claim about QRT's confidential or exact current
interview process.

## Your positioning in one sentence

> I bring mature Java engineering judgment in real-time, reliable systems, and I
> have translated that judgment into idiomatic typed Python, with particular focus
> on deterministic backtesting, data correctness, and production ownership.

Adapt this to evidence you can defend. Do not claim trading or Python production
experience you do not have. A strong honest bridge is better than inflated depth.

## The 90-second introduction

Use four beats:

1. **Present:** your current scope and the systems/users you serve.
2. **Proof:** one technically hard outcome with a number.
3. **Bridge:** why your Java strengths transfer and what Python evidence you built.
4. **Fit:** why trader/quant collaboration and cross-platform ownership appeal.

Example skeleton:

> I am a software engineer with [years] focused on [systems]. In my current/recent
> role I owned [component], where I [hard action] and improved [latency/reliability/
> delivery metric]. Most of my production work has been Java, which gave me strong
> habits around concurrency, testing, architecture, and operations. For this role I
> have deliberately rebuilt those patterns in Python: typed domain models,
> deterministic event replay, bounded async pipelines, profiling, and risk-tested
> backtesting. QRT is attractive because the role sits directly between research,
> trading, data, and production engineering rather than isolating development from
> the investment workflow.

## What to demonstrate

| Area | Minimum evidence | Excellent evidence |
|---|---|---|
| Python | clear coding and object-model explanations | measured or production Python outcome |
| architecture | one modular system with explicit contracts | migration that reduced coupling/risk |
| performance | benchmark/profile story | p99 improvement with correctness proof |
| real time | queues, ordering, failure policy | incident or design under burst/recovery |
| quant systems | capstone and bias awareness | live/backtest parity or data lineage story |
| collaboration | resolved ambiguous requirements | changed design through trader/quant feedback |
| operations | deployment and incident story | control/reconciliation improvement |

## Likely pressure points for a Java-first candidate

Expect follow-ups on why Python is suitable, where it is not, how you avoid dynamic
typing failures, how the GIL changes concurrency, whether Python collection
operations are safe, and what “idiomatic” means. Avoid defensive language. Treat
Python and Java as tools with different economics.

Good framing:

> Python is excellent for research velocity, orchestration, data work, and readable
> domain logic. I recover engineering safety with narrow typed boundaries, runtime
> validation at I/O, tests, immutable values, and observability. For a measured hot
> path, I first improve the algorithm and batching, then use proven native/vectorized
> components or isolate a lower-level implementation behind the same interface.

## Questions to ask the interviewers

- Where is the current boundary between research code and production framework?
- What are the hardest reliability or developer-experience problems for this team?
- Which workloads dominate: batch research, intraday event systems, or execution?
- How do developers, quants, and traders share ownership during incidents?
- What would excellent impact look like after three and twelve months?
- Where does Python reach its limits in your platform, and how are native components
  integrated and operated?
- How are point-in-time data correctness and reproducible backtests enforced?

## Red flags in your own answers

- “The GIL makes it thread safe.”
- “Async is faster.”
- “Kafka gives exactly once” without defining the end-to-end side effect.
- “We use microservices because they scale.”
- “The backtest looked good” without costs, bias controls, and out-of-sample tests.
- “We retry on timeout” without idempotency and reconciliation.
- theory with no decision, measurement, failure mode, or story.

## Final 24-hour checklist

- Re-run all companion tests from a clean shell.
- Solve two Python questions on paper or in a blank editor.
- Deliver one system design in 35 minutes and summarize in 5.
- Rehearse six story cards, including one failure and one disagreement.
- Prepare role/company questions and interviewer-specific variants.
- Sleep; do not replace recall and reasoning with last-minute breadth.
