# cost-meter (s01)

**Section 1 — Welcome: Why AI Costs What It Does · Lessons 1–4**

The course's first instrument: a cost meter that prices requests and a
whole sample day of traffic across model tiers, and prints where the
money went — the decomposition Lesson 1's team could not produce from
their invoice. Also lists a workload's always-running meters.

## How to run

```bash
python demo.py
```

Standard library only. Prints the priced day and ends with
`cost-meter demo: OK`.

## What it does

1. **Per-request pricing** (`price_request`): input tokens × input
   price + output tokens × output price, from a three-tier rate card
   (frontier / standard / small, USD per million tokens).
2. **A priced day** (`price_day`): four workloads, 41,500 calls,
   $500.07 total — with the frontier support copilot alone at $346.50
   (69.3%), the concentration an invoice total hides.
3. **Always-on meters** (`always_on_meters`): per-call for every
   workload; per-step if it loops, per-retrieval if it searches,
   per-retry if it can fail and retry (Lesson 3).

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 1 — Welcome: The Bill Nobody Budgeted For | The priced sample day answers "which part spent it, on what" |
| Lesson 2 — How to Use This Course and the Code Repository | This meter is the repo tour's first runnable check |
| Lesson 3 — The Meter Is Always Running | `always_on_meters` from a workload's feature flags |
| Lesson 4 — Success Is What Makes It Expensive | The day is priced at success volume — usage, not waste |

## Key functions

- `price_request(tier, input_tokens, output_tokens)` — cost of one
  request in USD; `price_request("frontier", 2400, 620)` is `0.0825`.
- `price_day(sample=SAMPLE_DAY)` — dict with per-workload `rows`
  (calls, token totals, cost per call, cost) and a rounded `total`.
- `always_on_meters(loops=False, retrieval=False, retries=False)` —
  the meter names that run for a workload with those features, always
  starting with `"per-call"`.
