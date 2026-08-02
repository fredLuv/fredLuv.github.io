# 12. Middle and Back Office Lifecycle

## Interview outcome

Explain what happens after a trade, model the lifecycle as auditable state
transitions, and design controls that detect missing, duplicated, late, or
inconsistent records before they become financial or regulatory problems.

## Front, middle, and back office

The boundaries vary by firm, but this working model is useful:

- **Front office:** investment decision, order generation, execution, and trader
  tooling.
- **Middle office:** independent risk, trade control, valuation/P&L checks,
  allocations, exceptions, financing/borrow controls, and cross-team workflow.
- **Back office:** confirmation, clearing, settlement, cash/securities movements,
  books and records, regulatory outputs, and reconciliation.

The middle/back office is not “just CRUD.” Its software establishes whether the
firm's economic and legal records agree with brokers, venues, clearinghouses,
custodians, administrators, and internal books.

## A simplified post-trade flow

```text
execution
   ↓
trade capture → enrich/reference data → allocate → affirm/confirm
   ↓                    ↓                   ↓
intraday risk       fees/currency       account/fund
   ↓
clearing/netting → settlement instruction → cash/securities movement
   ↓
positions, ledger, P&L, regulatory records, reconciliation, exceptions
```

Every arrow can fail independently. Model each transition with an event identity,
source, effective time, observed time, version, actor, reason, and correlation ID.

## Trade identity and state

One trade may have several identifiers: internal trade ID, execution ID, broker
ID, clearing ID, allocation ID, and settlement instruction ID. Never assume a
vendor identifier is globally unique. Store its namespace/source with the value.

A useful state model separates dimensions instead of forcing one giant status:

- economic state: booked, amended, cancelled;
- allocation state: unallocated, partial, allocated;
- confirmation state: unmatched, matched, affirmed;
- clearing state: pending, accepted, rejected;
- settlement state: instructed, pending, settled, failed;
- reconciliation state: unchecked, matched, break open, break resolved.

An amendment is usually a new version or compensating event, not an in-place edit
that destroys history. Keep current-state projections for fast reads, backed by an
immutable audit/event history.

## Clearing, settlement, locates, and risk

### Clearing

Clearing validates obligations, may novate a trade to a central counterparty,
calculates net obligations and margin, and manages default risk. Your system must
track acceptance/rejection, clearing account, netting set, fees, and source truth.

### Settlement

Settlement exchanges securities and cash on the agreed date. Correctness depends
on calendars, currency, standing settlement instructions, custody accounts,
cut-off times, partial settlement rules, and status feedback. A failed settlement
is a state requiring reason, owner, aging, escalation, and eventual resolution.

### Locates and stock borrow

For a short sale, a locate/borrow workflow establishes that shares can be borrowed
under applicable policy. Track request, approval, quantity consumed, expiry,
recall, rate, and source. Concurrent orders must not consume the same availability
twice; this is a transactional invariant.

### Risk

Middle-office risk aggregates positions and exposures across strategies, accounts,
legal entities, currencies, and asset classes. It needs explicit valuation time,
market-data version, FX rates, netting rules, and lineage. A number without “as of,”
scope, and source is not a reliable risk number.

## Reconciliation is a first-class product

Reconciliation compares two independently produced views and explains differences.

```text
internal trades ↔ broker confirms
internal positions ↔ prime broker/custodian positions
internal cash ↔ bank/custodian cash
expected settlements ↔ depository/agent status
internal P&L ↔ administrator/accounting P&L
```

Do not implement reconciliation as a boolean equality check. Normalize identifiers,
units, sign conventions, time zones, and tolerances; match exact records first,
then controlled fuzzy/aggregate rules; preserve unmatched items as durable breaks.

Each break needs category, amount/exposure, age, owner, status, evidence, action,
and resolution reason. Metrics include new breaks, aged breaks, value at risk,
time-to-resolution, and recurring root causes.

## Ledger thinking

Financial movements should be append-only and balanced. Corrections use reversing
and replacement entries rather than deleting history. Use integer minor units or
an explicit decimal policy. A double-entry-style invariant is:

```text
for each journal event and currency: sum(debits and credits) = 0
```

Database constraints enforce local facts (unique event, valid currency, foreign
keys); application transaction logic enforces cross-row balance; reconciliation
checks the ledger against independent external truth.

## Time, cutoffs, and batches

Middle/back-office systems combine event-driven intraday updates with scheduled
processes: end-of-day books, margin cycles, settlement cutoffs, statements, and
regulatory deadlines. Store business date separately from timestamp, use explicit
market calendars/time zones, and make reruns idempotent by batch/run identity.

A missed cutoff can matter more than microsecond latency. Define service objectives
for completeness, freshness, correctness, and deadline success.

## Vendor data platforms

Vendor feeds require contract ownership: schema/version, delivery schedule,
entitlements, completeness, revision behavior, identifiers, licensing, fallback,
and escalation. Land immutable raw files/messages, validate and quarantine errors,
normalize into internal contracts, and publish lineage/quality status to consumers.

## Failure modes

- update current state but lose audit history;
- duplicate a fill or cash movement on retry;
- accept an unknown identifier mapping silently;
- use the wrong business date or settlement calendar;
- overwrite a correction instead of preserving versions;
- mark a batch complete before every item is durably processed;
- auto-resolve a reconciliation break without evidence;
- retry an ambiguous external instruction and create a duplicate side effect.

## Design drill

Design a settlement-break platform for one million trades per day. Cover trade and
instruction identity, lifecycle events, current-state projection, external status
ingestion, exact/fuzzy matching, exception ownership, aging/escalation, reruns,
audit, SQL schema, Kafka partition key, and reconciliation metrics.

## Answer frame

> Middle and back office technology turns executions into correct, legally and
> economically consistent books and completed obligations. I model each lifecycle
> dimension explicitly, preserve immutable history, make retries idempotent, use
> transactional ledgers and durable exceptions, and reconcile every projection
> against independent external truth.
