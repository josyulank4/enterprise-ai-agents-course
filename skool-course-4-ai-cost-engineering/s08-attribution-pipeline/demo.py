"""s08 / attribution-pipeline — per-request records, four views.

Lesson mapping: Section 8, Lessons 31-34.
What it does:
  1. Emits a sample month of per-request records, each stamped with
     feature, team, tenant, and model at the gateway (Lesson 32's
     record schema and tagging discipline).
  2. Rolls the same records into Lesson 34's four views — by feature,
     by team, by tenant, by model — and proves they are four views
     of the same money: every view sums to the same grand total.
  3. Applies the five-percent rule (Lessons 31-33): the share of
     spend carrying no name must be at most 5%. This estate starts
     at 8.3% — the gap is the section's first finding.
"""

from __future__ import annotations

UNTAGGED = "(untagged)"

# Sample month spec: (feature, team, tenant, model, requests, cost each)
# An empty feature marks traffic the gateway could not name.
MONTH_SPEC = (
    ("copilot", "support", "acme", "frontier", 400, 0.09),
    ("copilot", "support", "globex", "frontier", 250, 0.09),
    ("search", "platform", "acme", "standard", 800, 0.012),
    ("triage", "support", "initech", "small", 1200, 0.004),
    ("nightly-batch", "platform", "acme", "standard", 90, 0.30),
    ("", "", "", "frontier", 60, 0.15),
)


def make_record(req_id: str, feature: str, team: str, tenant: str,
                model: str, cost: float) -> dict:
    """One per-request record (Lesson 32's schema): the name is the
    attribution; a record without tags is a record without a name."""
    return {"id": req_id, "feature": feature, "team": team,
            "tenant": tenant, "model": model, "cost": round(cost, 4)}


def emit_sample_month(spec=MONTH_SPEC) -> list:
    """Expand the spec into individual per-request records."""
    records = []
    seq = 0
    for feature, team, tenant, model, n, cost_each in spec:
        for _ in range(n):
            seq += 1
            records.append(make_record(f"req-{seq:05d}", feature, team,
                                       tenant, model, cost_each))
    return records


def rollup(records, key: str) -> dict:
    """Total spend grouped by one tag; blank tags read as (untagged).

    Accumulate raw and round once at the end: per-record costs are
    sub-cent (0.012, 0.004), and rounding per step would quietly
    delete them — a metering bug this course exists to prevent.
    """
    totals: dict = {}
    for rec in records:
        name = rec[key] or UNTAGGED
        totals[name] = totals.get(name, 0.0) + rec["cost"]
    return {name: round(total, 2) for name, total in totals.items()}


def four_views(records) -> dict:
    """Lesson 34's four views of the same money."""
    return {key: rollup(records, key)
            for key in ("feature", "team", "tenant", "model")}


def untagged_share(records) -> float:
    """Share of spend whose feature tag is blank."""
    total = sum(r["cost"] for r in records)
    unnamed = sum(r["cost"] for r in records if not r["feature"])
    return round(unnamed / total, 4)


def five_percent_rule(records, limit: float = 0.05) -> dict:
    """The section's definition of done: at most 5% unnamed spend."""
    share = untagged_share(records)
    return {"untagged_share": share, "limit": limit,
            "passes": share <= limit}


def main() -> None:
    records = emit_sample_month()
    views = four_views(records)
    total = round(sum(r["cost"] for r in records), 2)
    print(f"Sample month: {len(records):,} records, ${total:.2f} total")
    for key, view in views.items():
        view_total = round(sum(view.values()), 2)
        top = max(view.items(), key=lambda kv: kv[1])
        print(f"  by {key:<7} sums to ${view_total:.2f}; largest: "
              f"{top[0]} ${top[1]:.2f}")
    rule = five_percent_rule(records)
    print(f"Five-percent rule: untagged share "
          f"{100 * rule['untagged_share']:.1f}% vs limit "
          f"{100 * rule['limit']:.0f}% — passes: {rule['passes']} "
          f"(this estate's starting line, Lesson 31)")
    print("attribution-pipeline demo: OK")


if __name__ == "__main__":
    main()
