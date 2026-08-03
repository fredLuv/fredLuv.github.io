# Hedge Fund SWE & Quant Dev Interview Master Guide (London & HK Buy-Side)

This master textbook outlines the exhaustive technical preparation blueprint, Middle Office architecture, low-latency concurrency principles, system design templates, domain fundamentals, and 2026 buy-side interview trends for **Citadel Europe, Millennium, Jane Street, Man Group, Point72, QRT, Optiver, and Balyasny**.

---

# TABLE OF CONTENTS
1. [Middle Office Core Engineering Architecture](#1-middle-office-core-engineering-architecture)
2. [Low-Latency Systems, Concurrency & JVM Internals](#2-low-latency-systems-concurrency--jvm-internals)
3. [2026 Buy-Side Interview Trends & Evaluation Rubric](#3-2026-buy-side-interview-trends--evaluation-rubric)
4. [Financial Domain & Trade Lifecycle Fundamentals](#4-financial-domain--trade-lifecycle-fundamentals)
5. [The 4-Week August Sprint Roadmap](#5-the-4-week-august-sprint-roadmap)

---

# 1. MIDDLE OFFICE CORE ENGINEERING ARCHITECTURE

Middle Office Technology sits directly between Front Office Execution (OEMS/Trading Desks) and Back Office Accounting. It owns **Real-Time PnL, Intraday Risk Engines, Position Management, and Compliance/Limit Enforcement**.

```
[ Exchanges / OEMS ]               [ Market Data Feed Handlers ]
         |                                     |
         v (Execution Fills)                   v (Price Ticks)
   +-------------------------------------------------+
   |      Kafka Event Bus (Partitioned by Portfolio) |
   +-------------------------------------------------+
                            |
                            v
   +-------------------------------------------------+
   |    Stateful PnL Stream Processor Cluster        |
   |    (C++ / Java Flink with In-Memory RocksDB)    |
   +-------------------------------------------------+
          /                 |                 \
         v                  v                  v
  [L0 In-Memory Cache] [Redis Cluster]   [Apache Druid / ClickHouse]
         |                  |                  |
         v                  v                  v
  (Trading Desk UI)    (Risk Alerts API)  (EOD Audit & Historical)
```

---

### System Design 1: Real-Time PnL Aggregator (100,000 updates/sec)

#### A. Scale & Performance Targets
* **Execution Fills**: 100,000 msg/sec
* **Market Price Ticks**: 500,000 msg/sec
* **Throughput**: 120 MB/sec (960 Mbps)
* **Latency Budget**: Processing to UI update <= 20 ms (p99).

#### B. Threading & Lock-Free Partitioning Strategy
* **Partition Kafka by `Portfolio_ID`**: All trades and order updates for a given portfolio land on the **same Kafka partition** and are consumed by the **same dedicated worker thread**.
* **Result**: Enables **thread-local, lock-free state updates**. Zero mutex locking required across worker threads.

#### C. In-Memory Position State
```cpp
struct PositionState {
    int64_t portfolio_id;
    char    symbol[12];
    int64_t net_quantity;         // Positive = Long, Negative = Short
    double  avg_cost_basis;       // Weighted average entry price
    double  realized_pnl;         // Locked-in PnL from closed trades
    double  last_market_price;    // Latest market tick price
    uint64_t last_update_time_ns; // Nanosecond timestamp
};
```

#### D. PnL Mathematics

1. **When an Execution Fill Arrives (`FillQty`, `FillPrice`)**:
   * **Increasing Position** (Same sign, e.g., Long 100 -> Buy 50):

$$\text{NewAvgCost} = \frac{(\text{NetQty} \times \text{AvgCost}) + (\text{FillQty} \times \text{FillPrice})}{\text{NetQty} + \text{FillQty}}$$

$$\text{NetQty} = \text{NetQty} + \text{FillQty}$$

   * **Closing/Reducing Position** (Opposite sign, e.g., Long 100 -> Sell 40):

$$\text{QtyClosed} = \min(|\text{NetQty}|, |\text{FillQty}|)$$

$$\text{RealizedPnL} = \text{RealizedPnL} + (\text{QtyClosed} \times (\text{FillPrice} - \text{AvgCost}))$$

$$\text{NetQty} = \text{NetQty} + \text{FillQty}$$

2. **When a Market Price Tick Arrives (`CurrentPrice`)**:
   * **Unrealized PnL Calculation**:

$$\text{UnrealizedPnL} = \text{NetQty} \times (\text{CurrentPrice} - \text{AvgCost})$$

   * **Total PnL**:

$$\text{TotalPnL} = \text{RealizedPnL} + \text{UnrealizedPnL}$$

#### E. Storage Tiering Strategy
| Storage Tier | Technology | Purpose | Latency Target |
| :--- | :--- | :--- | :--- |
| **L0 Cache** | Thread-Local RAM / Shared Memory | Sub-millisecond PnL calculation loop | < 1 ms |
| **L1 Cache** | Redis Cluster | Real-time Risk Alerts & UI Websockets | < 5 ms |
| **L2 OLAP Database** | Apache Druid / ClickHouse | Multidimensional slicing, dicing & intraday risk | < 50 ms |
| **L3 Cold Archive** | Parquet files on S3 | End-of-Day (EOD) Accounting & Regulatory Audit | Batch |

---

### System Design 2: Intraday Risk Alert & Limit Enforcement Engine

* **Objective**: Evaluate pre-trade/post-trade risk limits (Max Drawdown, Value at Risk / VaR, Leverage Caps) across 10,000 active strategies.
* **Sliding Window Drawdown Calculation**: Maintain a **Monotonic Deque** of peak PnL values over a rolling 1-hour window to calculate Max Drawdown in O(1) time complexity.
* **Circuit Breakers**: If a trading pod breaches 80% of its daily drawdown limit, trigger automated risk warnings; at 100%, issue an automated **Kill-Switch API call** to the OEMS to cancel all open orders and flatten positions.

---

### System Design 3: Idempotent Trade Ingestion & Position Reconciliation Pipeline

* **Exactly-Once Ingestion**: Maintain a high-speed **Bloom Filter + In-Memory LRU Cache** indexed by `Execution_ID`. Duplicate execution reports from exchanges are dropped instantly at the ingress gateway.
* **EOD Position Reconciliation**: Asynchronous worker nodes pull End-of-Day position files from Prime Brokers (Goldman Sachs, Morgan Stanley) and perform automated diffing against Middle Office internal positions. Flag mismatches exceeding threshold >= $0.01.

---

# 2. LOW-LATENCY SYSTEMS, CONCURRENCY & JVM INTERNALS

Buy-side technical rounds in London and HK probe deep low-level execution details.

### A. Memory Model & Thread Safety
1. **`volatile` Semantics**:
   * Guarantees **visibility** across CPU cores (flushes write buffers to main memory) and prevents instruction reordering via **Memory Barriers** (StoreLoad, LoadLoad).
   * Does NOT guarantee atomicity for compound operations (e.g., `count++` requires CAS).
2. **Compare-And-Swap (CAS) & Atomic Primitives**:
   * Lock-free atomic mutations using CPU primitives (`LOCK CMPXCHG` on x86).
   * `AtomicReference`, `AtomicLong`, and Java 9+ `VarHandle` for high-throughput state updates.

### B. Lock-Free Concurrency & Disruption Patterns
1. **Why `ArrayBlockingQueue` Fails under 100k msg/sec**:
   * Uses a single `ReentrantLock` for both enqueue and dequeue, creating severe lock contention among worker threads.
2. **LMAX Disruptor Pattern (Ring Buffer)**:
   * **Pre-allocated Memory Array**: Zero garbage collection overhead during execution.
   * **Cache Line Padding (`@Contended`)**: Prevents **False Sharing** (when independent variables share the same 64-byte L1/L2 CPU cache line).
   * **Sequence Numbers**: Lock-free atomic sequence incrementing via memory barriers.

### C. Off-Heap Memory & Zero-Pause GC Tuning
1. **Direct Memory Access**:
   * `ByteBuffer.allocateDirect()` allocates memory outside the JVM garbage-collected heap.
   * Eliminates buffer copying between native OS sockets and JVM heap.
2. **Zero-Pause GC Algorithms**:
   * **ZGC** and **Shenandoah**: Concurrent garbage collectors maintaining max pause times < 1 ms regardless of heap size (up to terabytes).

### D. Zero-Copy & High-Performance Binary Serialization
* **Protobuf**: Compact binary encoding; requires parsing overhead.
* **SBE (Simple Binary Encoding) & FlatBuffers**: **Zero-copy deserialization**. Reads data directly out of byte buffers without allocating intermediate objects.

---

# 3. 2026 BUY-SIDE INTERVIEW TRENDS & EVALUATION RUBRIC

```
[ Traditional Format (Old) ]                    [ 2026 Buy-Side Format (Current) ]
  - Pure LeetCode algorithm memorization   ──>    - Multi-file Codebase Debugging
  - Single 30-line function from scratch   ──>    - AI-Enabled Coding (Cursor / Copilot Allowed)
  - Theoretical Big-O complexity           ──>    - "Vibe Coding" Screening & Code Auditing
```

### 1. Multi-File Codebase Debugging
* **Format**: Candidates are dropped into a **5–10 file C++/Java codebase** (e.g., a mini order router or PnL aggregator).
* **Evaluation Criteria**:
  1. Locating a subtle concurrency deadlock or memory leak;
  2. Refactoring a performance bottleneck to optimize p99 latency;
  3. Extending features while preserving existing unit test suites.

### 2. AI-Enabled Coding & Code Auditing
* **AI Tool Integration**: Coding platforms (CoderPad) allow AI tools (Cursor / Copilot).
* **The Evaluation Metric**: Interviewers test **Engineering Judgment and Code Auditing**:
  * *Can you prompt the AI like a junior developer?*
  * *Can you spot subtle bugs, race conditions, or memory overhead in AI-generated code?*

### 3. Strict Screening Against "Vibe Coding"
* Candidates who blindly accept AI suggestions without understanding memory barriers or data structure trade-offs get **instantly failed**. You must be prepared to walk through every line of code and justify its CPU/memory cost.

### 4. Citadel vs. Millennium Hiring Nuances
* **Citadel & Citadel Securities**: Strict 75-minute HackerRank OA (85%+ fail rate), followed by deep low-level systems & asymptotic discipline rounds.
* **Millennium & Point72**: Decentralized pod hiring directly by Portfolio Managers (PMs). High focus on practical codebase debugging, data pipeline refactoring, and domain risk/PnL logic.

---

# 4. FINANCIAL DOMAIN & TRADE LIFECYCLE FUNDAMENTALS

A Senior Middle Office Engineer must speak the language of Portfolio Managers:

```
[ Trade Execution (OEMS) ] ──(Fill)──> [ Middle Office Ingestion ] ──> [ Real-Time Position & PnL ]
                                                  │
                                                  ├──> [ Risk Engine (VaR / Drawdown) ]
                                                  └──> [ Compliance & Risk Limits ]
```

### 1. The Full Trade Lifecycle
Order Entry -> Matching/Fill -> Position State -> PnL Engine -> Risk Limits -> EOD Reconciliation -> Clearing/Settlement

### 2. Core Asset Classes & Derivatives
* **Equities**: Common stocks, ETFs, ADRs.
* **Fixed Income**: Government bonds, Corporate bonds, Interest Rate Swaps (IRS).
* **FX**: Spot FX, FX Forwards, FX Swaps.
* **Options & Derivatives**: The Greeks:
  * **Delta ($\Delta$)**: Sensitivity of option price to underlying asset price.
  * **Gamma ($\Gamma$)**: Rate of change of Delta.
  * **Vega ($\nu$)**: Sensitivity to implied volatility.
  * **Theta ($\Theta$)**: Time decay of the option.

---

# 5. THE 4-WEEK AUGUST SPRINT ROADMAP

| Week | Focus Area | Actionable Daily Tasks |
| :--- | :--- | :--- |
| **Week 1 (Aug 3–9)** | **Real-Time System Design** | Practice 100k updates/sec PnL Aggregator, Intraday Risk Engine, and Idempotent Ingestion diagrams. |
| **Week 2 (Aug 10–16)** | **Low-Latency & Concurrency** | Write lock-free Ring Buffer code, master Memory Barriers, CAS primitives, Disruptor pattern, and GC tuning. |
| **Week 3 (Aug 17–23)** | **LeetCode & Codebase Debugging** | Solve 20 Medium/Hard problems (Sliding Window, Monotonic Queue, Heap, LRU Cache); practice debugging multi-file repos. |
| **Week 4 (Aug 24–31)** | **Mock Interviews & PM Pitch** | Conduct mock rounds; refine your 2-minute ExodusPoint & AWS architecture narrative. |

---
*Created on 2026-08-02 for fredLuv.github.io/study-work-options.*
