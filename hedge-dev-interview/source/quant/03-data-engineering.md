# 11. Time-Series Data Engineering

## Interview outcome

Design data that is point-in-time correct, discoverable, reproducible, and safe to
evolve across research and production.

## Data has more than one time

For a fundamental or reference-data record, distinguish:

- `effective_at`: when the fact applies in the business world;
- `published_at`: when the source released it;
- `ingested_at`: when your platform observed it;
- `valid_from` / `valid_to`: when a particular version was considered valid.

A backtest query usually asks: “What was the latest value **known by** decision
time?” Joining only on effective date can leak later revisions.

## Point-in-time join

For each decision `(instrument, t)`, select the eligible record for that instrument
with `published_at <= t` (and often `ingested_at <= t`), then the latest version
under the dataset's revision policy. Make the policy testable and visible.

## Raw, normalized, curated

```text
immutable raw → validated normalized → research/live curated views
        │                 │                         │
  source fidelity   stable schema/IDs       purpose-specific features
```

- Raw enables reprocessing and audit.
- Normalized standardizes identifiers, timestamps, units, and quality flags.
- Curated data serves a defined use case and can be regenerated from upstream
  lineage.

## Data contracts

Specify field type, unit/currency, nullability, time semantics, uniqueness key,
ordering, allowed lateness, revision behavior, retention, and compatibility rules.
Validate ranges and relationships, not just types: bid ≤ ask, nonnegative sizes,
monotonic source sequence within a session, known instrument, finite values.

## Missing is not zero

Classify absence: not applicable, not observed, late, source outage, filtered,
invalid, or genuinely zero. Imputation is a modeling decision with an availability
timestamp. Preserve a missingness/quality indicator where it affects meaning.

## Storage trade-offs

- partition by common pruning keys, but avoid millions of tiny partitions/files;
- columnar formats suit analytical scans; row/event stores suit keyed updates and
  ordered logs;
- compression, sorting, and clustering must reflect query patterns;
- compaction and retention are operational features, not afterthoughts;
- schema evolution should be additive and backward compatible before removal.

## Research-production consistency

Publish versioned transformations rather than copy-pasted notebooks. A feature
definition should record code version, source versions, parameters, time semantics,
and quality checks. Online and offline implementations need parity tests using the
same golden events.

## Drill

An earnings value effective March 31 was first published April 20 and revised May
5. A strategy trades April 25. Which version may it use? Design columns and a query
that answers correctly, including the case where your platform did not ingest the
April 20 release until April 26.

Expected: the April 25 decision cannot use the May 5 revision. If the system did
not observe the first release until April 26 and the contract uses system knowledge,
it cannot use that value either.

## Answer frame

> I model both business time and knowledge time. Raw data is immutable, normalized
> data has stable identifiers and contracts, and curated views are reproducible.
> Point-in-time joins use what was published and observed by the decision time,
> with revisions, missingness, lineage, and quality flags preserved.
