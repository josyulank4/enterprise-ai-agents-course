# cost_security (s10)

**Section 10 — Cost, Security, and Governance · Lessons 38–41**

The money and the locks.

## Run

```bash
python demo.py
```

## What it does

1. **Unit economics** (Lesson 38) — cost per successful task for each demo
   (e.g. `hello_automation`: $0.0025) plus a portfolio figure.
2. **Build-vs-buy worksheet** (Lesson 39) — 3-year totals including the two
   costs buyers forget: the **exit price** ($15k to leave the vendor) and
   the **key-person premium** ($20k if your one expert leaves). Fixture →
   BUILD ($80k vs $87k).
3. **Secrets audit** (Lesson 40) — scans `fixture_config.ini`, finds the
   **planted** hardcoded `PROD_DB_PASSWORD` (fake — a fixture for this
   demo), and verifies the mock vault loads secrets by reference only, with
   no literals in code.
4. **Injection drill** (Lesson 41) — an "ignore previous instructions"
   payload is **BLOCKED** by the guardrail; a normal request is allowed.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 38 — Unit Economics | `unit_economics` |
| 39 — Build vs Buy | worksheet + exit price + key-person premium |
| 40 — Secrets | audit + mock vault |
| 41 — Injection Defense | guardrail drill |

> The credential in `fixture_config.ini` is a planted fake for the audit
> demo. The repo-wide secrets scan (validation check 15) excludes that
> file — everything else must be clean.
