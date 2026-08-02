# Runnable Capstone Lab

The companion project under [`../code/`](../code/README.md) is a deliberately small
single-symbol event-driven trading simulation. It is not a realistic exchange simulator. Its
purpose is to make interview concepts executable:

- frozen/slot-based domain events;
- protocols and injected policies;
- stable event ordering and deterministic replay;
- rolling signal generation without repeated full-window sums;
- pre-trade position/order limits;
- explicit fills, positions, cash, and decisions;
- bounded `asyncio` pipeline with observable backpressure;
- standard-library unit tests.

## Run it

From the GitBook directory:

```bash
cd code
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m hedgeprep.demo
PYTHONPATH=src python3 -m hedgeprep.async_pipeline
```

Python 3.12 or newer is recommended.

## Read in this order

1. `events.py`: immutable domain vocabulary.
2. `risk.py`: narrow policy with explicit rejection reasons.
3. `strategy.py`: O(1) rolling state and decision rule.
4. `engine.py`: deterministic orchestration and accounting.
5. `async_pipeline.py`: queue bounds, producer/consumer ownership, sentinel end.
6. `tests/`: executable invariants.

## Day 3 extension choices

Pick one, time-boxed to 90 minutes:

### A. Add costs

Add per-share fee and half-spread slippage. Keep prices/cash consistent, add a
hand-calculated test, and explain whether floats remain acceptable.

### B. Add delayed fills

Schedule fills at the next market event rather than immediately. Define order of
market, decision, order, and fill at equal timestamps. Test no same-tick look-ahead.

### C. Add kill switch

Stop new orders after cumulative loss or stale data, while continuing to process
fills. Test the difference between halting decisions and halting state updates.

### D. Add replay manifest

Hash the input events and write a JSON manifest containing code/config version,
seed, event count, and result checksum. Explain what is still missing for six-month
reproducibility.

## Interview walkthrough (five minutes)

1. State scope: teaching simulator, not production exchange fidelity.
2. Point to immutable events and the explicit total order.
3. Explain strategy/risk separation and deterministic injected inputs.
4. Name two deliberate limitations and how production would address them.
5. Show one invariant test and one extension trade-off.

## Review questions

- Why does the event order include a sequence after timestamp?
- What fails if duplicate fills arrive?
- Why does risk use projected position?
- Where would a broker adapter fit without changing the domain?
- Which async queue events could be coalesced and which must not be?
- How would you profile this before optimizing it?
