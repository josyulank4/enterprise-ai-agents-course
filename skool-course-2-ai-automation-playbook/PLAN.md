# Code Repository Plan — Skool Course 2: AI Automation Playbook

**Status:** PLANNED (not built). Build starts only on the production order (see `PREP-STATE.md`).

## Scope

One runnable demo project per section (13 demos), plain Python, standard library only — no external dependencies, no network calls, no API keys. Every demo runs end to end with `python <demo>/demo.py` and prints a verifiable result. Patterns to copy, not a framework to install.

| Section | Demo project | What it does |
|---------|--------------|--------------|
| s00 | `hello_automation/` | One automated task end to end in under a minute — the repo smoke test |
| s01 | `business_case/` | Business-case calculator: volume, minutes/run, loaded wage, error rate, rework cost → payback period and break-even; outcome-statement and stall self-assessment templates |
| s02 | `process_discovery/` | Process-discovery analyzer: parses a sample event log, outputs a discovered process map, flags top candidates by rework frequency; automation scorecard scorer with ranked top-three export |
| s03 | `engine_choice/` | Judgment-boundary classifier (scriptable / judgment / human-only), engine-decision tool (five-axis scoring → recommended engine with reasoning), RPA-maintenance estimator |
| s04 | `workflow_orchestration/` | Mini orchestrator: idempotent steps, exponential-backoff retries with jitter, saga compensation, run-ID tracing; chaos mode (duplicate messages, flaky step) with ledger-balance assertion |
| s05 | `agent_workforce/` | Role-based agent simulator (researcher, triager, drafter, checker), structured handoff packages, supervision sampler computing optimal sampling rate from error costs |
| s06 | `integrations/` | REST poll vs webhook vs event-bus comparison on one order event (latency/cost/failure); legacy-adapter demo with swappable adapter (mock legacy → mock new API, zero workflow changes) |
| s07 | `data_pipelines/` | Batch vs streaming pipeline on one source with freshness/cost counters; validation gates + quarantine on poisoned input; feature pipeline serving a mock agent with staleness refusal |
| s08 | `hitl/` | Approval-queue demo: blast-radius rating, calibrated confidence thresholds, terminal reviewer UI, rubber-stamp detector; exception simulator; trust-calibration worksheet on simulated 90-day history |
| s09 | `reliability/` | Test harness (golden runs + historical replay + synthetic fixtures), CI demo with cost-regression gate, canary/shadow promotion ladder with auto-rollback, monitoring dashboard with error-budget freeze |
| s10 | `cost_security/` | Unit-economics calculator (cost per successful task across all demos), build-vs-buy worksheet with exit price and key-person premium, secrets audit (scans configs, verifies mock-vault loading), injection drill with guardrail verification |
| s11 | `rollout/` | Rollout-plan template (pilot/expand/standardize), stakeholder map template, runbook template, adoption dashboard on simulated 90-day data (usage, overrides, satisfaction) |
| s12 | `maturity_roadmap/` | Five-stage maturity assessment questionnaire → domain map with evidence gaps; accountability-map template; three-year roadmap template; capstone checklist verifying all section artifacts present |

## Tech stack

- Python 3.10+, standard library only (`json`, `sqlite3`, `http.server`, `argparse`, `dataclasses`, `unittest`-style asserts in `validate.py`)
- `requirements.txt`: empty (stdlib only), pinned comment explaining why
- `.gitignore`: `__pycache__/`, `*.pyc`, `.venv/`, `results/`
- `LICENSE`: MIT, (c) 2026 Naveen Kumar Josyula
- `README.md`: per-demo table, quickstart (`python validate.py`), how each demo maps to its lessons

## Validation plan (`validate.py`)

Numbered checks, all must be green (target: match or beat Course 1's 14/14):

1. Repo structure: all 13 demo directories present with `demo.py` + `README.md`
2. `s00/hello_automation` runs end to end, exit 0, prints success marker
3. `s01/business_case` calculator: known inputs → expected payback within tolerance
4. `s02/process_discovery` analyzer: sample log → expected top candidate identified; scorecard ranks correctly
5. `s03/engine_choice`: classifier labels the fixture steps correctly; decision tool recommends expected engine
6. `s04/workflow_orchestration` chaos mode: ledger balances, no double-charge, dead-letter populated
7. `s05/agent_workforce`: handoff packages contain all four required fields; sampler math checks out
8. `s06/integrations`: adapter swap produces identical workflow outputs (zero-change assertion)
9. `s07/data_pipelines`: poisoned input → quarantine populated, clean records processed, agent refuses on stale features
10. `s08/hitl`: approval queue processes 50 actions; rubber-stamp detector flags the planted fast reviewer
11. `s09/reliability`: golden suite catches the deliberately broken step; cost-regression gate blocks the expensive change; canary auto-rollback triggers
12. `s10/cost_security`: unit-economics math verified on fixtures; secrets audit finds the planted hardcoded credential; injection drill blocked
13. `s11/rollout`: adoption dashboard flags the planted work-around team
14. `s12/maturity_roadmap`: assessment produces a five-stage map; capstone checklist passes on a complete fixture
15. No hardcoded secrets anywhere in the repo (independent scan, excluding the planted fixture consumed by check 12)
16. `README.md` documents every demo and its lesson mapping; `RESULTS.md` written by the validation run itself

`RESULTS.md` records the green run: date, Python version, check-by-check results, total (e.g. 16/16).
