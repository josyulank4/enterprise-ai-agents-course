"""s08 / hitl — humans where judgment lives, automation everywhere else.

Lesson mapping: Section 8, Lessons 30-33 (approval gates, reviewer UX,
exceptions, trust calibration).
What it does: runs 50 actions through an approval queue with calibrated
confidence thresholds and blast-radius ratings, renders a terminal reviewer
UI, catches a planted rubber-stamp reviewer, routes exceptions, and prints a
trust-calibration worksheet from a simulated 90-day history.
"""

from __future__ import annotations

AUTO_APPROVE_THRESHOLD = 0.85
N_ACTIONS = 50


def confidence(i: int) -> float:
    """Deterministic pseudo-confidence in [0.5, 1.0)."""
    return 0.5 + 0.5 * ((i * 37) % 100) / 100.0


def blast_radius(action: dict) -> str:
    impact = action["impact_usd"]
    if impact >= 10000:
        return "HIGH"
    if impact >= 1000:
        return "MEDIUM"
    return "LOW"


def build_actions(n: int = N_ACTIONS) -> list[dict]:
    return [{"action_id": f"a-{i:03d}", "confidence": confidence(i),
             "impact_usd": 500 * ((i * 13) % 40)}  # $0 .. $19,500
            for i in range(n)]


# ------------------------------------------------- reviewer simulation
def review_alice(action: dict) -> tuple[str, float]:
    """Careful reviewer: decides on merit, takes her time."""
    decision = "approve" if action["confidence"] >= 0.60 else "reject"
    seconds = 90.0 + (int(action["action_id"].split("-")[1]) % 60)
    return decision, seconds


def review_bob(action: dict) -> tuple[str, float]:
    """Planted rubber-stamper: approves everything in ~1.5 seconds."""
    return "approve", 1.5


def detect_rubber_stamps(reviews: dict[str, list[tuple[str, float]]]) -> list[str]:
    """Flags reviewers with median review time < 5s AND approval rate > 95%."""
    flagged = []
    for name, outcomes in reviews.items():
        times = sorted(s for _, s in outcomes)
        median = times[len(times) // 2]
        approve_rate = sum(1 for d, _ in outcomes if d == "approve") / len(outcomes)
        if median < 5.0 and approve_rate > 0.95:
            flagged.append(name)
    return flagged


# ------------------------------------------------- trust calibration
def trust_calibration_worksheet() -> list[dict]:
    """Simulated 90-day history: evidence accumulates, thresholds loosen."""
    weeks = []
    for w in range(13):
        approval_rate = round(0.55 + w * 0.03, 2)      # 0.55 -> 0.91
        override_rate = round(0.22 - w * 0.015, 3)      # 0.22 -> 0.04
        threshold = 0.95 if w < 4 else (0.90 if w < 9 else 0.85)
        weeks.append({"week": w + 1, "approval_rate": approval_rate,
                      "override_rate": override_rate, "threshold": threshold})
    return weeks


def main() -> None:
    actions = build_actions()
    auto_approved = [a for a in actions if a["confidence"] >= AUTO_APPROVE_THRESHOLD]
    queued = [a for a in actions if a["confidence"] < AUTO_APPROVE_THRESHOLD]
    assert len(auto_approved) + len(queued) == N_ACTIONS

    # Terminal reviewer UI: split the queue between the two reviewers.
    reviews: dict[str, list[tuple[str, float]]] = {"alice": [], "bob": []}
    decisions = {}
    for i, action in enumerate(queued):
        reviewer = "alice" if i % 2 == 0 else "bob"
        fn = review_alice if reviewer == "alice" else review_bob
        decision, seconds = fn(action)
        reviews[reviewer].append((decision, seconds))
        decisions[action["action_id"]] = (reviewer, decision, seconds)

    flagged = detect_rubber_stamps(reviews)
    assert flagged == ["bob"], f"rubber-stamp detector missed: {flagged}"

    # Exceptions: HIGH blast-radius queued items go to a specialist, not the line.
    exceptions = [a for a in queued if blast_radius(a) == "HIGH"]
    assert exceptions, "fixture must contain HIGH blast-radius exceptions"

    history = trust_calibration_worksheet()
    assert history[0]["threshold"] == 0.95 and history[-1]["threshold"] == 0.85
    assert history[-1]["approval_rate"] > history[0]["approval_rate"]

    print(f"hitl: {N_ACTIONS} actions | auto-approved {len(auto_approved)} "
          f"(conf >= {AUTO_APPROVE_THRESHOLD}) | queued {len(queued)}")
    print("terminal reviewer UI (first 5 queued):")
    for a in queued[:5]:
        reviewer, decision, seconds = decisions[a["action_id"]]
        print(f"  {a['action_id']} conf={a['confidence']:.2f} "
              f"blast={blast_radius(a):>6} -> {reviewer}: {decision} ({seconds:.0f}s)")
    print(f"rubber-stamp detector flagged: {flagged}")
    print(f"exception simulator: {len(exceptions)} HIGH blast-radius actions "
          f"routed to specialist queue")
    print("trust calibration (90-day simulated history): "
          f"threshold {history[0]['threshold']} -> {history[-1]['threshold']} as "
          f"approval rate {history[0]['approval_rate']} -> {history[-1]['approval_rate']}")
    print("hitl demo: OK")


if __name__ == "__main__":
    main()
