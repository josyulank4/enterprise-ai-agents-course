"""s02 / bill-decomposer — split a month of spend into named drivers.

Lesson mapping: Section 2, Lessons 5-8.
What it does:
  1. Decomposes one month of a support copilot's spend into the nine
     driver categories of Lesson 6, with shares of the total.
  2. Flags shadow-spend candidates: material lines with no named
     owner (Lesson 6's shadow-spend problem).
  3. Computes cost per successful task at p50 and p95 from a sample of
     task costs — Lesson 7's headline metric, tail included.
"""

from __future__ import annotations

# One month of the support copilot: (line, driver category, USD, owner)
MONTH_ITEMS = (
    ("frontier chat tokens", "model tokens", 9840.00, "copilot-team"),
    ("small classifier tokens", "model tokens", 610.00, "copilot-team"),
    ("embedding calls", "embeddings", 1120.00, "search-team"),
    ("vector search queries", "retrieval & search", 1470.00, "search-team"),
    ("failed-call retries", "retries & failures", 890.00, "unknown"),
    ("agent tool steps", "agent steps", 2260.00, "copilot-team"),
    ("cache + vector storage", "storage & cache infra", 640.00, "platform"),
    ("eval runs + tracing", "evaluation & observability", 380.00, "platform"),
    ("adapter fine-tune job", "fine-tuning", 290.00, "copilot-team"),
    ("idle provisioned capacity", "idle capacity", 1140.00, "unknown"),
)

# Cost per successful task for 20 sampled tasks (USD); the last is the tail.
TASK_COSTS = [0.10 + 0.01 * i for i in range(19)] + [1.85]


def decompose(items=MONTH_ITEMS) -> dict:
    """Group line items into driver categories with totals and shares."""
    total = sum(amount for _, _, amount, _ in items)
    by_category: dict = {}
    for _, category, amount, _ in items:
        by_category[category] = by_category.get(category, 0.0) + amount
    rows = [
        {"category": cat, "amount": round(amt, 2),
         "share": round(amt / total, 4)}
        for cat, amt in sorted(by_category.items(),
                               key=lambda kv: kv[1], reverse=True)
    ]
    return {"total": round(total, 2), "categories": rows}


def shadow_spend(items=MONTH_ITEMS, min_amount: float = 500.0) -> list:
    """Material lines nobody owns — the shadow-spend candidates."""
    return [
        {"line": line, "category": category, "amount": amount}
        for line, category, amount, owner in items
        if owner in ("", "unknown") and amount >= min_amount
    ]


def percentile(values, p: float) -> float:
    """Nearest-rank percentile: the value at rank ceil(p/100 * n)."""
    ordered = sorted(values)
    rank = max(1, -(-len(ordered) * int(p * 100) // 10000))  # ceil, int-safe
    rank = min(rank, len(ordered))
    return ordered[rank - 1]


def task_metrics(costs=TASK_COSTS) -> dict:
    """Cost per successful task: mean, p50, p95 (Lesson 7's metric set)."""
    return {
        "mean": round(sum(costs) / len(costs), 4),
        "p50": round(percentile(costs, 50), 4),
        "p95": round(percentile(costs, 95), 4),
    }


def main() -> None:
    report = decompose()
    print(f"One month, decomposed — total ${report['total']:,.2f}:")
    for row in report["categories"]:
        print(f"  {row['category']:<28} ${row['amount']:>9,.2f}  "
              f"{100 * row['share']:5.1f}%")
    shadow = shadow_spend()
    shadow_total = sum(s["amount"] for s in shadow)
    print(f"Shadow-spend candidates (no named owner, >= $500): "
          f"{len(shadow)} lines, ${shadow_total:,.2f}")
    for s in shadow:
        print(f"  {s['line']:<28} ${s['amount']:>9,.2f}")
    m = task_metrics()
    print(f"Cost per successful task: mean ${m['mean']:.4f}  "
          f"p50 ${m['p50']:.4f}  p95 ${m['p95']:.4f}  "
          f"(worst sampled task $1.85 — the tail the mean hides)")
    print("bill-decomposer demo: OK")


if __name__ == "__main__":
    main()
