# hitl (s08)

**Section 8 — Human-in-the-Loop · Lessons 30–33**

Humans where judgment lives, automation everywhere else.

## Run

```bash
python demo.py
```

## What it does

1. **Approval queue** (Lesson 30) — 50 actions; confidence ≥ 0.85
   auto-approves, the rest queue for review. Every action carries a
   **blast-radius rating** (HIGH ≥ $10k).
2. **Terminal reviewer UI** (Lesson 31) — the queue rendered as text with
   reviewer, decision and review time per action.
3. **Rubber-stamp detector** — reviewer "bob" approves everything in 1.5s;
   the detector (median review time < 5s AND approval rate > 95%) flags him.
   Rubber-stamping is the failure mode Lesson 31 warns about.
4. **Exception simulator** (Lesson 32) — HIGH blast-radius queued actions
   route to a specialist queue, not the line.
5. **Trust-calibration worksheet** (Lesson 33) — simulated 90-day history:
   approval rate climbs 0.55 → 0.91 while the auto-approve threshold loosens
   0.95 → 0.85. Start strict, loosen with evidence.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 30 — Approval Gates & Thresholds | queue + 0.85 threshold + blast radius |
| 31 — Reviewer Experience | terminal UI + rubber-stamp detector |
| 32 — Exceptions | specialist routing |
| 33 — Trust Calibration | 90-day worksheet |
