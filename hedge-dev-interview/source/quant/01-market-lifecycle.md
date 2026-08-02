# 9. Market and Order Lifecycle

## Interview outcome

Speak the domain language needed to build a trading platform and model an order as
a state machine rather than a database row.

## Minimum market vocabulary

- **Bid/ask:** best displayed buy/sell prices; spread is ask minus bid.
- **Mid:** `(bid + ask) / 2`; a reference value, not an executable guarantee.
- **Market order:** prioritizes execution, not price.
- **Limit order:** constrains price, not execution.
- **Liquidity:** ability to trade size with limited price impact.
- **Slippage:** execution price versus chosen reference; define sign convention.
- **Maker/taker:** liquidity-providing/removing behavior and often fee categories.
- **Position:** signed inventory; distinguish gross, net, and exposure by factor/book.
- **PnL:** realized plus unrealized under explicit marking, fees, FX, and funding rules.

## Order lifecycle

```text
CREATED → VALIDATED → SENT → ACKNOWLEDGED → PARTIALLY_FILLED → FILLED
    │          │         │          ├──────────────→ CANCEL_PENDING → CANCELLED
    └→ REJECTED└→ REJECTED└→ UNKNOWN└──────────────→ REJECTED/EXPIRED
```

Real venues vary. A cancel and fill can race. A timeout after submission produces
`UNKNOWN`, because absence of acknowledgement is not proof of absence at venue.

Important quantities:

```text
0 ≤ cumulative_filled ≤ original_quantity
leaves_quantity = original_quantity - cumulative_filled
```

Updates may duplicate or arrive late. Use venue/source sequence and cumulative
quantity to make state application idempotent. Never generate extra position from
a duplicated fill.

## Risk before and after the order

Pre-trade controls include max quantity/notional, price collars, position limits,
restricted instruments, market-data freshness, and message rate. Post-trade
controls reconcile positions, cash, fills, PnL, and broker/venue truth.

Risk should not be only a function called by strategy code. Enforce critical
limits independently at an execution boundary so a faulty or bypassing strategy
cannot skip them.

## Market data models

- **Trades:** executed events, not the whole available liquidity picture.
- **Top of book:** best bid/ask and sizes; updates can often be coalesced.
- **Depth/book deltas:** incremental state; one missing update may invalidate all
  later state until resnapshot.
- **Bars:** derived aggregates; define time zone, session, corporate actions, and
  whether incomplete bars are visible.

## Drill

Receive: acknowledgement, partial fill 30, duplicate partial fill 30, cancel
acknowledgement, then late fill with cumulative 40. State the final filled and
leaves quantities and whether `CANCELLED` may still receive a venue-authoritative
late fill. Explain how you prevent double-counting.

## Answer frame

> I model orders as explicit state transitions driven by idempotent events. I
> distinguish local intent, transport acknowledgement, and venue truth. Cancel/fill
> races and ambiguous timeouts are first-class states, and position is updated from
> deduplicated incremental or cumulative fill evidence.
