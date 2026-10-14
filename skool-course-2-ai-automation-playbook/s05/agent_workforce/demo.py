"""s05 / agent_workforce — a digital team with supervision that pays for itself.

Lesson mapping: Section 5, Lessons 18-21 (agent roles, supervision patterns,
handoffs, the digital team).
What it does: simulates a role-based pipeline (researcher -> triager ->
drafter -> checker) passing structured handoff packages, then computes the
cost-optimal supervision sampling rate from error economics.
"""

from __future__ import annotations

# ------------------------------------------------------- handoff packages
REQUIRED_FIELDS = ("item_id", "payload", "provenance", "confidence")


def make_handoff(item_id: str, payload: dict, provenance: list[str],
                 confidence: float) -> dict:
    return {"item_id": item_id, "payload": payload,
            "provenance": provenance, "confidence": confidence}


def validate_handoff(package: dict) -> list[str]:
    """Checker role: every handoff must carry all four fields."""
    return [f for f in REQUIRED_FIELDS if f not in package]


ITEMS = [
    {"item_id": "q-101", "text": "invoice INV-2041 from Acme totals $4,120, due Friday"},
    {"item_id": "q-102", "text": "refund request #8812 customer claims double charge $89"},
    {"item_id": "q-103", "text": "vendor contract renewal Globex $12k/yr auto-renews Monday"},
]


def researcher(item: dict) -> dict:
    facts = [w for w in item["text"].split() if w[0].isupper() or w.replace(",", "").replace("$", "").replace(".", "").isdigit()]
    return make_handoff(item["item_id"], {"facts": facts, "raw": item["text"]},
                        ["researcher"], 0.82)


def triager(handoff: dict) -> dict:
    urgent = any(k in handoff["payload"]["raw"].lower()
                 for k in ("friday", "monday", "double charge"))
    payload = dict(handoff["payload"], priority="urgent" if urgent else "normal")
    return make_handoff(handoff["item_id"], payload,
                        handoff["provenance"] + ["triager"], 0.88)


def drafter(handoff: dict) -> dict:
    summary = f"[{handoff['payload']['priority']}] " + " ".join(handoff["payload"]["facts"][:6])
    payload = dict(handoff["payload"], draft=summary)
    return make_handoff(handoff["item_id"], payload,
                        handoff["provenance"] + ["drafter"], 0.91)


def checker(handoff: dict, threshold: float = 0.85) -> dict:
    missing = validate_handoff(handoff)
    assert not missing, f"handoff missing fields: {missing}"
    decision = "ship" if handoff["confidence"] >= threshold else "escalate"
    return {"item_id": handoff["item_id"], "decision": decision,
            "provenance": handoff["provenance"] + ["checker"]}


# ------------------------------------------------------- supervision math
def optimal_sample_rate(p_error: float, cost_per_error: float,
                        cost_per_review: float, coordination_cost: float) -> float:
    """Minimize total cost per item:
        C(r) = r*C_rev + (1-r)*p*C_err + r^2*C_coord
    Sampling catches errors before they cost; coordination overhead grows
    quadratically with review load. dC/dr = 0 gives the optimum, clipped
    to [0, 1]."""
    r = (p_error * cost_per_error - cost_per_review) / (2 * coordination_cost)
    return max(0.0, min(1.0, r))


def total_cost_per_item(r: float, p_error: float, cost_per_error: float,
                        cost_per_review: float, coordination_cost: float) -> float:
    return (r * cost_per_review + (1 - r) * p_error * cost_per_error
            + r * r * coordination_cost)


# Fixture: 8% error rate, $500 per escaped error, $5 per review, $50 coordination.
SAMPLER_FIXTURE = {"p_error": 0.08, "cost_per_error": 500.0,
                   "cost_per_review": 5.0, "coordination_cost": 50.0}
EXPECTED_RATE = 0.35  # (0.08*500 - 5) / (2*50)


def main() -> None:
    shipped, escalated = [], []
    for item in ITEMS:
        h = researcher(item)
        assert not validate_handoff(h)
        h = triager(h)
        assert not validate_handoff(h)
        h = drafter(h)
        assert not validate_handoff(h)
        assert set(h) >= set(REQUIRED_FIELDS)
        assert h["provenance"] == ["researcher", "triager", "drafter"]
        outcome = checker(h)
        (shipped if outcome["decision"] == "ship" else escalated).append(outcome["item_id"])

    rate = optimal_sample_rate(**SAMPLER_FIXTURE)
    assert abs(rate - EXPECTED_RATE) < 1e-9, rate
    cost_opt = total_cost_per_item(rate, **SAMPLER_FIXTURE)
    cost_none = total_cost_per_item(0.0, **SAMPLER_FIXTURE)
    cost_all = total_cost_per_item(1.0, **SAMPLER_FIXTURE)
    assert cost_opt < cost_none and cost_opt < cost_all, "optimum must beat the edges"

    print("agent_workforce: researcher -> triager -> drafter -> checker")
    print(f"  shipped: {shipped} | escalated: {escalated}")
    print("  every handoff carried item_id, payload, provenance, confidence")
    print(f"supervision sampler: optimal review rate = {rate:.0%} "
          f"(p=8%, $500/error, $5/review)")
    print(f"  cost/item: sample-none ${cost_none:.2f} | optimal ${cost_opt:.2f} "
          f"| sample-all ${cost_all:.2f}")
    print("agent_workforce demo: OK")


if __name__ == "__main__":
    main()
