# 10. Backtesting Without Self-Deception

## Interview outcome

Design a deterministic, point-in-time-correct backtester whose limitations are
visible and testable.

## Backtest architecture

```text
versioned data → ordered events → strategy → target/orders → risk → fill model
                        ↑                                      │
                        └──────── portfolio/accounting ←───────┘
```

Use the same domain events and strategy/risk interfaces in simulation and live
execution where practical. Replace adapters and clocks, not the business rules.
Perfect parity is impossible—simulation must model fills—but gratuitous divergence
creates untestable risk.

## Determinism checklist

- immutable/versioned input data and universe;
- total event ordering with a documented tie-breaker;
- explicit clock; no call to current wall time inside domain logic;
- recorded random seed and deterministic sampling where possible;
- versioned code, dependencies, configuration, fees, calendars, and corporate
  action rules;
- stable numeric/rounding policy;
- output manifest with data and code fingerprints.

Re-running the same manifest should produce the same orders, fills, and results.

## How backtests lie

- **Look-ahead:** use information unavailable at the decision timestamp.
- **Survivorship:** test only instruments that survived to today's universe.
- **Selection/overfitting:** choose a winner after many trials without accounting
  for the search.
- **Revision bias:** use later-corrected fundamentals/economic releases.
- **Execution fantasy:** fill at mid/close despite latency, spread, queue, and size.
- **Corporate-action errors:** prices and cash flows adjusted inconsistently.
- **Missingness leakage:** forward-fill across a period where data was not knowable.
- **Timestamp leakage:** bar labeled by start/end used before it completed.

## Event-driven versus vectorized

Vectorized research is fast and expressive for signal exploration. Event-driven
simulation naturally models state, order lifecycle, latency, and causality. A
mature platform may use both: fast vectorized screening plus event-driven
validation before promotion.

## Fill and cost models

State assumptions explicitly:

- decision-to-order and order-to-venue latency;
- spread crossing and fees/rebates;
- participation/volume limits;
- partial fills and market impact;
- queue position if relevant;
- stale or missing market data;
- borrow, funding, FX, and trading-calendar rules.

A simple model is acceptable if conservative and declared. False precision is not.

## Evaluation discipline

Keep a final untouched out-of-sample period. Prefer rolling/walk-forward evaluation
when retraining/recalibration is part of the process. Report turnover, drawdown,
exposure, capacity assumptions, stability across regimes, and sensitivity to costs—not
only Sharpe or cumulative return.

## Tests that matter

- identical replay produces identical results;
- no order uses an event later than its decision time;
- fees and cash reconcile on a hand-calculated example;
- duplicate fills do not change position twice;
- split/dividend handling conserves economic value under the chosen convention;
- empty/missing session behavior is explicit;
- strategy cannot trade before warm-up completes.

## Drill

Your daily strategy uses today's official close to create an order filled at that
same close. Explain why this is generally look-ahead. Repair it by either trading
at the next event/session or by modeling a decision signal available before the
close and a realistic order cutoff/fill process.

## Answer frame

> A backtest is an executable causal model. I make data availability, ordering,
> clocks, fill assumptions, costs, and configuration explicit and reproducible.
> I test invariants on hand-calculable streams, guard point-in-time correctness,
> and separate fast research from execution-realistic validation.
