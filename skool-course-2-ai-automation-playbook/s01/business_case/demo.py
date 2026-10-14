"""s01 / business_case — the economics of automation.

Lesson mapping: Section 1, Lessons 3-5 (outcomes, why programs stall, economics).
What it does: turns volume, minutes/run, loaded wage, error rate and rework
cost into monthly savings, payback period and break-even volume, plus the
outcome-statement and stall self-assessment templates from the lessons.
"""

from __future__ import annotations

# ---------------------------------------------------------------- fixtures
# A mid-size AP invoice-coding task. These inputs are the worked example in
# Lesson 5; the validator re-derives the expected payback from them.
VOLUME_PER_MONTH = 1000          # runs/month
MINUTES_PER_RUN = 15             # manual minutes per run
LOADED_WAGE_PER_HOUR = 60.0      # fully loaded $/hour
ERROR_RATE = 0.05                # 5% of runs need rework
REWORK_COST_PER_ERROR = 25.0     # $ per error fixed
BUILD_COST = 12000.0             # one-time build $ 
RUN_COST_PER_RUN = 0.50          # automation $/run (infra + model)


# ------------------------------------------------------------------ model
def cost_per_manual_run(minutes: float, wage_per_hour: float) -> float:
    return (minutes / 60.0) * wage_per_hour


def monthly_manual_cost(volume: int, minutes: float, wage: float,
                        error_rate: float, rework: float) -> float:
    labor = volume * cost_per_manual_run(minutes, wage)
    rework_cost = volume * error_rate * rework
    return labor + rework_cost


def monthly_automation_cost(volume: int, run_cost: float) -> float:
    return volume * run_cost


def monthly_savings(volume: int, minutes: float, wage: float, error_rate: float,
                    rework: float, run_cost: float) -> float:
    return (monthly_manual_cost(volume, minutes, wage, error_rate, rework)
            - monthly_automation_cost(volume, run_cost))


def payback_months(build_cost: float, saving_per_month: float) -> float:
    assert saving_per_month > 0, "no savings -> no payback, automation not viable"
    return build_cost / saving_per_month


def break_even_monthly_volume(build_cost: float, saving_per_run: float,
                              horizon_months: int = 12) -> float:
    """Runs/month at which `horizon_months` of savings repay the build cost."""
    assert saving_per_run > 0
    return build_cost / (horizon_months * saving_per_run)


def outcome_statement(process: str, outcome: str, metric: str, target: str) -> str:
    return (f"Automate {process} so that {outcome}, measured by {metric}, "
            f"reaching {target}.")


STALL_QUESTIONS = [
    "Is there a single named owner with budget authority?",
    "Is the outcome stated as a business metric, not a task count?",
    "Does the pilot have a kill criterion and a date?",
    "Are the integration owners (IT/security) committed in writing?",
    "Is there a human-in-the-loop plan for the first 90 days?",
]


def stall_self_assessment(answers: list[bool]) -> tuple[int, str]:
    score = sum(answers)
    if score == len(STALL_QUESTIONS):
        verdict = "READY: stall risks addressed."
    elif score >= 3:
        verdict = "CAUTION: fix the 'no' answers before scaling."
    else:
        verdict = "STALL RISK: do not start building yet."
    return score, verdict


# ------------------------------------------------------------------- demo
def main() -> None:
    manual = monthly_manual_cost(VOLUME_PER_MONTH, MINUTES_PER_RUN,
                                 LOADED_WAGE_PER_HOUR, ERROR_RATE,
                                 REWORK_COST_PER_ERROR)
    auto = monthly_automation_cost(VOLUME_PER_MONTH, RUN_COST_PER_RUN)
    saving = monthly_savings(VOLUME_PER_MONTH, MINUTES_PER_RUN,
                             LOADED_WAGE_PER_HOUR, ERROR_RATE,
                             REWORK_COST_PER_ERROR, RUN_COST_PER_RUN)
    payback = payback_months(BUILD_COST, saving)
    per_run_saving = (cost_per_manual_run(MINUTES_PER_RUN, LOADED_WAGE_PER_HOUR)
                      + ERROR_RATE * REWORK_COST_PER_ERROR - RUN_COST_PER_RUN)
    breakeven = break_even_monthly_volume(BUILD_COST, per_run_saving)

    # Verifiable assertions on the worked example.
    assert abs(manual - 16250.0) < 1e-6, manual          # 15000 labor + 1250 rework
    assert abs(auto - 500.0) < 1e-6, auto
    assert abs(saving - 15750.0) < 1e-6, saving
    assert abs(payback - 12000.0 / 15750.0) < 1e-9, payback
    assert abs(breakeven - 12000.0 / (12 * 15.75)) < 1e-9, breakeven

    print("business_case: invoice-coding automation")
    print(f"  manual cost/month      : ${manual:,.2f}")
    print(f"  automation cost/month  : ${auto:,.2f}")
    print(f"  net saving/month       : ${saving:,.2f}")
    print(f"  payback period         : {payback:.3f} months (~{payback * 30.44:.1f} days)")
    print(f"  break-even volume      : {breakeven:.1f} runs/month over 12 months")
    print()
    print("  outcome statement:")
    print("   ", outcome_statement("invoice coding",
                                   "AP closes 2 days faster",
                                   "days to close", "3 days by Q2"))
    score, verdict = stall_self_assessment([True, True, False, True, True])
    print(f"  stall self-assessment  : {score}/{len(STALL_QUESTIONS)} — {verdict}")
    print("business_case demo: OK")


if __name__ == "__main__":
    main()
