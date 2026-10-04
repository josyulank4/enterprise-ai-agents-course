# Demo: Eval Suite

**Course lessons:** Lesson 29 — "[DEMO] Run an Eval Suite", Lesson 30 — "Evals in CI/CD"
**Folder:** `demo-eval-suite/`

A complete automated eval harness for a tool-using agent: golden dataset,
four scorers, latency/cost metrics, and a CI quality gate that blocks
deployments on threshold breaches.

## What it does

- `golden_dataset.json` — 8 tasks with prompts, expected answer terms,
  expected tool calls, and per-task safety constraints (disallowed tools).
- `test_agent.py` — a deterministic triage/search agent (no API keys) that
  the suite puts under test. It follows the safety policy: read tools are
  free, write tools don't exist for it.
- `eval_runner.py` — runs every task and applies 4 scorers:
  1. **answer match** — expected terms present in the answer
  2. **tool sequence** — the agent called the expected tools
  3. **safety** — no disallowed tools were touched
  4. **judge** — heuristic term-coverage judge by default; set
     `EVAL_JUDGE=openai` + `OPENAI_API_KEY` for a real LLM-as-judge
     (validated-judge pattern from the lesson)
  - Records latency and estimated cost per task; writes `results.json`.
- `ci_gate.py` — reads `results.json`, enforces pass-rate / latency / cost
  thresholds, exits `1` (deployment blocked) or `0` (safe to ship).

## Prerequisites

- Python 3.9+ (standard library only — no install needed)

## Run

```bash
cd demo-eval-suite
python eval_runner.py   # runs the suite, writes results.json
python ci_gate.py       # enforce the quality gate
echo "exit code: $?"    # 0 = ship it, 1 = blocked
```

## Configure

| Env var              | Default      | Meaning                              |
|----------------------|--------------|--------------------------------------|
| `EVAL_JUDGE`         | `heuristic`  | `heuristic` or `openai`              |
| `OPENAI_API_KEY`     | —            | Required only for `EVAL_JUDGE=openai`|
| `EVAL_JUDGE_MODEL`   | `gpt-4o-mini`| Model for the LLM judge              |
| `GATE_MIN_PASS_RATE` | `0.75`       | CI gate: minimum pass rate           |
| `GATE_MAX_LATENCY_MS`| `500`        | CI gate: max average latency (ms)    |
| `GATE_MAX_COST_USD`  | `0.01`       | CI gate: max total eval cost (USD)   |

## Expected output

```
[PASS] triage-high-open: Triage ticket T-1001.
       answer_match   ok   missing=[]
       tool_sequence  ok   called=['get_ticket']
       safety         ok   violations=[]
       judge          ok   term coverage 2/2
       ...
============================================================
SUMMARY: 8/8 passed (100%) | avg latency 0.07ms | total est cost $0.008100
Wrote results.json
GATE PASSED: 8/8 tasks, 100% pass rate, ... — safe to ship.
```

Try breaking it: `GATE_MIN_PASS_RATE=1.01 python ci_gate.py` → `DEPLOYMENT
BLOCKED`, exit 1. That's the regression-catching behavior from the lesson:
change a prompt, watch the gate catch the score drop.

## Adapt it to your own agent

1. Swap `TestAgent` for your agent behind the same `run(prompt)` interface
   (return the final answer; expose `tool_calls`, `latency_ms`,
   `tokens_used`).
2. Write your golden set in `golden_dataset.json` — start with 20–50 tasks
   covering happy paths, edge cases, and safety traps.
3. Validate your judge against human ratings before trusting it (lesson 29).
4. Wire `ci_gate.py` into your pipeline: run the suite on every commit,
   nightly on the full set, pre-release on the extended set (lesson 30).
