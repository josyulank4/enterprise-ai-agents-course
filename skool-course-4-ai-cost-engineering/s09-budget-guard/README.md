# budget-guard (s09)

**Section 9 — Budgets, Alerts, and FinOps Governance · Lessons 35–37**

A budget as a decision made in advance: the tree, the burn-rate
alerts wired to graceful degradation, and the same budget enforced
as code in CI.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `budget-guard demo: OK`.

## What it does

1. **The tree** (`BUDGET_TREE`): team × feature × environment cells,
   each with a monthly budget and a named owner — a cell with no
   owner is a governance gap found on paper (Lesson 35).
2. **The walk** (`burn_projection`, `alert_level`, `cell_status`):
   the support copilot's runaway month: day 10 on track ($900,
   projecting $2,700) → day 12 warning ($2,100 projecting $5,250)
   → day 20 soft limit ($3,900 ≥ 90%) → day 24 hard ($4,050 ≥
   budget), each level carrying its degradation step — bend, never
   break (Lesson 36).
3. **Policy as code** (`ci_check`): a change with unbounded
   max_tokens, no feature tag, and an unapproved frontier dependency
   is refused with all three violations named; the compliant change
   passes clean (Lesson 37).

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 35 — A Budget Is a Decision Made in Advance | `BUDGET_TREE` cells with owners and baselines |
| Lesson 36 — Alerts, Limits, and Graceful Degradation | The four-level walk + `DEGRADATION` actions |
| Lesson 37 — Showback, Chargeback, and Policy as Code | `ci_check` refusing the forbidden change loudly |

## Key functions

- `burn_projection(spent, day, days_in_month)` — month-end projection
  at the current burn rate.
- `alert_level(spent, budget, day)` — `"on_track"`, `"warning"`,
  `"soft"`, or `"hard"`.
- `cell_status(cell, spent, day, tree)` — the full governance row:
  owner, projection, level, and the action attached to the level.
- `ci_check(change, max_tokens_ceiling)` — the violation list; an
  empty list is a pass.
