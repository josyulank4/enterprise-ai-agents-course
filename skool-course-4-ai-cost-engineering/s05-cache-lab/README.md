# cache-lab (s05)

**Section 5 — Caching and Batching That Actually Pay · Lessons 17–20**

A three-layer cache simulator over traffic with honest repeat
structure, the break-even formula computed with honestly loaded
infrastructure, and the batching drill.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `cache-lab demo: OK`.

## What it does

1. **Exact layer** (`simulate_exact`): 200 requests — 80 hits (40%)
   once normalisation rescues case/whitespace/punctuation variants;
   $4.00 of from-scratch answers becomes $2.48.
2. **Prefix layer** (`prefix_saving`): a stable 800-token prefix over
   10,000 calls at a 90% cached-input discount saves $21.60 — paid
   once instead of ten thousand times.
3. **Semantic layer** (`semantic_match`, `semantic_demo`): Jaccard
   token-set similarity; all 3 near-duplicate pairs match at ≥ 0.8 —
   and the approved/denied pair scores 0.67 similarity on opposite
   facts, which is why this layer ships narrow, gated, and reviewed.
4. **Break-even + batching** (`breakeven_hit_rate`, `batch_savings`):
   infrastructure ÷ (traffic × uncached cost) = 0.075 for the lab's
   numbers; 5,000 batched async requests bank $50.00 at half price.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 17 — Answer Once, Serve Many: Cache Economics | Hit rate deciding whether a feature funds itself |
| Lesson 18 — The Three Cache Layers | Exact, prefix, and semantic layers priced separately |
| Lesson 19 — Hit Rate, Break-Even, and What Good Looks Like | `breakeven_hit_rate` vs the traffic's offered rate |
| Lesson 20 — Batching and the Failure Modes of Cheap | The batching drill at a 50% window discount |

## Key functions

- `normalize(prompt)` — the canonical cache key form.
- `build_traffic()` — the deterministic 200-request sample.
- `simulate_exact(traffic)` — hits, hit rate, uncached vs cached cost.
- `prefix_saving(requests, prefix_tokens, input_price_per_m, discount)`
  — USD saved by the prefix layer.
- `semantic_match(a, b)` — Jaccard similarity of token sets.
- `breakeven_hit_rate(infra_monthly, requests, uncached_cost)` —
  Lesson 19's break-even formula.
- `batch_savings(n_requests, per_request, discount)` — batch savings.
