# rollout (s11)

**Section 11 — Deployment and Change Management · Lessons 42–45**

Land the automation without breaking the organization.

## Run

```bash
python demo.py
```

## What it does

- **Rollout-plan template** (Lesson 42) — pilot → expand → standardize,
  each phase with an exit criterion (including a kill criterion for the
  pilot).
- **Stakeholder-map template** (Lesson 43) — sponsor, process owner,
  IT/security, end users, and the skeptic (recruited as co-designer).
- **Runbook template** (Lesson 44) — normal ops, degraded mode, rollback
  (RTO 30 min), on-call.
- **Adoption dashboard** (Lesson 45) — simulated 90-day data across 4
  teams; `team-phoenix` (12% usage, 78% overrides) is flagged as the
  planted **work-around team**: automation theater, not adoption.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 42 — Rollout Strategy | `ROLLOUT_PLAN` template |
| 43 — Stakeholders | `STAKEHOLDER_MAP` template |
| 44 — Training & Docs | `RUNBOOK` template |
| 45 — Measuring Adoption | dashboard + work-around detector |

Render the templates with your process name and fill in the names — a
rollout plan with blank owner boxes is a plan to stall.
