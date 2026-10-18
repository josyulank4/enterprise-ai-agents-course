"""s09 / budget-guard — budget tree, burn alerts, policy as code.

Lesson mapping: Section 9, Lessons 35-37.
What it does:
  1. Builds a budget tree by team x feature x environment, each cell
     with a named owner and a baseline budget (Lesson 35).
  2. Computes burn-rate projections and alert levels, and walks a
     runaway workload through them: on track -> warning -> soft
     limit -> hard limit, with the graceful-degradation step attached
     to each level (Lesson 36).
  3. Runs budget policy as code (Lesson 37): CI checks that refuse a
     change with unbounded max_tokens, a missing attribution tag, or
     a frontier-model dependency with no approval reference — loudly,
     with the violation named.
"""

from __future__ import annotations

# (team, feature, env) -> {"budget": USD/month, "owner": name}
BUDGET_TREE = {
    ("support", "copilot", "prod"): {"budget": 4000.0, "owner": "A. Rao"},
    ("support", "copilot", "dev"): {"budget": 300.0, "owner": "A. Rao"},
    ("platform", "search", "prod"): {"budget": 1500.0, "owner": "M. Chen"},
    ("platform", "batch", "prod"): {"budget": 900.0, "owner": "M. Chen"},
}

DEGRADATION = {
    "on_track": "full service",
    "warning": "full service; owner notified with the projection",
    "soft": "cache-first, route new traffic to the small tier",
    "hard": "queue non-urgent work, page the owner, serve cache only",
}


def burn_projection(spent: float, day: int, days_in_month: int = 30) -> float:
    """Month-end spend if today's burn rate simply continues."""
    return round(spent / day * days_in_month, 2)


def alert_level(spent: float, budget: float, day: int,
                days_in_month: int = 30) -> str:
    """Where this cell stands: hard at the budget, soft at 90%,
    warning when the projection crosses the budget, else on track."""
    if spent >= budget:
        return "hard"
    if spent >= 0.9 * budget:
        return "soft"
    if burn_projection(spent, day, days_in_month) > budget:
        return "warning"
    return "on_track"


def cell_status(cell, spent: float, day: int, tree=BUDGET_TREE) -> dict:
    info = tree[cell]
    level = alert_level(spent, info["budget"], day)
    return {"cell": cell, "owner": info["owner"], "budget": info["budget"],
            "spent": spent, "day": day,
            "projection": burn_projection(spent, day),
            "level": level, "action": DEGRADATION[level]}


def ci_check(change: dict, max_tokens_ceiling: int = 32000) -> list:
    """Policy as code (Lesson 37): the pipeline refuses what the
    budget forbids. Returns the list of violations (empty = pass)."""
    violations = []
    if change.get("max_tokens") is None or \
            change["max_tokens"] > max_tokens_ceiling:
        violations.append("unbounded max_tokens")
    if "feature" not in change.get("tags", {}):
        violations.append("missing attribution tag")
    if change.get("model") == "frontier" and not change.get("approval_ref"):
        violations.append("frontier model without approval reference")
    return violations


def main() -> None:
    cell = ("support", "copilot", "prod")
    print("The runaway workload meets the budget tree (Lesson 36):")
    for spent, day in ((900.0, 10), (2100.0, 12), (3900.0, 20),
                       (4050.0, 24)):
        st = cell_status(cell, spent, day)
        print(f"  day {day:>2}: spent ${spent:>7,.0f} of "
              f"${st['budget']:,.0f}, projection ${st['projection']:,.0f}"
              f" -> {st['level']:<8} action: {st['action']}")
    bad = {"max_tokens": None, "tags": {"team": "support"},
           "model": "frontier", "approval_ref": None}
    good = {"max_tokens": 4096, "tags": {"feature": "copilot"},
            "model": "frontier", "approval_ref": "COST-2026-114"}
    print(f"CI policy check, forbidden change: REFUSED — "
          f"{'; '.join(ci_check(bad))}")
    print(f"CI policy check, compliant change: PASS — "
          f"{ci_check(good) or 'no violations'}")
    print("budget-guard demo: OK")


if __name__ == "__main__":
    main()
