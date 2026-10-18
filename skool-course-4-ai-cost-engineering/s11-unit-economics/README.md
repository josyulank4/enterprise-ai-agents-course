# unit-economics (s11)

**Section 11 — Pricing, Forecasting, and Capacity · Lessons 42–45**

The unit is the price: fully-loaded unit cost and margin, the same
product repriced four ways over one meter, a forecast built from
drivers, and three futures with the decision taken from the worst.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `unit-economics demo: OK`.

## What it does

1. **The unit** (`avg_tasks`, `cost_per_user`, `gross_margin`): a
   70/25/5 population averages 77 tasks a month but tails at 380 —
   at $0.14 per completed task, $10.78 per average user and $53.20
   per heavy user. Flat price meets skewed cost; the tail decides.
2. **Four prices** (`compare_pricing`): seat $49 (78.0% average
   margin, **−8.6%** on the heavy user), usage $0.35/task (60.0%),
   hybrid $29 + $0.18/task (74.9%, tail-safe), credits $39 for 150
   (72.4%, tail billed as overage). Hybrid wins most often — a floor
   under a meter.
3. **The forecast** (`forecast_bill`, `forecast_quarters`): users ×
   sessions × tokens × price = $1,188.00 this quarter; growing users
   8% and tokens/session 3% per quarter gives $1,321.53, then
   $1,470.07.
4. **Three futures** (`three_futures`): base $1,283.04, surge
   $1,722.60, slump $1,009.80 in one quarter — and committed use
   sized to 680 users, 80% of the slump, never the likely case.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 42 — The Unit Is the Price: Gross-Margin Math | Fully-loaded cost per user, median and tail |
| Lesson 43 — Pricing Models Compared | `compare_pricing`'s four rows over one meter |
| Lesson 44 — A Forecast Built From Drivers | `forecast_quarters` growing each driver at its own rate |
| Lesson 45 — Capacity, Scenarios, and Committed Use | `three_futures` + the worst-future commitment rule |

## Key functions

- `avg_tasks(population)` / `cost_per_user(tasks, cost_per_task)` —
  the population's mean load and its fully-loaded cost.
- `gross_margin(price, cost)` — margin at one price/cost pair.
- `compare_pricing(population, cost_per_task)` — per model:
  `revenue_per_user`, `cost_per_user`, `margin`, `heavy_user_margin`.
- `forecast_bill(drivers)` — one period priced from its drivers.
- `forecast_quarters(base, growth, quarters)` — driver-grown bills.
- `three_futures(base)` — base/surge/slump bills plus
  `committed_use_users`, sized from the slump.
