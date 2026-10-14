"""s09 / reliability — prove it works before it matters.

Lesson mapping: Section 9, Lessons 34-37 (test harnesses, CI regression,
canary/shadow, monitoring and error budgets).
What it does:
  1. test harness: golden runs + historical replay + synthetic fixtures, with
     a deliberately broken step the harness must catch,
  2. CI demo: a cost-regression gate blocks an expensive change,
  3. canary/shadow promotion ladder with auto-rollback on error-rate breach,
  4. monitoring dashboard: exhausted error budget freezes deploys.
"""

from __future__ import annotations


# ------------------------------------------------- 1. test harness
def normalize_amount(raw: str) -> float:
    return float(raw.replace("$", "").replace(",", ""))


def broken_normalize_amount(raw: str) -> float:
    """Deliberately broken: drops the cents. The harness must catch this."""
    return float(raw.replace("$", "").replace(",", "").split(".")[0])


GOLDEN_RUNS = [
    ("normalize_amount", normalize_amount, "$1,234.56", 1234.56),
    ("normalize_amount", normalize_amount, "$89.00", 89.0),
]

HISTORICAL_REPLAY = [  # recorded (input -> output) pairs from production
    ("$4,120.75", 4120.75),
    ("$0.99", 0.99),
]

SYNTHETIC_FIXTURES = ["$0.00", "$1,000,000.01", "$7.5"]  # edge cases


def run_harness(step_fn, golden, replay, synthetic) -> dict:
    failures = []
    for name, fn, given, expected in golden:
        if fn is step_fn and abs(fn(given) - expected) > 1e-9:
            failures.append(f"golden {name}({given!r}): got {fn(given)}, want {expected}")
    for given, expected in replay:
        if abs(step_fn(given) - expected) > 1e-9:
            failures.append(f"replay({given!r}): got {step_fn(given)}, want {expected}")
    for given in synthetic:  # must not crash on edges
        step_fn(given)
    return {"failures": failures, "passed": not failures}


# ------------------------------------------------- 2. CI cost-regression gate
COST_BUDGET_PER_RUN = 0.20


def ci_gate(change: dict) -> tuple[bool, str]:
    if change["cost_per_run"] > COST_BUDGET_PER_RUN:
        return False, (f"BLOCKED: ${change['cost_per_run']:.2f}/run exceeds "
                       f"${COST_BUDGET_PER_RUN:.2f} budget")
    return True, "passed"


# ------------------------------------------------- 3. canary ladder
CANARY_ERROR_THRESHOLD = 0.05


def canary_check(error_rate: float) -> tuple[bool, str]:
    if error_rate > CANARY_ERROR_THRESHOLD:
        return True, (f"ROLLBACK: canary error rate {error_rate:.0%} exceeds "
                      f"{CANARY_ERROR_THRESHOLD:.0%} threshold")
    return False, "promote to next rung"


# ------------------------------------------------- 4. monitoring dashboard
def error_budget(slo: float, observed: float) -> dict:
    budget = 1.0 - slo
    consumed = max(0.0, slo - observed)
    exhausted = consumed >= budget
    return {"slo": slo, "observed": observed, "budget": budget,
            "consumed": consumed, "freeze_deploys": exhausted}


def main() -> None:
    good = run_harness(normalize_amount, GOLDEN_RUNS, HISTORICAL_REPLAY,
                       SYNTHETIC_FIXTURES)
    assert good["passed"], good["failures"]

    caught = run_harness(broken_normalize_amount, GOLDEN_RUNS, HISTORICAL_REPLAY,
                         SYNTHETIC_FIXTURES)
    assert not caught["passed"] and caught["failures"], "harness missed the broken step"

    ok, msg_ok = ci_gate({"name": "cheaper parser", "cost_per_run": 0.12})
    blocked, msg_blocked = ci_gate({"name": "bigger model", "cost_per_run": 0.50})
    assert ok and not blocked, (msg_ok, msg_blocked)

    rollback, msg_rb = canary_check(0.12)
    promote, msg_promote = canary_check(0.01)
    assert rollback and not promote

    budget = error_budget(slo=0.999, observed=0.995)
    assert budget["freeze_deploys"] is True
    healthy = error_budget(slo=0.999, observed=0.9995)
    assert healthy["freeze_deploys"] is False

    print("reliability: test harness")
    print(f"  golden runs + replay + synthetic fixtures: {len(GOLDEN_RUNS)} golden, "
          f"{len(HISTORICAL_REPLAY)} replay, {len(SYNTHETIC_FIXTURES)} synthetic — PASS")
    print(f"  deliberately broken step caught: {caught['failures'][0]}")
    print(f"CI cost-regression gate: '{msg_ok}' | bigger-model change -> {msg_blocked}")
    print(f"canary ladder: 12% errors -> {msg_rb} | 1% errors -> {msg_promote}")
    print(f"monitoring dashboard: SLO 99.9%, observed 99.5% -> "
          f"error budget exhausted, freeze_deploys={budget['freeze_deploys']}")
    print("reliability demo: OK")


if __name__ == "__main__":
    main()
