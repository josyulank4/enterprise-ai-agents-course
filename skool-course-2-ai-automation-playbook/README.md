# AI Automation Playbook — Code Repository (Skool Course 2)

**Course:** AI Automation Playbook: From Manual Work to Autonomous Systems (Skool-exclusive)
**Format:** 13 runnable demos, one per section — plain Python, standard library only.

No installs, no network calls, no API keys. Every demo runs end to end with
`python demo.py` inside its directory and prints a verifiable result plus a
`<name> demo: OK` marker. Patterns to copy, not a framework to install.

## Quickstart

```bash
git clone https://github.com/josyulank4/enterprise-ai-agents-course.git
cd enterprise-ai-agents-course/skool-course-2-ai-automation-playbook
python validate.py        # runs all 16 numbered checks; writes RESULTS.md
```

Or run any demo directly:

```bash
cd s04/workflow_orchestration && python demo.py
```

## Demos

| # | Directory | Section → Lessons | What it does |
|---|-----------|-------------------|--------------|
| s00 | `s00/hello_automation/` | 0 — Welcome → Lessons 1–2 | One automated task end to end in under a minute (repo smoke test) |
| s01 | `s01/business_case/` | 1 — The Automation Mindset → Lessons 3–5 | Business-case calculator: payback, break-even, outcome statement, stall self-assessment |
| s02 | `s02/process_discovery/` | 2 — Process Discovery and Task Mining → Lessons 6–9 | Event-log analyzer: process map, rework candidates, automation scorecard top-three |
| s03 | `s03/engine_choice/` | 3 — RPA vs AI-Native Automation → Lessons 10–13 | Judgment-boundary classifier, five-axis engine decision, RPA maintenance estimator |
| s04 | `s04/workflow_orchestration/` | 4 — Workflow Orchestration → Lessons 14–17 | Idempotent orchestrator: retries with jitter, saga compensation, chaos mode, dead-letter queue |
| s05 | `s05/agent_workforce/` | 5 — AI Agents as Workers → Lessons 18–21 | Role pipeline with structured handoffs, cost-optimal supervision sampling rate |
| s06 | `s06/integrations/` | 6 — Integrations and APIs → Lessons 22–25 | REST poll vs webhook vs event bus; swappable legacy adapter, zero-change assertion |
| s07 | `s07/data_pipelines/` | 7 — Data Pipelines → Lessons 26–29 | Batch vs streaming, validation gates + quarantine, feature staleness refusal |
| s08 | `s08/hitl/` | 8 — Human-in-the-Loop → Lessons 30–33 | Approval queue, blast-radius ratings, rubber-stamp detector, trust-calibration worksheet |
| s09 | `s09/reliability/` | 9 — Evaluation and Reliability → Lessons 34–37 | Test harness, CI cost gate, canary auto-rollback, error-budget dashboard |
| s10 | `s10/cost_security/` | 10 — Cost, Security, and Governance → Lessons 38–41 | Unit economics, build-vs-buy, secrets audit, injection drill |
| s11 | `s11/rollout/` | 11 — Deployment and Change Management → Lessons 42–45 | Rollout/stakeholder/runbook templates, adoption dashboard, work-around detector |
| s12 | `s12/maturity_roadmap/` | 12 — The Autonomous Enterprise + Capstone → Lessons 46–50 | Five-stage maturity assessment, accountability map, 3-year roadmap, capstone checklist |

## Lesson mapping

Each demo's `README.md` carries its own per-lesson table; the summary above
shows which course lessons each demo serves. The intended study loop: watch
the section, run its demo, then re-run the demo against your own workload
data before continuing.

## Validation

`validate.py` implements the 16 numbered checks from `PLAN.md`: repo
structure, every demo end to end, fixture-level assertions per demo (payback
math, top candidate, engine recommendation, ledger balance, handoff fields,
adapter swap, quarantine, rubber-stamp flag, golden-run catch, secrets
finding, work-around flag, capstone), the repo-wide secrets scan, and
README/RESULTS documentation. A green run writes `RESULTS.md`.
