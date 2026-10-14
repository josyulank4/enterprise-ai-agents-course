# engine_choice (s03)

**Section 3 — RPA vs AI-Native Automation · Lessons 10–13**

Pick the right engine for the work instead of defaulting to one.

## Run

```bash
python demo.py
```

## What it does

1. **Judgment-boundary classifier** (`classify`): labels each step
   `scriptable` / `judgment` / `human-only`. Regulated or safety-critical
   work is always `human-only`; judgment or unstructured/variable work is
   `judgment`; the rest is `scriptable`. All 5 fixture steps classify
   correctly.
2. **Engine-decision tool** (`recommend_engine`): five-axis scoring
   (input structure, volume, variability, exception rate, judgment need)
   across RPA, workflow script, AI agent and human — with a reasoning string
   per engine. Fixture (structured, high-volume invoice coding) → **RPA**.
3. **RPA maintenance estimator** (`rpa_annual_maintenance`): RPA's hidden tax.
   Fixture: 12 UI breaks × 6h × $75 + $8k license = **$13,400/yr**.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 10 — RPA | classifier's scriptable band; maintenance estimator |
| 11 — AI-Native | classifier's judgment band |
| 12 — Head-to-Head | five-axis scoring across 4 engines |
| 13 — Hybrid Architectures | per-step classification enables mixing engines |

Feed your own process steps through `classify`, then score the shortlist
with `recommend_engine`.
