# audit-kit (s12)

**Section 12 — The Full Audit · Lessons 46–48**

The end-to-end audit runner over the Harborline sample estate:
inventory, ninety-day attribution, ranked findings, the one-page
report, and the remediation plan — the course's method executed
by code, not described by slides.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `audit-kit demo: OK`.

## What it does

1. **The register** (`inventory`): 7 workloads — 3 claimed
   (support-copilot, doc-search, ticket-triage) and 4 the org chart
   had forgotten (legacy-summarizer, forgotten-etl-script,
   test-tenant-runner, shadow-dashboard), flagged unclaimed.
2. **The attribution** (`untagged_share`): $102,800 of 90-day spend,
   $17,400 of it unclaimed = **16.9%** — about a fifth of the money
   with no name on it, Harborline's first tenant truth.
3. **The findings** (`ranked_findings`, `recoverable_total`): six
   findings ranked by recoverable spend per unit of risk —
   untagged spend, unowned retries, frontier-on-trivial, uncached
   repetition, idle capacity, and the unbounded agent (priced as
   exposure, not saving). Recoverable total: $32,100 per quarter.
4. **The outputs** (`one_page_report`, `remediation_plan`): three
   numbers at the top, owners on every row, a plan dated and
   sequenced so quick wins fund the structural work.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 46 — Meet Harborline: Inventory and Attribution | `inventory` + `untagged_share` over the sample estate |
| Lesson 47 — Findings and the One-Page Report | `ranked_findings` + `one_page_report` |
| Lesson 48 — The Remediation Plan and Keeping It True | `remediation_plan` with owners, dates, savings |

## Key functions

- `inventory(register)` — workload counts, claimed/unclaimed split,
  90-day totals.
- `untagged_share(register)` — unclaimed share of estate spend.
- `ranked_findings(findings)` — findings with `score` (recoverable ÷
  risk), ranked descending.
- `recoverable_total(findings)` — summed recoverable spend.
- `one_page_report(register, findings)` — the report as one string.
- `remediation_plan(findings)` — ranked actions with owner, due
  date, and expected saving.
