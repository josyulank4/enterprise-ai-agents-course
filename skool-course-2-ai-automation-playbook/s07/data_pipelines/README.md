# data_pipelines (s07)

**Section 7 — Data Pipelines · Lessons 26–29**

Automations starve without data: freshness, quality gates and features.

## Run

```bash
python demo.py
```

## What it does

1. **Batch vs streaming** (Lesson 27) — one source through both shapes with
   freshness/cost counters: batch = 3600s freshness at $0.10/run, streaming
   = 2s freshness at $0.001/record.
2. **Validation gates + quarantine** (Lesson 28) — 8 records in, 3 poisoned
   (negative amount, missing email, non-numeric amount) → quarantine with
   reasons; 5 clean records processed ($638.75 total).
3. **Feature pipeline with staleness refusal** (Lesson 29) — the mock agent
   is served fresh features but **refuses** 900s-old features past the 300s
   limit. Stale features must never silently feed a decision.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 26 — Starved Engines | why the pipeline exists at all |
| 27 — Batch vs Streaming | freshness/cost counters |
| 28 — Validation & Quarantine | `validate` + quarantine list |
| 29 — Features & Freshness | `serve_features` staleness refusal |
