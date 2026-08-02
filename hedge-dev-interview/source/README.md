# Hedge Fund Quant Developer Interview Field Guide

This is a three-day, interview-first bridge from senior Java development to
production Python in a quantitative hedge-fund environment. The first role pack
targets **Qube Research & Technologies (QRT), Quant Developer, Hong Kong**.

The job description points to six signals:

1. strong Python, not merely Python syntax;
2. backtesting and quantitative data systems;
3. real-time and high-performance engineering;
4. clean architecture and code quality;
5. production ownership, CI/CD, and support;
6. clear collaboration with traders and quants.

This book teaches the reusable core once and keeps employer-specific preparation
in a role pack. Add another hedge-fund role later without duplicating the Python,
systems, or quant-platform material.

## The three-day contract

After three focused days, you should be able to:

- write idiomatic, typed, testable Python under interview time pressure;
- explain Python identity, mutability, hashing, iteration, exceptions,
  concurrency, and performance in terms a senior engineer respects;
- design an event-driven backtester or real-time market-data pipeline;
- reason about determinism, timestamps, data quality, backpressure, tail latency,
  risk controls, deployment, and production incidents;
- answer the QRT role's likely coding, design, and behavioral questions with
  concrete trade-offs rather than slogans.

Three days will not turn anyone into a Python language implementer or a quant
researcher. It can make an experienced Java developer interview-effective by
transferring existing engineering judgment and closing the highest-value gaps.

## Start here

1. Take the [20-minute diagnostic](start/diagnostic.md).
2. Read the [role-to-competency map](start/role-map.md).
3. Follow the [three-day schedule](start/three-day-plan.md).
4. Type the examples; do not only read them.
5. Run the [capstone lab](labs/README.md) and finish with a
   [mock interview](interview/mock-loops.md).

## How each chapter works

Every core chapter uses the same extension-friendly pattern:

- **Interview outcome** — what you must be able to do aloud or in code.
- **Java bridge** — the closest familiar concept and where the analogy breaks.
- **Python model** — the rule that predicts behavior.
- **Failure modes** — bugs interviewers expect senior developers to spot.
- **Drill** — an active task with an observable result.
- **Answer frame** — a concise way to explain the concept.

The runnable companion project is under [`code/`](code/README.md). It uses only
the Python standard library so setup cannot consume your study time.

> Interview north star: establish the contract, name the invariant, choose the
> mechanism, explain failure modes, then discuss measurement and trade-offs.
