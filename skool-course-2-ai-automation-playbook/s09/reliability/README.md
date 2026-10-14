# reliability (s09)

**Section 9 — Evaluation and Reliability · Lessons 34–37**

Prove it works before it matters.

## Run

```bash
python demo.py
```

## What it does

1. **Test harness** (Lesson 34) — golden runs + historical replay +
   synthetic edge-case fixtures. A deliberately broken `normalize_amount`
   (drops the cents) is **caught** by the golden runs; the fixed version
   passes everything.
2. **CI cost-regression gate** (Lesson 35) — a change costing $0.50/run
   against a $0.20 budget is **BLOCKED**; a $0.12 change passes. Reliability
   includes cost reliability.
3. **Canary ladder** (Lesson 36) — 12% canary error rate against a 5%
   threshold triggers **auto-rollback**; 1% promotes to the next rung.
4. **Monitoring dashboard** (Lesson 37) — SLO 99.9% with observed 99.5%
   exhausts the error budget → **deploys freeze**.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 34 — Test Harnesses | golden + replay + synthetic |
| 35 — CI for Workflows | cost-regression gate |
| 36 — Canary & Shadow | promotion ladder + auto-rollback |
| 37 — Monitoring | error-budget dashboard |

Copy the harness shape: every workflow step gets golden runs before it gets
a canary.
