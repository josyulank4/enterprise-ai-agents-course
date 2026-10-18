# breakeven (s07)

**Section 7 — GPU Economics and the Self-Hosting Break-Even · Lessons 26–30**

Both cost curves as arithmetic, a full week's utilisation the
proposal deck would have hidden, and the proposal audit that finds
the three omissions before the CFO does.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `breakeven demo: OK`.

## What it does

1. **The crossing** (`breakeven_volume`): $12,000 honest fixed ÷
   ($0.020 − $0.004) unit gap = **750,000 requests/month**. Below it
   the API line wins; above it, self-hosting does.
2. **Utilisation** (`weekly_utilisation`): a 168-hour sample week —
   peak 900/h, average 412.5/h — runs at **45.8%** of provisioned
   peak. The gap between the deck's number and the week's number is
   where bad capital requests are born.
3. **The audit** (`hidden_cost_audit`): the sample proposal states
   $8,600/mo and omits staffing ($2,400), maintenance ($800), and
   redundancy ($1,200). Honest fixed cost: $13,000 — which moves the
   crossing, which is the point of Lesson 29.
4. **The memo** (`decision_memo`): at 500k requests/mo → API
   ($10,000 vs $14,000); at 900k → self-host ($18,000 vs $15,600),
   with the hybrid note attached either way.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 26 — Two Cost Curves and Why They Cross | `api_monthly` / `selfhost_monthly` / `breakeven_volume` |
| Lesson 27 — Utilisation Is Everything | `weekly_utilisation` over the 168-hour week |
| Lesson 28 — The Self-Hosting Stack and Quantization | The marginal-cost line a quantized model lowers |
| Lesson 29 — The Hidden Costs Nobody Puts in the Proposal | `hidden_cost_audit`'s three priced omissions |
| Lesson 30 — The Break-Even Formula and Hybrid Patterns | `decision_memo` with the hybrid note |

## Key functions

- `api_monthly(requests, unit)` / `selfhost_monthly(requests, fixed, unit)`
  — the two curves at one volume.
- `breakeven_volume(fixed, api_unit, self_unit)` — the crossing.
- `weekly_utilisation(hours, capacity_per_hour)` — hours, peak,
  average, and utilisation of provisioned capacity.
- `hidden_cost_audit(proposal, audit_lines)` — stated total, the
  omission names, and the adjusted fixed cost.
- `decision_memo(monthly_requests, fixed)` — both lanes priced, the
  recommendation, and the hybrid note.
