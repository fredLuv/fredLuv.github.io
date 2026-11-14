# Research Statement — Ethan (Feiyu) Lu

*Draft v1, 2026-09-06 · Target: one page when rendered · Area: AI for Economic Agency (HCI / social computing)*

---

## The question

**How can personalized AI agents expand an individual's ability to identify and act on economic opportunities — and how do we design them so that the gains do not require surrendering privacy or decision autonomy?**

## Why now, and why this is hard

AI assistance is often assumed to be a great equalizer, but the best field evidence says otherwise. In a randomized experiment with 640 Kenyan entrepreneurs, a GPT-4 business mentor improved high performers' profits by ~15% while *lowering* low performers' by ~8% (Otis et al., *Management Science* 2026). Strikingly, the gap was not explained by usage skill — both groups asked equally many, equally well-written questions. The mechanism was **task selection**: struggling entrepreneurs, by necessity, brought the AI problems that advice cannot fix, then paid real money to implement confident-sounding recommendations. The people with the most to gain from AI assistance are structurally positioned to be harmed by it.

Meanwhile, HCI research has shown both halves of a solution without yet joining them. Gig2Gether (CHI 2025) demonstrated that workers *want* data-driven economic insight — pooled income data enabled financial reflection and cross-platform solidarity — but also surfaced a hard tension: the aggregate evidence policymakers need sits uneasily with workers' fear of individual exposure and platform retaliation (CSCW 2025). Proxona (CHI 2025) demonstrated the other half: an LLM system that transforms an individual creator's messy audience data into grounded, conversational decision support, with a structured intermediate representation that keeps insights traceable to the data. Creators — themselves gig workers — made measurably more confident, better-evidenced content decisions. What does not yet exist is the middle layer: **decision support that runs on a worker's own economic data, on the worker's side, so that empowerment does not require exposure.**

## What I propose to build and study

1. **A worker-side economic copilot.** An agent that computes "when/where/whether to work" and financial-planning recommendations locally from the worker's own earnings and activity data, contributing only privacy-preserving aggregate statistics to collectives and policymakers — dissolving the insight-versus-exposure tension rather than trading it off.
2. **Design against the Kenya failure mode.** The task-selection mechanism implies concrete, testable design principles: *triage* (recognize when a problem needs capital or exit, not advice), *cost-aware recommendations* (rank actions by implementation cost for cash-constrained users), and *calibrated confidence* (stop producing polished five-point plans for problems the model cannot help with). Each is a buildable system feature and a field-testable hypothesis about who benefits.
3. **Evaluation with real stakes.** Following the standard set by incentive-compatible field studies, I want to measure whether such systems change real economic behavior and outcomes — not just perceived usefulness — and for whom, with heterogeneity by baseline position as a first-class outcome rather than a robustness check.

## Why I can do this

I have spent nine years building exactly the substrate this research needs: real-time financial risk systems processing 100GB+/minute at ExodusPoint, privacy-sensitive telemetry and IAM-controlled data paths at AWS, and compliance data pipelines at Goldman Sachs. I can build the systems worth running a field experiment on — and I want to spend a PhD learning to ask, and causally answer, the question of who they actually help.

---

*Contact: FredLu0521@gmail.com · linkedin.com/in/feiyulu001*
