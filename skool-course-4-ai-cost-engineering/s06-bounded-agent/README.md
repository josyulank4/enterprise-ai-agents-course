# bounded-agent (s06)

**Section 6 — RAG and Agent Cost Traps · Lessons 21–25**

The section's argument as a runnable contrast: the same looping task,
run unbounded and then bounded — price, trajectory, and exit compared
side by side.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `bounded-agent demo: OK`.

## What it does

1. **The trajectory** (`run_unbounded`): Lesson 21's looping task —
   plan → retrieve → verify-fail, 12 cycles, 36 steps, 165,600
   tokens, $0.756. Steps a chatbot estimate never counts: the
   replans, the repeated retrievals, the reflections.
2. **The bounded agent** (`run_bounded`): step, token, and max-cost
   budgets checked before every step. The cost budget binds first:
   the run stops at step 23 having spent $0.483, and hands back a
   partial result with its spend report — never a silent kill.
3. **The bloat table** (`context_bloat_table`): context × steps
   priced at input rates; the 32,000-token × 60-step cell costs
   $5.76 of pure re-billing — the region guardrails exist to fence.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 21 — Agents Have Trajectories, Not Costs | The priced 36-step loop trajectory |
| Lesson 22 — RAG Inflation, Step by Step | Each step carries its retrieval context at full price |
| Lesson 23 — Architecture of a Bounded Agent | `run_bounded`'s three budgets, checked per step |
| Lesson 24 — The Arithmetic of Context Bloat | `context_bloat_table` and its marked cell |
| Lesson 25 — Guardrails That Actually Work | Stop-with-report instead of silent exhaustion |

## Key functions

- `step_cost(input_tokens, output_tokens)` — one step's carrying cost.
- `run_unbounded(task)` — steps, tokens, cost, stop reason.
- `run_bounded(task, max_steps, max_tokens, max_cost)` — the guarded
  run: steps completed, spend, which budget bound, `partial_result`.
- `context_bloat_table(contexts, steps, in_price)` — dict keyed by
  `(context_tokens, steps)` with the re-billing cost per cell.
