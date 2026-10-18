"""s11 / unit-economics — unit cost, four prices, drivers, futures.

Lesson mapping: Section 11, Lessons 42-45.
What it does:
  1. Computes fully-loaded cost per user and gross margin, at the
     median user and at the heavy tail (Lesson 42).
  2. Reprices the same product, same meter, under four pricing
     models — seat, usage, hybrid, credits — and compares margin
     and tail exposure (Lesson 43).
  3. Forecasts from drivers, not from the invoice: users x sessions
     x tokens x price, two quarters out (Lesson 44).
  4. Runs three futures and takes the committed-use decision from
     the worst one (Lesson 45).
"""

from __future__ import annotations

COST_PER_TASK = 0.14  # fully-loaded USD per completed task (Lesson 42)

# Population mix: (share of users, tasks per user per month)
POPULATION = ((0.70, 40), (0.25, 120), (0.05, 380))


def avg_tasks(population=POPULATION) -> float:
    return round(sum(share * tasks for share, tasks in population), 2)


def cost_per_user(tasks: float, cost_per_task: float = COST_PER_TASK) -> float:
    return round(tasks * cost_per_task, 2)


def gross_margin(price: float, cost: float) -> float:
    """(price - fully-loaded cost) / price, per user."""
    return round((price - cost) / price, 4)


def compare_pricing(population=POPULATION,
                    cost_per_task: float = COST_PER_TASK) -> dict:
    """Four pricing models over the same meter (Lesson 43).

    Each row: revenue and margin at the average user, plus the
    heavy-tail user's margin — where flat prices go to die.
    """
    avg = avg_tasks(population)
    heavy_tasks = max(tasks for _, tasks in population)
    avg_cost = cost_per_user(avg, cost_per_task)
    heavy_cost = cost_per_user(heavy_tasks, cost_per_task)

    def row(revenue_avg, revenue_heavy):
        return {"revenue_per_user": round(revenue_avg, 2),
                "cost_per_user": avg_cost,
                "margin": gross_margin(revenue_avg, avg_cost),
                "heavy_user_margin": gross_margin(revenue_heavy,
                                                  heavy_cost)}

    return {
        "seat": row(49.00, 49.00),
        "usage": row(avg * 0.35, heavy_tasks * 0.35),
        "hybrid": row(29.00 + avg * 0.18, 29.00 + heavy_tasks * 0.18),
        "credits": row(39.00, 39.00 + (heavy_tasks - 150) * 0.30),
    }


def forecast_bill(drivers: dict) -> float:
    """One period's bill from its drivers (Lesson 44):
    users x sessions/user x tokens/session x price/token."""
    return round(drivers["users"] * drivers["sessions_per_user"]
                 * drivers["tokens_per_session"]
                 * drivers["price_per_token"], 2)


def forecast_quarters(base: dict, growth: dict, quarters: int = 2) -> list:
    """Grow each driver at its own rate, per quarter, and price it.
    Growth maps driver name -> quarterly multiplier."""
    rows = []
    current = dict(base)
    for q in range(1, quarters + 1):
        for name, mult in growth.items():
            current[name] = current[name] * mult
        rows.append({"quarter": q, "drivers": dict(current),
                     "bill": forecast_bill(current)})
    return rows


BASE_DRIVERS = {"users": 1000, "sessions_per_user": 22,
                "tokens_per_session": 9000, "price_per_token": 6e-6}
GROWTH = {"users": 1.08, "tokens_per_session": 1.03}


def three_futures(base: dict = BASE_DRIVERS) -> dict:
    """Base, surge, and slump in one quarter (Lesson 45), and the
    committed-use decision: sized from the worst future, never the
    likely one — commit to 80% of the slump's volume."""
    futures = {}
    for name, user_mult in (("base", 1.08), ("surge", 1.45),
                            ("slump", 0.85)):
        drivers = dict(base)
        drivers["users"] = base["users"] * user_mult
        futures[name] = {"drivers": drivers,
                         "bill": forecast_bill(drivers)}
    slump_users = futures["slump"]["drivers"]["users"]
    futures["committed_use_users"] = round(0.8 * slump_users, 2)
    return futures


def main() -> None:
    avg = avg_tasks()
    print(f"Population: average {avg:.0f} tasks/user/month, "
          f"heavy tail {max(t for _, t in POPULATION)} tasks")
    print(f"Cost per user at ${COST_PER_TASK:.2f}/task: average "
          f"${cost_per_user(avg):.2f}, heavy "
          f"${cost_per_user(380):.2f}")
    table = compare_pricing()
    print("Four prices, same meter:")
    for model, row in table.items():
        print(f"  {model:<8} revenue ${row['revenue_per_user']:>6.2f}  "
              f"margin {100 * row['margin']:5.1f}%  heavy-user margin "
              f"{100 * row['heavy_user_margin']:6.1f}%")
    quarters = forecast_quarters(BASE_DRIVERS, GROWTH)
    print(f"Driver forecast: this quarter "
          f"${forecast_bill(BASE_DRIVERS):,.2f}; "
          + "; ".join(f"Q+{q['quarter']} ${q['bill']:,.2f}"
                      for q in quarters))
    futures = three_futures()
    print("Three futures (one quarter): "
          + ", ".join(f"{name} ${futures[name]['bill']:,.2f}"
                      for name in ("base", "surge", "slump"))
          + f"; committed-use sized to "
            f"{futures['committed_use_users']:,.0f} users — the "
            f"slump's floor, per Lesson 45")
    print("unit-economics demo: OK")


if __name__ == "__main__":
    main()
