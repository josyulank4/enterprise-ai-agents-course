# token-ledger (s03)

**Section 3 — Tokens Are the Currency · Lessons 9–12**

Token counting you can verify by hand, the per-request cost formula,
and the section's central demonstration: in a conversation, the
context is re-billed on every call.

## How to run

```bash
python demo.py
```

Standard library only. Ends with `token-ledger demo: OK`.

## What it does

1. **Counting** (`count_tokens`): a deterministic teaching tokenizer
   (words + punctuation) so students can audit every count; a real
   system swaps in its provider's tokenizer, the ledger math is the
   same.
2. **The formula** (`request_cost`): input × input price + output ×
   output price — note the asymmetry, output priced 5× input here.
3. **Re-billing** (`conversation_cost`): a 100-token system prompt and
   three turns; call inputs run 150 → 290 → 420 tokens, and the total
   is $0.00603. Call 3 costs more than call 1 for a shorter reply.
4. **Budgets + diagnosis** (`check_budget`, `diagnose`): prompt token
   budgets per workload, and the three token stories — context bloat,
   reasoning overflow, retry storm — named from a spend profile.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| Lesson 9 — What a Token Is and Why Prices Differ | `count_tokens` + the in/out price asymmetry |
| Lesson 10 — Context Is Re-Billed on Every Call | `conversation_cost`'s growing call inputs |
| Lesson 11 — The Per-Request Cost Formula | `request_cost` + `check_budget` prompt budgets |
| Lesson 12 — Long Context and Reasoning Tokens: Tradeoffs | `diagnose` names the dominant token story |

## Key functions

- `count_tokens(text)` — token count from the teaching tokenizer.
- `request_cost(input_tokens, output_tokens, in_price, out_price)` —
  one request's cost in USD.
- `conversation_cost(turns, system_tokens)` — (per-call rows, total)
  with full history re-sent per call.
- `check_budget(name, prompt_tokens, budgets)` — `(ok, over_by)`.
- `diagnose(profile)` — dominant story key: `"context_bloat"`,
  `"reasoning_overflow"`, or `"retry_storm"` — the starting diagnosis of the Lesson 12 diagnosis pack.
