"""s01 / cost-meter — price a sample day of traffic across model tiers.

Lesson mapping: Section 1, Lessons 1-4.
What it does:
  1. Prices individual requests with the per-request cost formula
     (input tokens x input price + output tokens x output price).
  2. Prices a full sample day of traffic for four workloads on three
     model tiers and prints where the money went — the question the
     team in Lesson 1's story could not answer from their invoice.
  3. Lists a workload's always-running meters (per-call, per-step,
     per-retrieval, per-retry) from its feature flags (Lesson 3).
"""

from __future__ import annotations

# USD per 1,000,000 tokens, (input, output) — sample rate card.
RATE_CARD = {
    "frontier": (15.00, 75.00),
    "standard": (3.00, 15.00),
    "small": (0.25, 1.25),
}

# One sample day: (workload, tier, calls, avg input tokens, avg output tokens)
SAMPLE_DAY = (
    ("support-copilot", "frontier", 4200, 2400, 620),
    ("doc-search", "standard", 9800, 1800, 340),
    ("agent-research", "standard", 1500, 5200, 900),
    ("ticket-triage", "small", 26000, 480, 120),
)


def price_request(tier: str, input_tokens: int, output_tokens: int) -> float:
    """Cost of one request: tokens x per-token price, summed in/out."""
    in_price, out_price = RATE_CARD[tier]
    return (input_tokens * in_price + output_tokens * out_price) / 1_000_000


def price_day(sample=SAMPLE_DAY) -> dict:
    """Price a day of traffic. Returns per-workload rows and the total."""
    rows = []
    total = 0.0
    for workload, tier, calls, avg_in, avg_out in sample:
        per_call = price_request(tier, avg_in, avg_out)
        cost = per_call * calls
        total += cost
        rows.append({
            "workload": workload,
            "tier": tier,
            "calls": calls,
            "input_tokens": calls * avg_in,
            "output_tokens": calls * avg_out,
            "cost_per_call": round(per_call, 6),
            "cost": round(cost, 2),
        })
    return {"rows": rows, "total": round(total, 2)}


def always_on_meters(loops: bool = False, retrieval: bool = False,
                     retries: bool = False) -> list:
    """The meters that run for a workload with these features (Lesson 3).

    Every workload has a per-call meter. Anything that loops adds a
    per-step meter, anything that searches adds a per-retrieval meter,
    and anything that can fail and retry adds a per-retry meter.
    """
    meters = ["per-call"]
    if loops:
        meters.append("per-step")
    if retrieval:
        meters.append("per-retrieval")
    if retries:
        meters.append("per-retry")
    return meters


def main() -> None:
    print("Sample day, priced per workload:")
    report = price_day()
    for row in report["rows"]:
        print(f"  {row['workload']:<16} {row['tier']:<9} "
              f"{row['calls']:>6,} calls  "
              f"${row['cost_per_call']:.4f}/call  ${row['cost']:>8.2f}")
    print(f"  {'TOTAL':<16} {'':<9} {'':>6}  {'':>11}  ${report['total']:>8.2f}")
    biggest = max(report["rows"], key=lambda r: r["cost"])
    print(f"Where the money went: {biggest['workload']} on the "
          f"{biggest['tier']} tier = ${biggest['cost']:.2f} of "
          f"${report['total']:.2f} "
          f"({100 * biggest['cost'] / report['total']:.1f}%)")
    print("Always-on meters for the agent-research workload "
          "(loops + retrieval + retries): "
          + ", ".join(always_on_meters(loops=True, retrieval=True,
                                       retries=True)))
    print("cost-meter demo: OK")


if __name__ == "__main__":
    main()
