# workflow_orchestration (s04)

**Section 4 — Workflow Orchestration · Lessons 14–17**

Reliability patterns that survive chaos: idempotent steps, exponential-
backoff retries with jitter, saga compensation and run-ID tracing.

## Run

```bash
python demo.py
```

## What it does

`Orchestrator.run_step` implements the Lesson 15 pattern set:

- **Idempotency keys** — a duplicate delivery of the debit message returns
  the recorded result instead of re-executing (chaos mode fires one).
- **Exponential backoff + jitter** — the flaky debit step fails twice, then
  succeeds on retry.
- **Saga compensation** — a second run's credit step always fails, so the
  saga refunds the debit; the ledger ends exactly where it started.
- **Run-ID tracing** — every attempt, backoff and dedup is logged per run.
- **Dead-letter queue** — the exhausted credit step lands there with its
  run ID, step name and error.

Verifiable result: ledger A=$900 / B=$100 after a $100 transfer (no double
charge — `debit_applications == 1` on the chaos run), saga refund verified,
dead-letter queue holds exactly 1 item.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 14 — Orchestration vs Choreography | central `Orchestrator` owns the run |
| 15 — Idempotency, Retries, Sagas | `run_step` + compensation |
| 16 — Observability | run-ID trace log |
| 17 — First Reliable Workflow | chaos run as the acceptance test |
