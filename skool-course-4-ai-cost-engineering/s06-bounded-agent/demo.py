"""s06 / bounded-agent — agent loops with budgets that stop them.

Lesson mapping: Section 6, Lessons 21-25.
What it does:
  1. Prices one looping agent task step by step — the full trajectory
     a chatbot estimate would never show (Lesson 21).
  2. Runs the same task unbounded (36 steps, $0.756) and bounded:
     step, token, and max-cost budgets stop it at step 23 with a
     partial result and a spend report, never a silent kill
     (Lessons 23 and 25).
  3. Builds the context-bloat multiplication table (Lesson 24):
     context size x steps, priced — and marks where budgets break.
"""

from __future__ import annotations

IN_PRICE, OUT_PRICE = 3.00, 15.00   # standard tier, USD per 1M tokens
STEP_IN, STEP_OUT = 4000, 600       # tokens carried per agent step

# The looping task from Lesson 21: plan -> retrieve -> verify, and the
# verify step keeps failing, so the agent replans. 12 cycles x 3 steps.
LOOP_TASK = tuple(
    step for _ in range(12) for step in ("plan", "retrieve", "verify")
)


def step_cost(input_tokens: int = STEP_IN,
              output_tokens: int = STEP_OUT) -> float:
    """One agent step at carrying cost: context in, action out."""
    return (input_tokens * IN_PRICE + output_tokens * OUT_PRICE) / 1_000_000


def run_unbounded(task=LOOP_TASK) -> dict:
    """The agent as shipped in Lesson 21: it runs the whole loop."""
    cost = len(task) * step_cost()
    return {"steps": len(task), "tokens": len(task) * (STEP_IN + STEP_OUT),
            "cost": round(cost, 4), "stop_reason": "task_exhausted",
            "completed": False}


def run_bounded(task=LOOP_TASK, max_steps: int = 30,
                max_tokens: int = 120_000, max_cost: float = 0.50) -> dict:
    """The bounded agent of Lesson 23: three budgets, checked per step.
    On exhaustion it stops and reports what it finished, what it left
    undone, and what it spent (Lesson 25's guardrail contract)."""
    spent = 0.0
    tokens = 0
    done = 0
    reason = "task_exhausted"
    for _ in task:
        nxt_cost = step_cost()
        nxt_tokens = STEP_IN + STEP_OUT
        if done + 1 > max_steps:
            reason = "max_steps_budget"
            break
        if tokens + nxt_tokens > max_tokens:
            reason = "max_tokens_budget"
            break
        if spent + nxt_cost > max_cost:
            reason = "max_cost_budget"
            break
        spent += nxt_cost
        tokens += nxt_tokens
        done += 1
    return {"steps": done, "tokens": tokens, "cost": round(spent, 4),
            "stop_reason": reason, "completed": done == len(task),
            "partial_result": done < len(task)}


def context_bloat_table(contexts=(2000, 8000, 32000),
                        steps=(5, 25, 60),
                        in_price: float = IN_PRICE) -> dict:
    """USD of input re-billing for each (context, steps) cell:
    context tokens x steps x input price (Lesson 24's arithmetic)."""
    table = {}
    for ctx in contexts:
        for n in steps:
            table[(ctx, n)] = round(ctx * n * in_price / 1_000_000, 4)
    return table


def main() -> None:
    unb = run_unbounded()
    print(f"Unbounded run: {unb['steps']} steps, {unb['tokens']:,} tokens, "
          f"${unb['cost']:.3f}, stop={unb['stop_reason']} — the loop "
          f"from Lesson 21, priced step by step")
    bnd = run_bounded()
    print(f"Bounded run:   {bnd['steps']} steps, {bnd['tokens']:,} tokens, "
          f"${bnd['cost']:.3f}, stop={bnd['stop_reason']}, "
          f"partial result handed back: {bnd['partial_result']}")
    table = context_bloat_table()
    print("Context-bloat table (USD of re-billed input):")
    for (ctx, n), cost in sorted(table.items()):
        print(f"  context {ctx:>6,} tokens x {n:>2} steps = ${cost:.2f}")
    print(f"  the marked cell — 32,000 x 60 = ${table[(32000, 60)]:.2f} — "
          f"is where an unbounded design spends its budget invisibly")
    print("bounded-agent demo: OK")


if __name__ == "__main__":
    main()
