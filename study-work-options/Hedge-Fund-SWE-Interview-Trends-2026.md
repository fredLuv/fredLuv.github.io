# How Hedge Fund SWE / Quant Dev Interviews Evolved (2026 Trends)

This document summarizes recent industry research on how top buy-side firms (**Citadel, Millennium, Jane Street, Point72, Man Group**) have updated their Software Engineer and Quantitative Developer interview formats.

---

## 🔍 Key Findings: Do They Still Test LeetCode in 2026?

### Short Answer:
**LeetCode is still used as an initial automated filter (OA), but pure "whiteboard algorithm recall" is largely DEAD in live interview rounds.**

---

## 🚨 The 3 Major Shifts in 2026 Buy-Side Interviews

```
[ Traditional Format (Old) ]                    [ 2026 Buy-Side Format (Current) ]
  - Pure LeetCode algorithm memorization   ──>    - Multi-file Codebase Debugging
  - Single 30-line function from scratch   ──>    - AI-Enabled Coding (Cursor / Copilot Allowed)
  - Theoretical Big-O complexity           ──>    - "Vibe Coding" Screening & Code Auditing
```

### 1. Shift to "Multi-File Codebase Debugging & Feature Extension"
* **Old Way**: "Reverse a linked list" or "Find median of two sorted arrays".
* **2026 Way**: You are dropped into a **realistic 5–10 file codebase** (e.g., a mini order router, a real-time PnL aggregator, or a lock-free memory buffer).
* **Your Task**: 
  1. Identify a subtle concurrency race condition or memory leak;
  2. Implement a new risk limit feature without breaking existing tests;
  3. Refactor a bottleneck to improve p99 latency.

---

### 2. Shift to "AI-Enabled / Copilot-Allowed" Engineering
* Top funds now recognize that senior engineers use AI coding tools in daily production.
* **The New Evaluation Metric**: Interviewers assess **Engineering Judgment, Spec Definition, and Prompt Architecture**:
  * *Can you instruct the AI like a junior developer?*
  * *Can you audit AI-generated code for hidden edge cases, memory leaks, and concurrency bugs?*

---

### 3. Rigorous Screening Against "Vibe Coding"
* **The "Vibe Coding" Trap**: Candidates who blindly accept AI code suggestions without understanding the underlying logic get **instant-failed**.
* **What Interviewers Test**: You will be asked to defend every single line of code:
  * *"Why did the AI choose `AtomicReference` here instead of a `ReentrantLock`?"*
  * *"What is the memory barrier impact of this volatile write under high throughput?"*

---

## 🏛️ Firm-Specific Nuances: Citadel vs. Millennium

### 🏰 Citadel & Citadel Securities
* **Online Assessment (HackerRank)**: Extremely strict 75-minute filter (85%+ fail rate). Requires 100% test case coverage on 2-3 LeetCode Medium/Hard problems.
* **Superday / Onsite Rounds**: Focuses heavily on **Low-Level Systems & Asymptotic Discipline** (Memory management, C++/Java concurrency internals, and low-latency system design).

### 🏢 Millennium & Point72 (Pod-Based Hiring)
* **Pod-Decentralized**: Interview loops are designed directly by the Portfolio Manager (PM) and Senior Tech Lead for that specific trading pod.
* **Practical Engineering Focus**: High focus on real-world debugging, data pipeline refactoring (PySpark/Java/Druid), and domain-specific risk/PnL logic over abstract puzzles.

---

## 🎯 Updated 4-Week Prep Strategy

1. **Initial Filter (30%)**: Keep sharp on LeetCode Medium/Hard patterns (Sliding Window, Monotonic Queue, Heap, LRU Cache).
2. **Codebase Debugging & Refactoring (35%)**: Practice navigating multi-file codebases, identifying race conditions, and writing clean, production-ready unit tests.
3. **AI Code Auditing (20%)**: Practice using Claude/Cursor to generate system components, then perform line-by-line code reviews identifying edge cases, GC pauses, and memory overhead.
4. **Low-Latency & Concurrency Fundamentals (15%)**: Master Java/C++ memory models, lock-free ring buffers, and off-heap memory management.

---
*Created on 2026-08-02 for fredLuv.github.io/study-work-options.*
