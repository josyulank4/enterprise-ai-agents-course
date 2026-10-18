"""s04 / model-router — tiered routing, threshold sweep, quality gate.

Lesson mapping: Section 4, Lessons 13-16.
What it does:
  1. Builds a 100-request golden set with known difficulty, the small
     model's correctness per request, and a confidence signal.
  2. Routes by confidence threshold: confident requests stay on the
     small model, the rest escalate to the frontier tier.
  3. Sweeps the threshold so the savings/quality trade-off is a curve,
     not an opinion (Lesson 15's threshold lab).
  4. Runs the golden-set quality gate (Lesson 16): certify the small
     model for production, or refuse it — with the evidence printed.
"""

from __future__ import annotations

SMALL_COST = 0.002     # USD per request on the small tier
FRONTIER_COST = 0.04   # USD per request on the frontier tier
SMALL_MAX_DIFFICULTY = 6  # the small model is correct up to difficulty 6


def build_golden_set(n: int = 100) -> list:
    """Deterministic golden set: difficulties cycle 0..9, confidence
    falls as difficulty rises, the small model is right up to its
    known ceiling. Mirrors the hand-labelled set from Lesson 13."""
    golden = []
    for i in range(n):
        difficulty = i % 10
        golden.append({
            "id": i,
            "difficulty": difficulty,
            "confidence": round(1.0 - 0.09 * difficulty, 2),
            "small_correct": difficulty <= SMALL_MAX_DIFFICULTY,
        })
    return golden


GOLDEN_SET = build_golden_set()


def route_tier(request: dict, threshold: float) -> str:
    """Cascade rule: small model unless confidence < threshold."""
    return "small" if request["confidence"] >= threshold else "frontier"


def evaluate(threshold: float, golden=GOLDEN_SET) -> dict:
    """Cost and accuracy of the cascade at one threshold."""
    cost = 0.0
    correct = 0
    escalated = 0
    for req in golden:
        tier = route_tier(req, threshold)
        if tier == "small":
            cost += SMALL_COST
            correct += 1 if req["small_correct"] else 0
        else:
            cost += FRONTIER_COST
            escalated += 1
            correct += 1  # frontier tier answers the hard tail correctly
    return {"threshold": threshold, "total_cost": round(cost, 4),
            "accuracy": round(correct / len(golden), 4),
            "escalation_rate": round(escalated / len(golden), 4)}


def sweep_thresholds(thresholds=(0.0, 0.3, 0.55, 0.8, 1.01), golden=GOLDEN_SET):
    """The threshold lab: one evaluate() row per threshold."""
    return [evaluate(t, golden) for t in thresholds]


def quality_gate(threshold: float, min_accuracy: float = 0.95,
                 golden=GOLDEN_SET) -> dict:
    """Certify or refuse the small model at this threshold (Lesson 16).

    Both outcomes are successes: a refusal with evidence is the gate
    working exactly as designed.
    """
    evidence = evaluate(threshold, golden)
    certified = evidence["accuracy"] >= min_accuracy
    return {"certified": certified, "min_accuracy": min_accuracy,
            "evidence": evidence}


def main() -> None:
    all_frontier = evaluate(1.01)
    all_small = evaluate(0.0)
    print(f"Baselines: all-frontier ${all_frontier['total_cost']:.2f} "
          f"at accuracy {all_frontier['accuracy']:.2f}; "
          f"all-small ${all_small['total_cost']:.2f} at accuracy "
          f"{all_small['accuracy']:.2f} — cheap and wrong on the tail")
    print("Threshold sweep (the Lesson 15 lab):")
    for row in sweep_thresholds():
        print(f"  threshold {row['threshold']:.2f}: "
              f"cost ${row['total_cost']:.2f}, "
              f"accuracy {row['accuracy']:.2f}, "
              f"escalation {100 * row['escalation_rate']:.0f}%")
    gate = quality_gate(0.55)
    print(f"Quality gate @0.55: certified={gate['certified']} "
          f"(accuracy {gate['evidence']['accuracy']:.2f} >= "
          f"{gate['min_accuracy']:.2f}, cost "
          f"${gate['evidence']['total_cost']:.2f} vs $4.00 all-frontier)")
    loose = quality_gate(0.0)
    print(f"Quality gate @0.00: certified={loose['certified']} — refused "
          f"with evidence: accuracy {loose['evidence']['accuracy']:.2f} "
          f"is below the floor")
    print("model-router demo: OK")


if __name__ == "__main__":
    main()
