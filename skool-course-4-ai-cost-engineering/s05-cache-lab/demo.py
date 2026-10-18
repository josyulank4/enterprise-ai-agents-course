"""s05 / cache-lab — three cache layers, break-even math, batching.

Lesson mapping: Section 5, Lessons 17-20.
What it does:
  1. Simulates an exact-match cache over sample traffic with real
     repeat structure, including case/whitespace/punctuation
     variants that normalisation alone rescues (Lesson 18).
  2. Prices the provider prompt-prefix layer: a stable prefix is
     re-bought at full price on every call unless cached (Lesson 18).
  3. Runs the semantic layer on near-duplicate pairs, gated by a
     token-set similarity threshold — and shows the pair it must
     refuse (near in words, opposite in fact).
  4. Computes the break-even hit rate (Lesson 19) and the batching
     discount drill (Lesson 20).
"""

from __future__ import annotations

import re

UNCACHED_COST = 0.02   # USD to answer one request from scratch
LOOKUP_COST = 0.001    # USD to serve one cached answer


def normalize(prompt: str) -> str:
    """Lowercase, collapse whitespace, drop trailing punctuation —
    the normalisation that alone is worth double-digit hit rate."""
    text = re.sub(r"\s+", " ", prompt.strip().lower())
    return text.rstrip("?.! ")


def build_traffic() -> list:
    """200 requests with honest repeat structure: 50 questions asked
    twice verbatim, 30 of them asked again as messy variants, and 70
    one-off questions no cache can help."""
    base = [f"question {i}" for i in range(50)]
    traffic = list(base)                                   # 50 first asks
    traffic += base                                        # 50 exact repeats
    traffic += [f"  {q.upper()} ?" for q in base[:30]]     # 30 variants
    traffic += [f"unique {i}" for i in range(70)]          # 70 one-offs
    return traffic


def simulate_exact(traffic) -> dict:
    """Exact-match layer: first sight is a miss, repeats are hits."""
    seen = set()
    hits = 0
    for prompt in traffic:
        key = normalize(prompt)
        if key in seen:
            hits += 1
        else:
            seen.add(key)
    misses = len(traffic) - hits
    uncached = len(traffic) * UNCACHED_COST
    cached = hits * LOOKUP_COST + misses * UNCACHED_COST
    return {"requests": len(traffic), "hits": hits, "misses": misses,
            "hit_rate": round(hits / len(traffic), 4),
            "uncached_cost": round(uncached, 4),
            "cached_cost": round(cached, 4),
            "saved": round(uncached - cached, 4)}


def prefix_saving(requests: int, prefix_tokens: int,
                  input_price_per_m: float = 3.00,
                  discount: float = 0.90) -> float:
    """USD saved by prompt-prefix caching over N requests: the stable
    prefix is paid once instead of N times (first call warms it)."""
    full = requests * prefix_tokens * input_price_per_m / 1_000_000
    with_cache = full * (1 - discount) + (
        prefix_tokens * input_price_per_m / 1_000_000) * discount
    return round(full - with_cache, 4)


def token_set(text: str) -> set:
    return set(normalize(text).split())


def semantic_match(a: str, b: str, threshold: float = 0.8) -> float:
    """Jaccard similarity of the two prompts' token sets."""
    sa, sb = token_set(a), token_set(b)
    return len(sa & sb) / len(sa | sb)


SEMANTIC_PAIRS = (
    ("how do i reset my password", "reset my password how do i"),
    ("what is the refund window", "refund window what is the"),
    ("cancel my subscription please", "please cancel my subscription"),
)


def semantic_demo(pairs=SEMANTIC_PAIRS, threshold: float = 0.8) -> dict:
    hits = sum(1 for a, b in pairs if semantic_match(a, b) >= threshold)
    return {"pairs": len(pairs), "hits": hits, "threshold": threshold}


def breakeven_hit_rate(infra_monthly: float, requests: int,
                       uncached_cost: float = UNCACHED_COST) -> float:
    """Lesson 19's formula: infrastructure / (traffic x uncached cost).
    Below this hit rate the cache loses money, however good it feels."""
    return round(infra_monthly / (requests * uncached_cost), 4)


def batch_savings(n_requests: int, per_request: float = UNCACHED_COST,
                  discount: float = 0.5) -> float:
    """USD saved by moving N requests into a batch window (Lesson 20):
    batch what nobody is waiting for, at roughly half price."""
    return round(n_requests * per_request * discount, 4)


def main() -> None:
    sim = simulate_exact(build_traffic())
    print(f"Exact layer over {sim['requests']} requests: "
          f"{sim['hits']} hits ({100 * sim['hit_rate']:.0f}%), "
          f"${sim['uncached_cost']:.2f} -> ${sim['cached_cost']:.2f}, "
          f"saved ${sim['saved']:.2f}")
    saved_prefix = prefix_saving(10000, 800)
    print(f"Prefix layer: 10,000 calls x 800 stable tokens saves "
          f"${saved_prefix:.2f} at a 90% cached-input discount")
    sem = semantic_demo()
    danger = semantic_match("refund approved for order 9",
                            "refund denied for order 9")
    print(f"Semantic layer: {sem['hits']}/{sem['pairs']} near-duplicate "
          f"pairs matched at >= {sem['threshold']}; the dangerous pair "
          f"(approved vs denied) scores {danger:.2f} — below the "
          f"serving threshold here, and the reason this layer also "
          f"keeps human spot-checks for pairs that score above it "
          f"(Lesson 18)")
    print(f"Break-even hit rate ($300 infra, 200k requests): "
          f"{breakeven_hit_rate(300, 200000):.3f} — the lab's traffic "
          f"offers {sim['hit_rate']:.2f}, so this cache pays")
    print(f"Batching drill: 5,000 async requests bank "
          f"${batch_savings(5000):.2f} at the 50% batch discount")
    print("cache-lab demo: OK")


if __name__ == "__main__":
    main()
