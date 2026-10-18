# AI Cost Engineering — Code Repository (Skool Course 4)

**Course:** AI Cost Engineering: Control Production AI Spend (Skool-exclusive)
**Companion to:** *AI Cost Engineering* by Naveen Kumar Josyula

This repository is the hands-on half of the course. It contains **13 runnable demos — one per course section** — that implement production AI cost engineering in plain Python: cost meters, bill decomposition, token ledgers, a model router with a quality gate, a three-layer cache lab, a bounded-agent simulator, a GPU break-even calculator, an attribution pipeline, a budget guard with policy-as-code checks, a savings planner, unit economics, a full audit kit, and the capstone studio.

Everything runs on the **Python standard library only**. There is nothing to install, no API key, and no network access anywhere. These are patterns to copy into your own systems, not a framework to depend on.

## Quickstart

```bash
# 1. Verify the whole repository end to end (16 checks):
python validate.py

# 2. Run any single demo:
cd s01-cost-meter
python demo.py        # ends with: cost-meter demo: OK
```

`validate.py` runs every demo in a fresh interpreter, re-verifies key behaviors by importing the demos as libraries, scans the tree for hardcoded secrets, and checks these docs. A green run writes `RESULTS.md`. **Python 3.10+** (on systems where the interpreter is named `python3`, use `python3` everywhere).

## How to study

Watch a section's lessons, then run its demo, then re-run the demo against your own numbers — your own invoice, your own traffic — before moving on. The formulas and checklists inside the demos are the durable artifacts.

## Demo map — section by section, tied to lessons

### s01 — `s01-cost-meter` (cost-meter) — Section 1: Welcome: Why AI Costs What It Does
Prices a sample day of traffic across model tiers and prints where the money went; lists a workload's always-running meters.
- Lesson 1 — Welcome: The Bill Nobody Budgeted For
- Lesson 2 — How to Use This Course and the Code Repository
- Lesson 3 — The Meter Is Always Running
- Lesson 4 — Success Is What Makes It Expensive

### s02 — `s02-bill-decomposer` (bill-decomposer) — Section 2: The Bill Nobody Read
Splits one month of sample spend into the nine named drivers, flags shadow-spend candidates, and computes cost per successful task at p50/p95.
- Lesson 5 — The Invoice Is a Summary, Not an Explanation
- Lesson 6 — Anatomy of a Production AI Bill
- Lesson 7 — Metrics That Reveal the Real Drivers
- Lesson 8 — Decomposing a Support Copilot's Bill

### s03 — `s03-token-ledger` (token-ledger) — Section 3: Tokens Are the Currency
Token counting and the per-request cost formula with prompt token budgets; a priced conversation showing context re-billed on every call; the three token stories diagnosis pack.
- Lesson 9 — What a Token Is and Why Prices Differ
- Lesson 10 — Context Is Re-Billed on Every Call
- Lesson 11 — The Per-Request Cost Formula
- Lesson 12 — Long Context and Reasoning Tokens: Tradeoffs

### s04 — `s04-model-router` (model-router) — Section 4: The Right Model for the Job
A tiered router with confidence signals and escalation thresholds, a threshold sweep lab, and the golden-set quality gate that certifies or refuses the small model with evidence.
- Lesson 13 — Model Tiers and Why Most Traffic Is Easy
- Lesson 14 — Four Routing Strategies
- Lesson 15 — Confidence Signals and Escalation Thresholds
- Lesson 16 — Proving Small Is Good Enough

### s05 — `s05-cache-lab` (cache-lab) — Section 5: Caching and Batching That Actually Pay
A three-layer cache simulator (exact-match, prompt-prefix, semantic) with hit-rate and break-even math, plus the batching-window discount drill.
- Lesson 17 — Answer Once, Serve Many: Cache Economics
- Lesson 18 — The Three Cache Layers
- Lesson 19 — Hit Rate, Break-Even, and What Good Looks Like
- Lesson 20 — Batching and the Failure Modes of Cheap

### s06 — `s06-bounded-agent` (bounded-agent) — Section 6: RAG and Agent Cost Traps
An agent-loop simulator with step, token, and max-cost budgets, and the context-bloat multiplication table — the looping task of Lesson 21 run unbounded, then bounded.
- Lesson 21 — Agents Have Trajectories, Not Costs
- Lesson 22 — RAG Inflation, Step by Step
- Lesson 23 — Architecture of a Bounded Agent
- Lesson 24 — The Arithmetic of Context Bloat
- Lesson 25 — Guardrails That Actually Work

### s07 — `s07-breakeven` (breakeven) — Section 7: GPU Economics and the Self-Hosting Break-Even
The API-vs-self-host break-even calculator with a full-week utilisation sweep, the hidden-cost proposal audit, and a decision-memo generator.
- Lesson 26 — Two Cost Curves and Why They Cross
- Lesson 27 — Utilisation Is Everything
- Lesson 28 — The Self-Hosting Stack and Quantization
- Lesson 29 — The Hidden Costs Nobody Puts in the Proposal
- Lesson 30 — The Break-Even Formula and Hybrid Patterns

### s08 — `s08-attribution-pipeline` (attribution-pipeline) — Section 8: Cost Observability and Attribution
A per-request record emitter with a tagging schema, rolled into the four views — feature, team, tenant, model — with the five-percent untagged rule applied.
- Lesson 31 — Attribution Is a Name, Not a Number
- Lesson 32 — The Per-Request Record and Tagging Discipline
- Lesson 33 — The Attribution Pipeline: Gateway to Dashboard
- Lesson 34 — Four Views of the Same Money

### s09 — `s09-budget-guard` (budget-guard) — Section 9: Budgets, Alerts, and FinOps Governance
A budget tree by team × feature × environment with burn-rate alerts, soft and hard limits, graceful degradation, and policy-as-code CI checks.
- Lesson 35 — A Budget Is a Decision Made in Advance
- Lesson 36 — Alerts, Limits, and Graceful Degradation
- Lesson 37 — Showback, Chargeback, and Policy as Code

### s10 — `s10-savings-planner` (savings-planner) — Section 10: The Savings Playbook
The ranked lever list scored by return per unit of risk, quiet and commercial lever passes in the course's family order, the Meridian replay ($48,000 → $31,336), and a ninety-day plan builder.
- Lesson 38 — Savings Are a Portfolio, Not a Trick
- Lesson 39 — The Ranked Lever List
- Lesson 40 — The Quiet Levers and the Commercial Levers
- Lesson 41 — The Meridian Workload and Your First Ninety Days

### s11 — `s11-unit-economics` (unit-economics) — Section 11: Pricing, Forecasting, and Capacity
A fully-loaded unit-cost and gross-margin calculator, a four-model pricing comparator, and a driver-based two-quarter forecaster with a three-futures scenario.
- Lesson 42 — The Unit Is the Price: Gross-Margin Math
- Lesson 43 — Pricing Models Compared
- Lesson 44 — A Forecast Built From Drivers
- Lesson 45 — Capacity, Scenarios, and Committed Use

### s12 — `s12-audit-kit` (audit-kit) — Section 12: The Full Audit
An end-to-end audit runner over the Harborline sample estate — inventory register, ninety-day attribution, ranked findings, one-page report, and a remediation plan with owners and dates.
- Lesson 46 — Meet Harborline: Inventory and Attribution
- Lesson 47 — Findings and the One-Page Report
- Lesson 48 — The Remediation Plan and Keeping It True

### s13 — `s13-capstone-studio` (capstone-studio) — Section 13: Capstone: Your Production Cost Audit
The capstone audit-pack template with a completeness gate, the Appendix A readiness-checklist scorer, and the roadmap planner.
- Lesson 49 — Capstone Studio: Your Own Production Cost Audit
- Lesson 50 — Course Close: Durable Principles, Your Roadmap

## Validation

```bash
python validate.py
```

16 numbered checks: repo structure; each of the 13 demos run end to end plus API-level assertions on its documented key functions; a repo-wide hardcoded-secrets scan; and a documentation check (this README against the demo tree). The run prints `ALL CHECKS PASSED (16/16 green)` and writes `RESULTS.md` with the full record.

## Layout

```text
code-repo/
├── README.md            (this file)
├── validate.py          (16-check validation harness; writes RESULTS.md)
├── RESULTS.md           (written by the validation run)
├── requirements.txt     (intentionally empty — standard library only)
├── LICENSE
└── s01-cost-meter/ … s13-capstone-studio/
                         (one directory per section, each holding its
                          demo: demo.py + README.md — see each demo's
                          README for its key functions and lesson detail)
```
