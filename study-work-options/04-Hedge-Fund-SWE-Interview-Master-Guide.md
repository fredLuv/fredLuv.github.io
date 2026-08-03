# Hedge Fund SWE & Quant Dev Interview Master Guide

This master document outlines the technical preparation blueprint, Middle Office architecture, system design templates, and 2026 buy-side interview trends for **Citadel, Millennium, Jane Street, Man Group, Point72, and QRT**.

---

## 🏛️ 1. Middle Office Engineering Core Architecture

Middle Office Tech owns **Real-Time PnL, Intraday Risk Systems, Position Management, and Compliance/Limit Enforcement**.

### Key System Design Patterns:
1. **Real-Time PnL Engine (100,000 updates/sec)**:
   * **Partitioning**: Partition Kafka by `Portfolio_ID` for thread-local, lock-free state calculation (zero mutex contention).
   * **In-Memory Core**: Ring buffers and off-heap memory maps (`DirectByteBuffer`).
   * **PnL Math**:
     * *Realized PnL*: $\text{qty\_closed} \times (\text{fill\_price} - \text{avg\_cost})$
     * *Unrealized PnL (MtM)*: $\text{net\_qty} \times (\text{current\_market\_price} - \text{avg\_cost})$
   * **Storage Tiers**: L0 Ring Buffer $\rightarrow$ L1 Redis $\rightarrow$ L2 Apache Druid/ClickHouse $\rightarrow$ L3 Parquet/S3.
2. **Idempotency & Deduplication**:
   * Bloom Filter + LRU Deduplication Cache indexed by `Execution_ID` for exactly-once processing.

---

## 🔍 2. 2026 Buy-Side Interview Trends

```
[ Traditional Format ]                          [ 2026 Buy-Side Format ]
  - Pure LeetCode algorithm memorization   ──>    - Multi-file Codebase Debugging
  - Single 30-line function from scratch   ──>    - AI-Enabled Coding (Cursor / Copilot Allowed)
  - Theoretical Big-O complexity           ──>    - "Vibe Coding" Screening & Code Auditing
```

* **LeetCode Status**: Still used as automated filter (HackerRank OA), but whiteboard algorithm recall is replaced in live rounds.
* **Multi-File Codebase Debugging**: Candidate dropped into a 5-10 file codebase to locate concurrency deadlocks, memory leaks, or refactor p99 latency.
* **AI Tool Usage & Screening**: AI coding tools allowed in CoderPad, but interviewers screen heavily against "vibe coding"—candidates must defend memory barriers, thread safety, and data structure choices.

---

## 📅 3. Interview Timing & 4-Week Prep Roadmap

* **Timing**: **September is the peak hiring surge** in London & HK following August summer holidays.
* **Prep Schedule**:
  * **Week 1**: Real-Time Trading System Design & PnL Architecture.
  * **Week 2**: Low-Latency Java/C++, Concurrency & LMAX Disruptor Pattern.
  * **Week 3**: LeetCode Medium/Hard Patterns (Sliding Window, Monotonic Queue, Heap, LRU Cache).
  * **Week 4**: Mock Interviews & Behavioral/PM Pitch.

---
*Created on 2026-08-02 for fredLuv.github.io/study-work-options.*
