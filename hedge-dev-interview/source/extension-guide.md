# How to Add Another Role

The book separates reusable knowledge from employer-specific emphasis. Do not fork
the Python chapters for every firm.

## Directory contract

```text
core-python/       language and engineering fundamentals
systems/           performance, concurrency, real time
quant/             market, backtest, and data foundations
engineering/       production practices
interview/         active role pack (QRT in this edition)
templates/         reusable role intake template
code/              runnable evidence and labs
```

For multiple active roles, move employer pages to `roles/<firm-role>/` and add
each only once to `SUMMARY.md`.

## Extension workflow

1. Preserve the full job description and date/source.
2. Extract explicit responsibilities, required skills, preferred skills, domain,
   location, seniority, and operational expectations.
3. Map every signal to an existing competency/chapter.
4. Rank critical/high/medium/bonus using wording and role centrality.
5. Add only truly missing reusable concepts to core chapters.
6. Create role-specific positioning, questions, drills, and a final checklist.
7. Run link and code validation before publishing.

## Common overlays

- **Execution/low latency:** market microstructure, C++/native memory, networking,
  lock-free structures, hardware and tail-latency measurement.
- **Research platform:** pandas/NumPy, distributed compute, experiment tracking,
  point-in-time data, reproducibility, notebook-to-production workflows.
- **Data platform:** streaming/batch, temporal databases, lineage, quality, schema,
  partitioning, compaction, and access controls.
- **Risk platform:** pricing/exposure concepts, explainability, reconciliation,
  scenario calculations, controls and audit.
- **Quant researcher/developer:** statistics, optimization, signal evaluation,
  numerical methods, and stronger research methodology.

## Quality gate for a role pack

- Every claimed interview priority traces to the job description or is labeled an
  inference.
- No claim about a confidential/exact interview process is presented as fact.
- The three-day path has observable outputs, not reading-only tasks.
- Coding drills have edge cases and complexity expectations.
- Design drills include failure, recovery, measurement, and operations.
- Candidate positioning is honest about transferable versus direct experience.
- All internal links resolve and companion tests pass.
