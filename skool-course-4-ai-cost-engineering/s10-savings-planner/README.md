# savings-planner (s10)

**Section 10 — The Savings Playbook · Lessons 38–41**

Savings as a portfolio: levers scored by return per unit of risk,
sequenced by family law, compounded on the remainder, and replayed
against the book's Meridian workload.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `savings-planner demo: OK`.

## What it does

1. **The ranking** (`lever_score`, `rank_levers`): monthly saving ÷
   (risk × engineering weeks), inside the family order — quiet
   (waste) levers, then substitution, commercial last. Context diet
   leads at score 2,400; the committed-use discount, despite its
   quick win, waits its turn by law.
2. **The compounding** (`apply_portfolio`): each lever takes its
   fraction of what the previous levers left. Six fractions that
   "add up to 44.5%" deliver less — remainders, not headlines.
3. **The Meridian replay**: $48,000 → $43,200 → $41,256 → $37,956 →
   $36,437 → **$31,336** after tier routing (the book's "roughly
   thirty-one thousand") → $28,516 after committed use reprices only
   the optimized remainder.
4. **The plan** (`ninety_day_plan`): ranked levers start back to
   back from week 1, bucketed into 30-day phases.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 38 — Savings Are a Portfolio, Not a Trick | `apply_portfolio`'s remainder compounding |
| Lesson 39 — The Ranked Lever List | `lever_score` + `rank_levers` |
| Lesson 40 — The Quiet Levers and the Commercial Levers | The family order: quiet first, commercial last |
| Lesson 41 — The Meridian Workload and Your First Ninety Days | The $48k replay + `ninety_day_plan` |

## Key functions

- `lever_score(lever, base)` — expected monthly saving per unit of
  risk × effort.
- `rank_levers(levers, base)` — family order, then score descending.
- `apply_portfolio(base, ordered)` — running-balance rows after each
  lever (`monthly_after`, `saved_so_far`).
- `ninety_day_plan(ordered)` — start week and phase per lever.
