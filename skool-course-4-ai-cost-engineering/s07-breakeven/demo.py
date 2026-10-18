"""s07 / breakeven — API vs self-host: two curves and why they cross.

Lesson mapping: Section 7, Lessons 26-30.
What it does:
  1. Draws both cost curves as numbers: the API's pure variable line
     and self-hosting's fixed-plus-marginal line, and computes the
     break-even volume where they cross (Lessons 26 and 30).
  2. Sweeps a full sample week hour by hour and computes the
     utilisation provisioned-peak capacity actually sees (Lesson 27)
     — the number proposal decks hide.
  3. Audits a sample proposal for its three omissions, prices them,
     and re-runs the comparison (Lesson 29).
  4. Emits a decision memo: lane recommendation at a given volume,
     including the quantized option and the hybrid note (Lesson 30).
"""

from __future__ import annotations

FIXED_MONTHLY = 12_000.0     # honest all-in self-host fixed cost, USD/mo
API_UNIT = 0.020             # USD per request on the API lane
SELF_UNIT = 0.004            # USD marginal per request self-hosted

# One sample day of hourly demand, repeated for a 7-day week (Lesson 27).
DAY_SHAPE = tuple([50] * 6 + [400] * 6 + [900] * 6 + [300] * 6)
WEEK_HOURS = DAY_SHAPE * 7

# The sample proposal from Lesson 29: realistic, so its omissions are
# realistic too. Lines the audit prices when missing: staffing,
# maintenance, redundancy — at these standard monthly rates.
PROPOSAL = {"hardware": 8000.0, "power & cooling": 600.0}
AUDIT_LINES = {"staffing (0.5 FTE platform)": 2400.0,
               "maintenance & spares": 800.0,
               "redundancy (second node)": 1200.0}


def api_monthly(requests: int, unit: float = API_UNIT) -> float:
    return round(requests * unit, 2)


def selfhost_monthly(requests: int, fixed: float = FIXED_MONTHLY,
                     unit: float = SELF_UNIT) -> float:
    return round(fixed + requests * unit, 2)


def breakeven_volume(fixed: float = FIXED_MONTHLY,
                     api_unit: float = API_UNIT,
                     self_unit: float = SELF_UNIT) -> float:
    """Lesson 30's formula: fixed / (api unit - self unit). Above
    this monthly volume the self-host line runs cheaper."""
    return round(fixed / (api_unit - self_unit), 2)


def weekly_utilisation(hours=WEEK_HOURS, capacity_per_hour: int = 900) -> dict:
    """Average demand vs provisioned peak across a full week."""
    avg = sum(hours) / len(hours)
    return {"hours": len(hours), "peak": max(hours),
            "average": round(avg, 2),
            "utilisation": round(avg / capacity_per_hour, 4)}


def hidden_cost_audit(proposal=PROPOSAL, audit_lines=AUDIT_LINES) -> dict:
    """Price the lines the proposal forgot; return the honest fixed
    cost and the omission list (Lesson 29's audit drill)."""
    omissions = [name for name in audit_lines if name not in proposal]
    stated = sum(proposal.values())
    adjusted = stated + sum(audit_lines[name] for name in omissions)
    return {"stated": round(stated, 2), "omissions": omissions,
            "adjusted_fixed": round(adjusted, 2)}


def decision_memo(monthly_requests: int,
                  fixed: float = FIXED_MONTHLY) -> dict:
    """A CFO-auditable recommendation at one volume (Lesson 30)."""
    crossing = breakeven_volume(fixed)
    if monthly_requests < crossing:
        lane = "api"
    else:
        lane = "self-host"
    return {"monthly_requests": monthly_requests,
            "breakeven_volume": crossing,
            "api_cost": api_monthly(monthly_requests),
            "selfhost_cost": selfhost_monthly(monthly_requests, fixed),
            "recommendation": lane,
            "hybrid_note": "keep bursty peaks on the API lane either "
                           "way; commit the stable floor only"}


def main() -> None:
    crossing = breakeven_volume()
    print(f"Break-even: ${FIXED_MONTHLY:,.0f} fixed / "
          f"(${API_UNIT:.3f} - ${SELF_UNIT:.3f}) = {crossing:,.0f} "
          f"requests/month")
    util = weekly_utilisation()
    print(f"Utilisation sweep: {util['hours']} hours, peak "
          f"{util['peak']}/h, average {util['average']}/h -> "
          f"utilisation {100 * util['utilisation']:.1f}% of the "
          f"provisioned peak (the deck would have quoted the peak)")
    audit = hidden_cost_audit()
    print(f"Proposal audit: stated ${audit['stated']:,.2f}/mo, "
          f"{len(audit['omissions'])} omissions priced "
          f"({', '.join(audit['omissions'])}) -> honest fixed "
          f"${audit['adjusted_fixed']:,.2f}/mo")
    for volume in (500_000, 900_000):
        memo = decision_memo(volume)
        print(f"Memo @ {volume:,}/mo: api ${memo['api_cost']:,.2f} vs "
              f"self-host ${memo['selfhost_cost']:,.2f} -> "
              f"{memo['recommendation']}")
    print("breakeven demo: OK")


if __name__ == "__main__":
    main()
