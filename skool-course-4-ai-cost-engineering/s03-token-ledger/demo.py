"""s03 / token-ledger — token counting, the per-request formula, budgets.

Lesson mapping: Section 3, Lessons 9-12.
What it does:
  1. Counts tokens with a small deterministic tokenizer so every
     number in the demo can be checked by hand (Lesson 9).
  2. Applies the per-request cost formula (Lesson 11).
  3. Prices a three-turn conversation and shows the Lesson 10 effect:
     context is re-billed on every call, so call 3 costs more than
     call 1 for a shorter reply.
  4. Checks prompt token budgets and diagnoses the three token
     stories (Lesson 12) from a workload's cost profile.
"""

from __future__ import annotations

import re

TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[^\sA-Za-z0-9]")

# USD per 1M tokens for the standard tier used throughout this demo.
IN_PRICE, OUT_PRICE = 3.00, 15.00

SYSTEM_TOKENS = 100
CONVERSATION = (  # (user tokens, reply tokens) per turn
    (50, 80),
    (60, 90),
    (40, 60),
)

PROMPT_BUDGETS = {"triage-classifier": 600, "support-answer": 2500,
                  "doc-summary": 8000}


def count_tokens(text: str) -> int:
    """Deterministic teaching tokenizer: words and punctuation marks."""
    return len(TOKEN_RE.findall(text))


def request_cost(input_tokens: int, output_tokens: int,
                 in_price: float = IN_PRICE,
                 out_price: float = OUT_PRICE) -> float:
    """The per-request cost formula (Lesson 11), USD."""
    return (input_tokens * in_price + output_tokens * out_price) / 1_000_000


def conversation_cost(turns=CONVERSATION, system_tokens: int = SYSTEM_TOKENS):
    """Price a conversation where all history is re-sent every call.

    Call i's input = system prompt + every earlier user/reply token
    pair + this turn's user tokens. Returns (per-call rows, total).
    """
    rows = []
    history = 0
    for i, (user, reply) in enumerate(turns, 1):
        call_input = system_tokens + history + user
        cost = request_cost(call_input, reply)
        rows.append({"call": i, "input_tokens": call_input,
                     "output_tokens": reply, "cost": round(cost, 6)})
        history += user + reply
    return rows, round(sum(r["cost"] for r in rows), 6)


def check_budget(name: str, prompt_tokens: int, budgets=PROMPT_BUDGETS):
    """(ok, over_by) for a prompt against its token budget (Lesson 11)."""
    budget = budgets[name]
    return (prompt_tokens <= budget, max(0, prompt_tokens - budget))


def diagnose(profile: dict) -> str:
    """Name the dominant token story from a cost profile (Lesson 12).

    profile maps story keys to their share of token spend:
    context_share, reasoning_share, retry_share.
    """
    key = max(profile, key=profile.get)
    return {
        "context_share": "context_bloat",
        "reasoning_share": "reasoning_overflow",
        "retry_share": "retry_storm",
    }[key]


def main() -> None:
    sample = "Hello, world! Your invoice has arrived."
    print(f"count_tokens({sample!r}) = {count_tokens(sample)}")
    rows, total = conversation_cost()
    print("Three-turn conversation, history re-billed every call:")
    for r in rows:
        print(f"  call {r['call']}: in {r['input_tokens']:>4} tokens, "
              f"out {r['output_tokens']:>3} tokens, ${r['cost']:.5f}")
    print(f"  conversation total: ${total:.5f} — call 3 costs more than "
          f"call 1 despite the shortest reply: the context is the bill")
    ok, over = check_budget("support-answer", 2840)
    print(f"Budget check 'support-answer' at 2,840 tokens: "
          f"ok={ok}, over by {over} tokens")
    story = diagnose({"context_share": 0.62, "reasoning_share": 0.23,
                      "retry_share": 0.15})
    print(f"Profile diagnosis (62% context): {story}")
    print("token-ledger demo: OK")


if __name__ == "__main__":
    main()
