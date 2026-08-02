# Jump Trading — Middle / Back Office Software Engineer

This role pack is derived from the supplied **Jump Trading, Core Development —
Software Engineer, Middle / Back Office Technology (Python)** description. It is a
capability-based preparation plan, not a claim about Jump's exact interview loop.

## Role thesis

Jump is hiring a software engineer to build critical transactional infrastructure
around risk and clearing, post-trade automation, vendor data, and workflows across
business teams. The strongest candidate combines production Python/Java judgment
with relational data correctness, Kafka, domain learning, precise requirements,
and reliable independent delivery.

This is not primarily an alpha-research or exchange hot-path role. Low-latency
knowledge helps, but over-indexing on lock-free algorithms while neglecting SQL,
reconciliation, and settlement correctness would misread the posting.

## Posting-to-competency map

| Posting signal | Interview evidence | Core material | Priority |
|---|---|---|---|
| 3+ years Python, Java, or C++ | readable coding, testing, production ownership | Chapters 1–5 | Critical |
| SQL databases | schema, joins/windows, isolation, indexes, query plans | Chapter 14 | Critical |
| Kafka/messaging | keys, ordering, offsets, replay, idempotency, outbox | Chapter 15 | Critical |
| Data architecture and software design | domain model, constraints, lifecycle history, contracts | Chapters 4, 11–15 | Critical |
| Risk, clearing, locates, settlement | accurate lifecycle vocabulary and invariants | Chapter 12 | High-plus |
| Interdepartmental workflows | requirements, exception ownership, audit, usability | This pack + behavioral | High |
| Post-trade automation/vendor data | idempotent batches, validation, lineage, reconciliation | Chapters 11–15 | High |
| Attention to detail | boundary tests, tie-breakers, money/time/identity policy | Throughout | High |
| Independent contributor/team dynamic | scoped ownership plus early risk communication | Behavioral | High |
| Reliable, predictable availability | operational ownership without heroics | Behavioral | High |

## Positioning for a Java-first engineer

> I bring mature Java experience building reliable event-driven and transactional
> systems, and I have translated those habits into typed, testable Python. For this
> role I focus on the invariants that middle/back-office infrastructure lives or dies
> by: stable identity, relational constraints, transaction boundaries, idempotent
> Kafka consumers, durable workflow state, reconciliation, and observable exception
> handling. I am comfortable turning ambiguous business processes into explicit
> contracts with users and owning them predictably in production.

Use only evidence you can defend. If direct settlement/clearing experience is
limited, say so and demonstrate the domain model, SQL/outbox lab, and a comparable
workflow you learned quickly.

## QRT versus Jump: change the emphasis

| Dimension | QRT Quant Developer | Jump Middle / Back Office |
|---|---|---|
| Primary outcome | research/trading framework and strategy support | correct post-trade, risk, clearing, and data workflows |
| Python depth | critical | critical |
| Real-time/performance | high | useful, usually secondary to transactional correctness |
| Backtesting | critical | not central unless the team says otherwise |
| Relational SQL | important | critical |
| Kafka/messaging | helpful/high | explicitly critical |
| Domain | electronic trading and quant platform | risk, clearing, locates, settlement, reconciliation |
| Stakeholders | traders and quants | operations, risk, finance, clearing, vendors, engineering |
| Failure lens | stale signals, latency, trading/risk faults | broken books, missed cutoff, duplicate/missing obligation, unresolved break |

## Jump-focused three-day overlay

Use the shared schedule, but replace QRT-only blocks as follows.

### Day 1 — Python plus SQL foundations

- Chapters 1–5: Python object model, typing, exceptions, testing.
- Chapter 14 through transactions: model trades, settlement, and event identity.
- Write four queries: net position, latest status, aged breaks, duplicate detection.
- Run the SQLite ledger/outbox tests in the companion lab.

**Proof:** explain one schema and one concurrent update invariant without notes.

### Day 2 — Kafka plus post-trade domain

- Chapter 12: trace one trade from execution through settlement/reconciliation.
- Chapter 15: partitioning, offset commit, duplicates, rebalances, outbox.
- Design the execution-to-settlement pipeline below.
- Rehearse how a timeout/duplicate/amendment changes state.

**Proof:** explain why “Kafka exactly once” does not make a SQL side effect exactly
once and show the schema constraint that closes the gap.

### Day 3 — Production and business partnership

- Chapter 13: deployment, observability, incident response, schema migration.
- SQL query plan/index drill and one Python coding question.
- Prepare six behavioral stories, including business requirements and availability.
- Run the Jump mock loop and repair the two weakest answers.

**Proof:** deliver a 35-minute design and a two-minute incident/business story.

## Likely capability prompts

### Python

- Model trade lifecycle events and current state with dataclasses/enums.
- Deduplicate a stream while rejecting conflicting duplicate IDs.
- Merge or group ordered records under memory constraints.
- Build a context-managed transaction/retry boundary.
- Explain generators, mutability, hashing, typing, async versus threads, and tests.

### SQL and data modeling

- Design trade, allocation, clearing, settlement, locate, and break tables.
- Write latest-row-per-trade and net-exposure queries.
- Explain primary/business keys, constraints, normalization, and history.
- Prevent two workers from consuming the same locate availability.
- Diagnose a slow break report using its query plan.
- Choose an isolation level and retry/locking policy from an explicit anomaly.

### Kafka

- Choose a partition key for lifecycle ordering and discuss hot keys.
- Explain offsets, groups, rebalances, lag, retention, and replay.
- Design database-to-Kafka consistency using an outbox.
- Make a Kafka-to-database consumer idempotent.
- Handle poison records without silently skipping financial state.
- Evolve a schema while old/new producers and consumers coexist.

### Domain and design

- What is the difference between execution, clearing, and settlement?
- What does a locate protect, and what is the concurrency invariant?
- Design a reconciliation workflow, not only a comparison query.
- Handle a late trade amendment after clearing or settlement instruction.
- Define completeness/freshness SLOs around a market or settlement cutoff.

## System-design drill: execution to settlement

Design for one million executions/day with 10× intraday bursts and several vendors.
The system must capture/amend trades, enrich instruments/accounts, allocate,
calculate intraday positions, instruct clearing/settlement, ingest external statuses,
and manage reconciliation breaks.

Your answer must include:

1. trade/event identity and versioning;
2. SQL tables, constraints, history, and current projections;
3. Kafka topics, schemas, keys, consumer groups, and retention;
4. transactional outbox and processed-event dedupe;
5. late/out-of-order amendments and cancel/correct flows;
6. vendor validation/quarantine and lineage;
7. reconciliation matching, exception ownership, aging, and replay;
8. cutoffs, business calendars, SLOs, alerting, and recovery;
9. permissions, audit, and sensitive-data handling;
10. a compatible schema/deployment migration.

Pressure questions:

- The database commit succeeded but Kafka timed out. What is the state?
- One trade update is poison and blocks its partition. What do you do?
- A vendor sends the same event ID with a different amount.
- A settlement update arrives before its trade amendment.
- Consumer lag is zero, but positions are wrong. What did monitoring miss?
- A batch says complete but one partition was never assigned.

## SQL drill schema

Sketch queries against:

```text
trade(trade_id, account_id, symbol, business_date, quantity, price, currency, version)
trade_status(trade_id, status, observed_at, source_sequence)
settlement(trade_id, expected_date, actual_date, status, failure_reason)
processed_event(consumer_name, event_id, payload_hash, processed_at)
outbox(event_id, topic, event_key, payload, created_at, published_at)
```

Tasks:

1. return the latest status known as of a timestamp;
2. aggregate net quantity and signed notional by account/symbol;
3. find failed/late settlements ordered by exposure and age;
4. propose indexes and validate them with `EXPLAIN`;
5. atomically apply one event and create its outbox record;
6. explain how a duplicate and a conflicting duplicate behave.

## Behavioral story bank

Prepare six SCARL stories:

1. **Requirements:** turned a user's manual or ambiguous workflow into explicit
   states, rules, and acceptance checks.
2. **Detail:** caught a small identity/time/money assumption before it became a
   large production issue.
3. **Reliability:** supported a critical deadline or incident predictably, without
   relying on uncommunicated heroics.
4. **Independence:** owned a problem end to end while surfacing risk early.
5. **Collaboration:** resolved a disagreement across engineering and business teams.
6. **Learning:** entered an unfamiliar domain, found authoritative sources/users,
   and shipped a correct result.

For “reliable and predictable availability,” describe on-call/coverage agreements,
runbooks, early escalation, handoffs, and automation. Do not promise permanent
personal availability; demonstrate a reliable operating system.

## Questions for the interviewers

- Which workflows are most in need of modernization: risk, clearing, locates,
  settlement, reconciliation, or vendor data?
- Where are the current sources of truth, and which reconciliation breaks consume
  the most human time?
- How are Python services, SQL databases, and Kafka responsibilities divided?
- What processing deadlines or market cutoffs define reliability for the team?
- How closely do engineers work with operations, risk, finance, and vendors?
- What does independent ownership look like during the first six months?
- How are schema and event-contract changes reviewed across departments?

## Jump mock loop (75 minutes)

- 0–10: introduction and why middle/back-office technology.
- 10–30: Python coding—deduplicate/apply trade lifecycle events.
- 30–45: SQL—latest status plus indexes/concurrency follow-ups.
- 45–62: Kafka/SQL outbox and failure semantics.
- 62–70: requirements or reliability behavioral story.
- 70–75: candidate questions and concise summary.

Score 0–2 on correctness, Python clarity, relational modeling, SQL, Kafka semantics,
domain reasoning, production failure handling, and communication. Target 12/16.

## Final answer frame

> This role optimizes correctness and business throughput across a long-lived trade
> lifecycle. I would make identity and state explicit, enforce invariants in SQL,
> preserve immutable history, connect services through keyed Kafka events and an
> outbox, make every consumer idempotent, and operate the workflows through
> reconciliation, exception ownership, deadline SLOs, and close user feedback.
