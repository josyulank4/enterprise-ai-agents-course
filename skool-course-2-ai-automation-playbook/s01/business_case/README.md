# business_case (s01)

**Section 1 — The Automation Mindset · Lessons 3–5**

The economics of automation: volume, minutes/run, loaded wage, error rate and
rework cost → monthly savings, payback period and break-even volume.

## Run

```bash
python demo.py
```

## What it does

- `monthly_manual_cost` / `monthly_automation_cost` / `monthly_savings`
- `payback_months` — the worked example: $15,750/month savings on a $12,000
  build repays in **0.762 months (~23 days)**
- `break_even_monthly_volume` — runs/month at which 12 months of savings
  repay the build (~63.5)
- `outcome_statement` template (Lesson 3: outcomes, not tasks)
- `stall_self_assessment` — the 5-question stall checklist (Lesson 4)

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 3 — Outcomes, Not Tasks | `outcome_statement` template |
| 4 — Why Programs Stall | `STALL_QUESTIONS` self-assessment |
| 5 — Economics | payback / break-even math |

Swap the fixture constants at the top of `demo.py` for your own process to
build a real business case.
