# Three Mock Interview Loops

Record yourself. Use a blank editor and no autocomplete for coding if the real
format is unknown. Each loop has a scorecard; do not grade on vibes.

## Mock 1 — Python depth and coding (60 minutes)

- 0–5: 90-second introduction.
- 5–15: `is`/`==`, hashability, mutable defaults, generator behavior.
- 15–45: P2 merge event streams or P7 bounded async mapper.
- 45–55: tests, complexity, memory, malformed/late input.
- 55–60: one question for the interviewer.

Score 0–2: clarification, correctness, idiomatic Python, tests/edge cases,
complexity, explanation. Target 9/12.

## Mock 2 — System design (60 minutes)

- 0–5: requirements for Drill B or C.
- 5–15: events, invariants, scale, success and failure semantics.
- 15–35: architecture, state, partitioning, main flow.
- 35–50: overload, ordering, recovery, idempotency, operations.
- 50–55: alternatives and evolution.
- 55–60: concise summary.

Score the eight items in the system-design chapter. Target 12/16.

## Mock 3 — Hiring manager and production (60 minutes)

- 0–10: introduction and role motivation.
- 10–22: system ownership story.
- 22–34: incident story with technical drill-down.
- 34–44: disagreement/ambiguous stakeholder story.
- 44–52: Python transition challenge and evidence.
- 52–60: candidate questions.

Score 0–2: concise structure, personal ownership, technical depth, quantified
result, honest self-correction, role connection. Target 9/12.

## Repair loop

For every lost point:

1. write the exact weak moment;
2. classify knowledge, retrieval, coding, structure, or communication;
3. do the smallest targeted repair;
4. repeat only that segment from a blank start;
5. rerun the full loop later, not immediately.

## Interview-day operating rules

- Clarify before coding/designing, but keep momentum.
- State invariants and choose one concrete path; mention alternatives afterward.
- Test with normal, boundary, empty, invalid, and duplicate/out-of-order cases.
- If you do not know, state what you know, what is uncertain, and how you would
  verify. Do not improvise false internals.
- End with a summary that connects decisions to the role's reliability and
  collaboration needs.
