# 14. Relational Databases and SQL

## Interview outcome

Model a post-trade workflow with keys and constraints, write production-grade SQL,
reason about isolation and locking, diagnose a query plan, and explain how the
database and Kafka remain consistent.

## The Java-to-relational bridge

An object graph optimizes navigation in one process. A relational model optimizes
shared facts, integrity, set operations, concurrent transactions, and multiple
access paths. Do not map every class hierarchy mechanically into tables.

Start with business identity and invariants:

```sql
CREATE TABLE trade (
    trade_id        TEXT PRIMARY KEY,
    execution_id    TEXT NOT NULL,
    execution_venue TEXT NOT NULL,
    account_id      TEXT NOT NULL,
    symbol          TEXT NOT NULL,
    trade_time      TIMESTAMPTZ NOT NULL,
    business_date   DATE NOT NULL,
    quantity        NUMERIC(24, 8) NOT NULL CHECK (quantity <> 0),
    price           NUMERIC(24, 10) NOT NULL CHECK (price > 0),
    currency        CHAR(3) NOT NULL,
    version         INTEGER NOT NULL CHECK (version > 0),
    UNIQUE (execution_venue, execution_id, version)
);
```

The primary key supplies internal identity. The namespaced unique key prevents a
duplicated external execution/version. `NOT NULL`, `CHECK`, `UNIQUE`, and foreign
keys make invalid local states unrepresentable even if one application path fails.

## Normalize facts; denormalize deliberately

Third normal form is a useful default: each fact has one authoritative location
and non-key attributes depend on the key. This limits contradictory updates.

Denormalize only for a measured read pattern, with a named source of truth and a
repair/rebuild path. A current-state projection may duplicate the latest status
from an immutable event history; that is deliberate because the history remains
authoritative and the projection is reconstructible.

## Keys and history

- Use surrogate internal IDs when external identity is composite, mutable, or
  vendor-scoped, but preserve a unique business key.
- Do not use timestamps alone as identity.
- Use optimistic version columns to detect lost updates.
- Represent amendments as versions/events; do not silently overwrite audit fields.
- For temporal data, distinguish effective time from system/knowledge time.

## SQL operations you should write fluently

Given `trade`, `trade_status_history`, and `settlement`:

### Aggregate exposure

```sql
SELECT account_id,
       symbol,
       SUM(quantity) AS net_quantity,
       SUM(quantity * price) AS signed_notional
FROM trade
WHERE business_date = :business_date
GROUP BY account_id, symbol
HAVING SUM(quantity) <> 0;
```

Use bound parameters, never string concatenation. Define whether quantity is signed
and whether notional needs FX conversion or an absolute/gross measure.

### Latest status per trade

```sql
WITH ranked AS (
    SELECT trade_id,
           status,
           observed_at,
           ROW_NUMBER() OVER (
               PARTITION BY trade_id
               ORDER BY observed_at DESC, source_sequence DESC
           ) AS position
    FROM trade_status_history
    WHERE observed_at <= :as_of
)
SELECT trade_id, status, observed_at
FROM ranked
WHERE position = 1;
```

The deterministic tie-breaker matters. `MAX(observed_at)` alone does not return
the other columns from the same row and can duplicate ties.

### Find aged settlement breaks

```sql
SELECT t.trade_id,
       t.account_id,
       s.expected_date,
       :business_date - s.expected_date AS days_late,
       ABS(t.quantity * t.price) AS exposure
FROM settlement AS s
JOIN trade AS t USING (trade_id)
WHERE s.status IN ('PENDING', 'FAILED')
  AND s.expected_date < :business_date
ORDER BY exposure DESC, s.expected_date, t.trade_id;
```

Clarify calendar days versus business days. Real settlement aging often requires a
calendar table rather than date subtraction.

## Transactions and isolation

ACID is not a spell; state the invariant and anomaly you are preventing.

- **Atomicity:** every change in the unit commits or none does.
- **Consistency:** committed state satisfies declared invariants.
- **Isolation:** concurrent work has defined visibility/serialization behavior.
- **Durability:** acknowledged commits survive the database's stated failure model.

At Read Committed, two statements in one transaction can see different committed
snapshots. Repeatable Read provides a stable transaction snapshot but can still
require retries. Serializable prevents serialization anomalies by aborting a
conflicting transaction; the application must retry the complete transaction.

### Prevent double consumption of a locate

```sql
BEGIN;

SELECT available_quantity
FROM locate
WHERE locate_id = :locate_id
FOR UPDATE;

UPDATE locate
SET available_quantity = available_quantity - :requested
WHERE locate_id = :locate_id
  AND available_quantity >= :requested;

-- Require exactly one updated row, then insert the allocation.
COMMIT;
```

The conditional update protects the invariant. `FOR UPDATE` can make the workflow
and error reporting clearer but increases blocking; consistent lock order reduces
deadlocks. Treat deadlock/serialization errors as bounded whole-transaction retries,
not a retry of only the last statement.

## Idempotency in the schema

Put the idempotency boundary in a unique constraint:

```sql
CREATE TABLE processed_event (
    consumer_name TEXT NOT NULL,
    event_id      TEXT NOT NULL,
    payload_hash  TEXT NOT NULL,
    processed_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (consumer_name, event_id)
);
```

An identical duplicate becomes a no-op. The same ID with a different payload is a
data-integrity incident, not another retry.

## Index design

An index trades read speed for write, storage, vacuum/maintenance, and cache cost.
Design it from a query:

```sql
CREATE INDEX settlement_open_by_date
ON settlement (expected_date, trade_id)
WHERE status IN ('PENDING', 'FAILED');
```

This partial index matches the aged-break predicate. For a composite B-tree index,
leading columns matter. Equality columns typically precede range/order columns,
but verify with the actual planner and data distribution.

Avoid:

- indexing every column;
- wrapping indexed columns in functions without a matching expression index;
- leading-wildcard search and implicit type casts on hot paths;
- fetching wide rows when only a few columns are needed;
- assuming an index will help a query returning most of a table.

## Read `EXPLAIN` as evidence

Use `EXPLAIN (ANALYZE, BUFFERS)` in a safe representative environment. Compare
estimated versus actual rows, scan type, join algorithm/order, loops, sort spill,
buffer hits/reads, and total time. Large row-estimate errors point to statistics,
correlation, or predicate-model problems. `ANALYZE` executes the query—do not run it
carelessly on a mutating production statement.

## Schema evolution

Use expand-and-contract:

1. add nullable/compatible structure;
2. deploy readers tolerant of old and new;
3. dual-write or backfill in bounded chunks;
4. validate counts/checksums and lag;
5. switch reads;
6. enforce stronger constraints and remove the old path later.

Avoid a long blocking table rewrite or index build during a critical processing
window. Know the online/concurrent DDL behavior of the actual database/version.

## Python database hygiene

- Use parameter binding and explicit transactions/context managers.
- Keep transactions short; never wait for a user or remote service while holding
  locks.
- Bound the connection pool below database capacity and measure queue wait.
- Stream/batch large results rather than `fetchall()` by default.
- Map rows into validated domain types at the boundary.
- Include SQLSTATE/error category, query name, duration, rows, and correlation ID
  in observability—never secrets or raw sensitive payloads.

## Database-to-Kafka consistency: transactional outbox

A database commit followed by a Kafka publish can fail between the two steps. A
publish followed by a database commit has the inverse failure. Write domain state
and an outbox row in one database transaction, then let a separate publisher send
the outbox record to Kafka and mark it published. Consumers still deduplicate:
publication and acknowledgement can be ambiguous.

## Drills

1. Model trades, allocations, settlement instructions, lifecycle history, and
   reconciliation breaks with keys and constraints.
2. Write a point-in-time latest-status query and explain its tie-breaker.
3. Diagnose why `WHERE DATE(trade_time) = :day` may miss an index; rewrite it as a
   half-open timestamp range.
4. Design a transaction that applies a cash journal and outbox event exactly once
   per source event.

## Answer frame

> I begin with business identity and invariants, enforce local integrity with
> relational constraints, and choose isolation/locking from the concurrency anomaly
> I must prevent. I design indexes from measured query plans, keep transactions
> short and retryable, evolve schemas compatibly, and use an outbox plus idempotent
> consumers across the database/Kafka boundary.
