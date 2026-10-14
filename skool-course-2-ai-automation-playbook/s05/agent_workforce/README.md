# agent_workforce (s05)

**Section 5 — AI Agents as Workers · Lessons 18–21**

A digital team with supervision that pays for itself.

## Run

```bash
python demo.py
```

## What it does

1. **Role pipeline** — researcher → triager → drafter → checker over 3 work
   items (Lesson 18). Each role passes a **structured handoff package** with
   the four required fields (Lesson 20): `item_id`, `payload`, `provenance`
   (who touched it), `confidence`. The checker rejects any handoff missing a
   field and escalates low-confidence items.
2. **Supervision sampler** (Lesson 19) — the cost-optimal review rate from
   error economics. Minimizing
   `C(r) = r·C_review + (1−r)·p·C_error + r²·C_coordination` gives
   `r* = (p·C_error − C_review) / (2·C_coordination)`. Fixture
   (8% errors, $500/error, $5/review) → **35% sampling**, cheaper per item
   than sampling nothing or everything.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 18 — Designing Agent Roles | researcher/triager/drafter/checker |
| 19 — Supervision Patterns | `optimal_sample_rate` |
| 20 — Handoffs | four-field handoff packages |
| 21 — The Digital Team | end-to-end pipeline run |
