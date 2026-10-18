# attribution-pipeline (s08)

**Section 8 — Cost Observability and Attribution · Lessons 31–34**

The per-request record, the tagging discipline, and the four views —
with the conservation proof that they are views of the same money,
and the five-percent rule applied honestly to the starting estate.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `attribution-pipeline demo: OK`.

## What it does

1. **The record** (`make_record`, `emit_sample_month`): 2,800
   per-request records for a sample month, each stamped at emission
   with feature, team, tenant, model, and cost (Lesson 32's schema).
   One stream arrives untagged — 60 frontier requests nobody named.
2. **The four views** (`rollup`, `four_views`): by feature, team,
   tenant, and model — each sums to the same $108.90. By feature,
   the copilot leads at $58.50.
3. **The rule** (`untagged_share`, `five_percent_rule`): untagged
   spend is $9.00 of $108.90 = **8.3%**, over the 5% limit. That
   number is the estate's starting line — Lesson 31's audit exercise,
   printed instead of asserted away.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 31 — Attribution Is a Name, Not a Number | The untagged stream: spend with no name |
| Lesson 32 — The Per-Request Record and Tagging Discipline | `make_record`'s schema, stamped at the gateway |
| Lesson 33 — The Attribution Pipeline: Gateway to Dashboard | `emit_sample_month` → `four_views`, end to end |
| Lesson 34 — Four Views of the Same Money | Every view summing to one grand total |

## Key functions

- `make_record(req_id, feature, team, tenant, model, cost)` — one
  schema-complete per-request record.
- `emit_sample_month(spec)` — the deterministic sample month.
- `rollup(records, key)` — totals by one tag; blanks read
  `"(untagged)"`.
- `four_views(records)` — rollups for feature, team, tenant, model.
- `untagged_share(records)` / `five_percent_rule(records, limit)` —
  the unnamed share and the pass/fail against the 5% target.
