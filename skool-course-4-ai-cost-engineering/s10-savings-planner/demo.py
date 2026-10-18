"""s10 / savings-planner — the ranked lever portfolio, in order.

Lesson mapping: Section 10, Lessons 38-41.
What it does:
  1. Scores the sample estate's levers by return per unit of risk
     and effort, and ranks them inside the course's family order:
     waste removal (quiet levers) first, substitution second,
     commercial levers last (Lessons 39-40).
  2. Applies the portfolio the way savings actually work — each
     lever takes its fraction of the remainder the previous levers
     left, never of the original bill (Lesson 38).
  3. Replays the Meridian workload: $48,000/month to $31,336 after
     the structural levers, $28,516 after the commercial lever —
     the book's "roughly thirty-one thousand", reproduced in code.
  4. Sequences the ranked levers into a ninety-day plan (Lesson 41).
"""

from __future__ import annotations

BASE_MONTHLY = 48_000.0  # the Meridian workload's starting bill (L41)

FAMILY_ORDER = {"quiet": 0, "substitution": 1, "commercial": 2}

# (name, family, fraction of remainder saved, engineering weeks, risk 1-5)
LEVERS = (
    ("context diet", "quiet", 0.10, 2, 1),
    ("prompt caching", "quiet", 0.08, 2, 1),
    ("batch the async work", "quiet", 0.045, 1, 1),
    ("retry discipline", "quiet", 0.04, 1, 1),
    ("tier routing", "substitution", 0.14, 4, 2),
    ("committed-use discount", "commercial", 0.09, 1, 3),
)


def lever_score(lever, base: float = BASE_MONTHLY) -> float:
    """Expected monthly saving per unit of risk x effort."""
    _, _, frac, weeks, risk = lever
    return round(base * frac / (risk * weeks), 2)


def rank_levers(levers=LEVERS, base: float = BASE_MONTHLY) -> list:
    """Family order first (quiet, substitution, commercial), then
    score descending — Lesson 40's sequence is law, not preference."""
    return sorted(levers,
                  key=lambda lv: (FAMILY_ORDER[lv[1]],
                                  -lever_score(lv, base), lv[0]))


def apply_portfolio(base: float, ordered) -> list:
    """Apply levers in order, each to the remainder. Returns the
    running-balance rows: (lever name, monthly after, saved so far)."""
    rows = []
    current = base
    for name, *_rest in ordered:
        frac = next(lv[2] for lv in LEVERS if lv[0] == name)
        current = round(current * (1 - frac), 2)
        rows.append({"lever": name, "monthly_after": current,
                     "saved_so_far": round(base - current, 2)})
    return rows


def ninety_day_plan(ordered) -> list:
    """Sequence ranked levers back to back from week 1 and bucket the
    starts into 30-day phases (Lesson 41's plan builder)."""
    plan = []
    week = 1
    for name, _family, _frac, weeks, _risk in ordered:
        plan.append({"lever": name, "start_week": week,
                     "phase": (week - 1) // 4 + 1,
                     "duration_weeks": weeks})
        week += weeks
    return plan


def main() -> None:
    ranked = rank_levers()
    print("Ranked lever list (return per unit of risk, family order):")
    for lv in ranked:
        print(f"  {lv[0]:<24} {lv[1]:<12} saves "
              f"{100 * lv[2]:4.1f}% of remainder, score "
              f"{lever_score(lv):>8,.0f}")
    rows = apply_portfolio(BASE_MONTHLY, ranked)
    print(f"Meridian replay from ${BASE_MONTHLY:,.0f}/month:")
    for row in rows:
        print(f"  after {row['lever']:<24} ${row['monthly_after']:>9,.2f}"
              f"  (saved ${row['saved_so_far']:,.2f})")
    structural = rows[-2]["monthly_after"]
    print(f"  structural levers land at ${structural:,.0f} — the book's "
          f"'roughly thirty-one thousand'; the commercial lever then "
          f"reprices only what remains")
    plan = ninety_day_plan(ranked)
    starts = ", ".join(f"{p['lever']} w{p['start_week']}" for p in plan)
    print(f"Ninety-day plan starts: {starts}")
    print("savings-planner demo: OK")


if __name__ == "__main__":
    main()
