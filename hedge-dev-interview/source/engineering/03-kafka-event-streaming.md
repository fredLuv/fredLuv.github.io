# 15. Kafka and Durable Event Pipelines

## Interview outcome

Design a Kafka pipeline with deliberate topic boundaries, keys, ordering,
delivery semantics, schema evolution, offset handling, backpressure, replay, and
database consistency. Explain what Kafka guarantees—and what the application must.

## Mental model

```text
producer → topic partition 0: [record offset 0, 1, 2, ...]
          topic partition 1: [record offset 0, 1, 2, ...]
                         ↓
        consumer group: one active consumer per partition
```

- A **topic** is a named durable stream.
- A **record** has key, value, headers, timestamp, topic, partition, and offset.
- A **partition** is the unit of ordered storage and consumer parallelism.
- An **offset** is a position within one partition, not a global event ID.
- A **consumer group** is one logical subscriber; each partition is assigned to at
  most one active consumer in that group at a time.

Ordering is guaranteed within a partition, not across a topic. The record key and
partitioning strategy therefore encode a domain correctness decision.

## Choose the key from the invariant

Examples:

- `trade_id` keeps all lifecycle updates for one trade ordered;
- `account_id` keeps account-level ledger changes ordered but can create hot keys;
- `instrument_id` helps build ordered market state per instrument;
- no key spreads load but gives no same-entity ordering guarantee.

If a portfolio calculation needs many accounts/partitions, it must tolerate and
define cross-partition timing. Adding partitions can change key-to-partition mapping
under common partitioners, so do not casually rely on a permanent numeric partition.

## Topic and event contract

Use domain events, not database-row-change trivia, at business boundaries:

```json
{
  "event_id": "01J...",
  "event_type": "SettlementFailed",
  "schema_version": 3,
  "trade_id": "T-1042",
  "effective_at": "2026-08-02T15:00:00Z",
  "observed_at": "2026-08-02T15:00:02Z",
  "source": "custodian-x",
  "reason_code": "INSUFFICIENT_SECURITIES"
}
```

The event ID supports deduplication; type and version support evolution; two clocks
separate business occurrence from observation; source and reason support audit.

Topic design considers ownership, retention, sensitivity, throughput, ordering,
replay use, and failure policy. Do not create one topic per customer/trade or put
unrelated data behind one vague `events` topic.

## Delivery semantics without slogans

### At most once

Commit/advance position before side effects. A crash can lose work, but duplicates
are unlikely. Appropriate only when loss is acceptable, such as replaceable metrics.

### At least once

Perform the side effect, then commit the offset. A crash between them replays the
record. This is the common robust default when the side effect is idempotent.

### Exactly once

Kafka producer idempotence and transactions can give strong guarantees for a
Kafka-read → Kafka-write pipeline when configured and consumed correctly. They do
not automatically make an external SQL write, email, payment, or broker instruction
exactly once. End-to-end safety still needs stable identity, transactional boundaries,
deduplication, and reconciliation.

## Consumer processing pattern

```text
poll bounded batch
  → validate schema and business invariants
  → begin database transaction
      → insert processed_event unique key
      → apply state/ledger changes
      → insert outbound outbox rows
    commit database
  → commit Kafka offsets
```

If the process crashes after the database commit but before the offset commit, the
record returns. The unique processed-event key turns it into a safe no-op and can
detect the same ID with a conflicting payload.

Do not commit offsets for work that is only queued in volatile memory. Keep poll
and processing timing compatible with consumer liveness settings, or separate
polling from bounded workers while preserving partition order and commit safety.

## Rebalances

Consumers rebalance when group membership or subscriptions change. Partition
ownership moves, so a consumer must stop/finish or safely abandon in-flight work,
commit only completed contiguous offsets, and initialize state for new partitions.

Long pauses, slow processing, deployment churn, and autoscaling can produce
rebalance storms. Measure rebalance count/duration and use cooperative/sticky
assignment features supported by the deployed client/version when appropriate.

## Retries, poison records, and ordering

Immediate infinite retry blocks a partition. Blindly skipping a failure corrupts
state. Classify:

- transient dependency failure → bounded retry with jitter/deadline;
- deterministic bad payload → quarantine/dead-letter with full evidence;
- business rejection → durable rejection event/workflow;
- unknown bug → stop or quarantine according to data criticality and page an owner.

Retry topics delay work but can reorder events for one key. If order matters, keep
the partition blocked, route the entire key to a controlled repair flow, or design
events/state application to tolerate out-of-order versions.

A dead-letter queue is not disposal. It needs ownership, alerting, replay tooling,
retention, access controls, and a resolution audit.

## Schema evolution

Prefer additive compatible changes:

- consumers ignore unknown fields;
- producers supply defaults/optional fields where semantics allow;
- never reuse a field name/number for a new meaning;
- introduce a new event type when semantics fundamentally change;
- validate compatibility in CI against registered schemas and representative events;
- deploy tolerant consumers before producers emit the new form.

Keep transport compatibility separate from business compatibility. A field can be
syntactically optional while its absence makes a consumer's decision unsafe.

## Retention, replay, and compaction

Retention is time/size policy independent of consumption. Consumers may reset
offsets to replay retained history. Compaction retains the latest record per key
eventually and is useful for reconstructible current-state topics, but tombstones,
lag, and compaction timing must be understood.

Kafka is a durable log, not a general relational query engine. Build materialized
views/databases for operational queries and make them reconstructible where useful.

## Capacity and observability

Partition count caps active consumer parallelism per group and affects metadata,
files, recovery, and ordering. Size using peak records/sec, bytes/sec, record size,
retention, replication, consumer service time, and headroom.

Measure:

- produce error/rate/latency and acknowledgement failures;
- consumer lag in offsets **and time/freshness**;
- processing latency, batch size, poll interval, and queue depth;
- rebalances, assignment, commit errors, retries, quarantines;
- under-replicated/offline partitions and broker storage/network saturation;
- end-to-end event time → durable business-state time.

Zero offset lag does not prove correct processing if the consumer committed too
early or produced corrupt state.

## Security and controls

Use encryption in transit, authenticated principals, least-privilege topic/group
ACLs, secrets management, audit logs, and data classification/retention controls.
Separate production write access from read/replay tooling. Redact personal,
credential, and sensitive trading data from logs and non-production topics.

## Database plus Kafka: outbox and CDC

Write business state and an outbox event in one SQL transaction. A publisher or
change-data-capture process sends committed outbox rows to Kafka. Marking published
can race with acknowledgement, so producer idempotence and event-ID deduplication
remain useful. The outbox should have status/attempt/created timestamps, indexes for
pending scans, bounded retention, and lag alerts.

The inverse, consuming Kafka and updating SQL, uses a processed-event unique key in
the same transaction as the business write. Together these patterns avoid the
uncoordinated dual-write gap without pretending two systems share one simple ACID
transaction.

## Design drill

Design a post-trade pipeline that receives execution events, enriches reference
data, persists trades, calculates intraday positions, sends clearing instructions,
and tracks settlement status. Cover topics, schemas, partition keys, SQL/outbox
boundaries, consumer groups, duplicate/conflicting events, late amendments,
rebalances, retries, poison records, replay, access control, and business-level SLOs.

## Answer frame

> Kafka gives me durable partitioned logs, per-partition ordering, replay, and
> consumer-group parallelism. I choose keys from domain ordering, use at-least-once
> processing with database-enforced idempotency, bridge SQL with an outbox, evolve
> schemas compatibly, and treat lag, rebalances, poison events, and reconciliation
> as production behavior—not edge cases.
