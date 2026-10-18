# model-router (s04)

**Section 4 — The Right Model for the Job · Lessons 13–16**

A tiered router over a golden set you can inspect: confidence signals,
escalation thresholds, the sweep lab, and the gate that certifies —
or refuses — the small model with evidence either way.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `model-router demo: OK`.

## What it does

1. **Golden set** (`build_golden_set`): 100 requests, difficulties
   0–9, confidence falling as difficulty rises, the small model
   correct up to difficulty 6 — the hand-labelled set of Lesson 13
   as data.
2. **Cascade routing** (`route_tier`, `evaluate`): small unless
   confidence is below threshold. At 0.55 the cascade costs $1.72
   (vs $4.00 all-frontier) at accuracy 1.00; all-small costs $0.20
   at accuracy 0.70.
3. **Threshold sweep** (`sweep_thresholds`): the Lesson 15 lab —
   savings and quality loss as two curves against one dial.
4. **Quality gate** (`quality_gate`): certifies @0.55, refuses @0.00
   (0.70 < the 0.95 floor). A refusal with evidence is a success.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 13 — Model Tiers and Why Most Traffic Is Easy | The golden set: difficulty distribution of real traffic |
| Lesson 14 — Four Routing Strategies | The cascade strategy, priced against both baselines |
| Lesson 15 — Confidence Signals and Escalation Thresholds | `sweep_thresholds`, the threshold lab |
| Lesson 16 — Proving Small Is Good Enough | `quality_gate` certify/refuse with evidence |

## Key functions

- `build_golden_set(n=100)` — deterministic labelled request list.
- `route_tier(request, threshold)` — `"small"` or `"frontier"`.
- `evaluate(threshold, golden)` — `total_cost`, `accuracy`,
  `escalation_rate` at that threshold.
- `sweep_thresholds(thresholds, golden)` — one `evaluate` row each.
- `quality_gate(threshold, min_accuracy=0.95, golden)` — dict with
  `certified` and the full `evidence` row.
