# bill-decomposer (s02)

**Section 2 — The Bill Nobody Read · Lessons 5–8**

Turns one month of invoice-shaped spend into an explanation: named
driver categories with shares, the lines nobody owns, and the metric
that matters — cost per successful task, tail included.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `bill-decomposer demo: OK`.

## What it does

1. **Decomposition** (`decompose`): ten line items grouped into
   Lesson 6's nine driver categories — model tokens dominate at
   $10,450 of the $18,640 month (56.1%).
2. **Shadow spend** (`shadow_spend`): lines with owner `"unknown"` at
   $500 or more — failed-call retries ($890) and idle provisioned
   capacity ($1,140), $2,030 nobody can explain today.
3. **Task metrics** (`task_metrics`, `percentile`): nearest-rank
   percentiles over 20 sampled task costs — mean $0.2730, p50 $0.19,
   p95 $0.28, with one $1.85 tail task the mean quietly absorbs.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 5 — The Invoice Is a Summary, Not an Explanation | The decomposer answers what the invoice cannot |
| Lesson 6 — Anatomy of a Production AI Bill | The nine driver categories + shadow-spend flags |
| Lesson 7 — Metrics That Reveal the Real Drivers | Cost per successful task at p50/p95 |
| Lesson 8 — Decomposing a Support Copilot's Bill | The worked example: one month, decomposed end to end |

## Key functions

- `decompose(items=MONTH_ITEMS)` — dict with rounded `total` and
  `categories` rows (`category`, `amount`, `share`), largest first.
- `shadow_spend(items=MONTH_ITEMS, min_amount=500.0)` — unowned,
  material lines as dicts (`line`, `category`, `amount`).
- `percentile(values, p)` — nearest-rank percentile of a sample.
- `task_metrics(costs=TASK_COSTS)` — `mean`, `p50`, `p95` of cost per
  successful task, rounded to 4 decimals.
