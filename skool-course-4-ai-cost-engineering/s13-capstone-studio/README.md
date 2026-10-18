# capstone-studio (s13)

**Section 13 — Capstone: Your Production Cost Audit · Lessons 49–50**

The studio where the course becomes a deliverable: the five-part
audit pack template with a completeness gate, the Appendix A
readiness scorer that grades it, and the dated roadmap planner.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `capstone-studio demo: OK`.

## What it does

1. **The pack** (`blank_pack`, `fill_sample_pack`, `check_pack`):
   the five parts of Lesson 49 — register, attribution views,
   one-page report, remediation plan, checklist score. An empty
   pack fails with all five parts named missing; the filled sample
   passes. The standard: a peer could re-run the audit from the
   pack alone.
2. **The scorer** (`score_checklist`): Appendix A's five areas
   (metering, attribution, budgets, optimisation, governance), four
   items each. The sample estate scores 14/20 = 70% — attribution
   weakest at 50%, exactly where the course said it would be.
3. **The roadmap** (`roadmap_plan`, `FIVE_FORMULAS`): first audit
   date, first three levers in order, first budget tree — as dated
   commitments, beside the five durable formulas the course closes
   with.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 49 — Capstone Studio: Your Own Production Cost Audit | The five-part pack + `check_pack` completeness gate |
| Lesson 50 — Course Close: Durable Principles, Your Roadmap | `roadmap_plan` + `FIVE_FORMULAS` |

## Key functions

- `blank_pack()` / `fill_sample_pack()` — the template and a filled
  example.
- `check_pack(pack)` — `(complete, missing)` over the five parts.
- `score_checklist(answers)` — per-area fractions and the overall
  readiness (`areas`, `overall`, `passed_items`, `total_items`).
- `roadmap_plan(first_audit_date, first_levers, budget_tree_cells)`
  — the dated commitment list.
- `FIVE_FORMULAS` — the course's five durable formulas, verbatim
  for the roadmap page.
