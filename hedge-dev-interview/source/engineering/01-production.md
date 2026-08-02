# 13. Architecture, CI/CD, and Operations

## Interview outcome

Explain how a quant platform moves safely from change to production and how you
would support it when money and users depend on it.

## Architecture principles that earn trust

- Keep domain policy independent from brokers, databases, and schedulers.
- Make time, randomness, configuration, and external I/O injectable.
- Use immutable events and explicit state transitions.
- Prefer a modular monolith until independent scaling, ownership, or failure
  isolation justifies a service boundary.
- Treat schemas and operational behavior as public contracts.
- Record enough input and version metadata for replay and audit.

Microservices are not a synonym for clean architecture. They add network failure,
distributed tracing, deployment coordination, and eventual consistency.

## A production path

```text
format/lint/type → unit/property → component → replay/regression → package once
       → security/license scan → staging/shadow → canary → promote → observe
```

Promote the same immutable artifact. Do not rebuild between environments. Pin
dependencies and record the artifact, code, schema, config, and data/model version.

## Deployment patterns

- **Rolling:** simple, but old/new versions coexist; requires compatibility.
- **Blue/green:** fast switch/rollback; doubles capacity and needs state planning.
- **Canary:** limits blast radius; requires meaningful automated health comparison.
- **Shadow:** sends copied inputs without authoritative side effects; ideal for
  output and latency comparison, but must prevent accidental trading.

For a strategy or risk change, use replay plus shadow, explicit position/risk
limits, a small canary allocation, and a tested kill/rollback path.

## Schema evolution

Use expand-and-contract:

1. add compatible fields/representation;
2. deploy readers that tolerate both;
3. dual-write or translate if needed;
4. backfill and reconcile;
5. switch reads and monitor;
6. remove the old form only after all consumers are proven migrated.

Never coordinate a “flag day” across many producers and consumers if compatibility
can remove the risk.

## Incident response

1. Detect and state user/trading impact.
2. Stabilize: halt, isolate, degrade, or roll back within known controls.
3. Preserve evidence: logs, metrics, events, versions, configuration, timelines.
4. Form and test hypotheses; distinguish correlation from cause.
5. Recover and reconcile external truth.
6. Prevent recurrence with a system/control improvement, not only “be careful.”

Communicate known facts, unknowns, next action, owner, and next update time. In a
trading incident, correctness and exposure usually outrank availability.

## Observability and SLOs

Define service-level indicators close to business outcomes:

- valid market-data freshness and gap rate;
- end-to-end decision/order latency percentiles;
- order acknowledgement/reject/error rate;
- queue utilization and dropped/coalesced counts by declared policy;
- position/cash reconciliation mismatch;
- strategy heartbeat, stale input gate, and risk-limit utilization.

A green CPU graph does not prove a healthy trading system.

## Security and controls

- least-privilege service identities and short-lived credentials;
- secrets outside source and logs;
- authenticated, authorized control actions;
- append-only audit trail for orders, risk/config changes, and deploys;
- separation of duties for sensitive production changes;
- dependency/image scanning and controlled artifact provenance.

## Drill

A new pricing library passes unit tests but changes 0.3% of historical signals.
Design the promotion plan: golden/replay comparison, tolerance classification,
explainable diffs, shadow outputs, canary limits, dashboards, rollback trigger,
and who approves semantic changes.

## Answer frame

> I package once, prove the change at increasing levels of realism, and promote
> the same artifact. Compatibility is designed with expand-and-contract. Runtime
> safety comes from business-level telemetry, bounded rollout, independent risk
> controls, reconciliation, and a rollback or kill path that is tested before use.
