"""s02 / process_discovery — let the data reveal the work.

Lesson mapping: Section 2, Lessons 6-9 (candidates, discovery practice,
process/task mining, the automation scorecard).
What it does: parses a sample event log into a discovered process map, flags
the top rework-driven automation candidate, then scores candidates on the
automation scorecard and exports the ranked top three.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict

# ---------------------------------------------------------------- fixtures
# (case_id, activity, sequence). Designed so manual_data_entry has the most
# rework loops (3), validate has 2, manager_approval has 1.
EVENT_LOG = [
    ("A", "receive_order", 1), ("A", "manual_data_entry", 2),
    ("A", "validate", 3), ("A", "ship", 4),
    ("B", "receive_order", 1), ("B", "manual_data_entry", 2),
    ("B", "validate", 3), ("B", "manual_data_entry", 4),
    ("B", "validate", 5), ("B", "ship", 6),
    ("C", "receive_order", 1), ("C", "manual_data_entry", 2),
    ("C", "validate", 3), ("C", "manual_data_entry", 4),
    ("C", "manual_data_entry", 5), ("C", "validate", 6),
    ("C", "ship", 7),
    ("D", "receive_order", 1), ("D", "manual_data_entry", 2),
    ("D", "manager_approval", 3), ("D", "manager_approval", 4),
    ("D", "ship", 5),
]

CANDIDATES = [
    {"name": "manual_data_entry", "volume": 9, "frequency": 10, "pain": 8, "rule_fit": 9},
    {"name": "invoice_approval", "volume": 7, "frequency": 6, "pain": 7, "rule_fit": 4},
    {"name": "email_triage", "volume": 8, "frequency": 9, "pain": 6, "rule_fit": 5},
    {"name": "vendor_onboarding", "volume": 4, "frequency": 3, "pain": 9, "rule_fit": 6},
]

WEIGHTS = {"volume": 0.3, "frequency": 0.3, "pain": 0.2, "rule_fit": 0.2}

EXPECTED_TOP_CANDIDATE = "manual_data_entry"
EXPECTED_TOP_THREE = ["manual_data_entry", "email_triage", "invoice_approval"]


# ------------------------------------------------------------- discovery
def discover_process_map(log: list[tuple]) -> dict[tuple[str, str], int]:
    """Count direct transitions between consecutive activities per case."""
    by_case: dict[str, list[tuple]] = defaultdict(list)
    for case, activity, seq in log:
        by_case[case].append((seq, activity))
    transitions: Counter = Counter()
    for events in by_case.values():
        ordered = [a for _, a in sorted(events)]
        for a, b in zip(ordered, ordered[1:]):
            transitions[(a, b)] += 1
    return dict(transitions)


def rework_counts(log: list[tuple]) -> dict[str, int]:
    """Rework loops: extra occurrences of an activity inside one case."""
    by_case: dict[str, Counter] = defaultdict(Counter)
    for case, activity, _ in log:
        by_case[case][activity] += 1
    total: Counter = Counter()
    for counts in by_case.values():
        for activity, n in counts.items():
            if n > 1:
                total[activity] += n - 1
    return dict(total)


def top_rework_candidate(log: list[tuple]) -> tuple[str, int]:
    counts = rework_counts(log)
    name = max(counts, key=counts.get)
    return name, counts[name]


# ------------------------------------------------------------- scorecard
def score_candidate(candidate: dict, weights: dict = WEIGHTS) -> float:
    return sum(candidate[axis] * w for axis, w in weights.items())


def rank_candidates(candidates: list[dict], top_n: int = 3) -> list[dict]:
    ranked = sorted(candidates, key=lambda c: score_candidate(c), reverse=True)
    return [
        {"rank": i + 1, "name": c["name"], "score": round(score_candidate(c), 2)}
        for i, c in enumerate(ranked[:top_n])
    ]


# ------------------------------------------------------------------- demo
def main() -> None:
    process_map = discover_process_map(EVENT_LOG)
    rework = rework_counts(EVENT_LOG)
    top_name, top_loops = top_rework_candidate(EVENT_LOG)
    top_three = rank_candidates(CANDIDATES)

    assert top_name == EXPECTED_TOP_CANDIDATE, f"got {top_name}"
    assert top_loops == 3, top_loops
    assert [c["name"] for c in top_three] == EXPECTED_TOP_THREE, top_three
    assert process_map[("receive_order", "manual_data_entry")] == 4

    print("process_discovery: discovered process map (top transitions)")
    for (a, b), n in sorted(process_map.items(), key=lambda kv: -kv[1])[:5]:
        print(f"  {a} -> {b}: {n}x")
    print(f"rework loops per activity: {dict(sorted(rework.items(), key=lambda kv: -kv[1]))}")
    print(f"top automation candidate by rework: {top_name} ({top_loops} loops)")
    print("automation scorecard — top three:")
    print(json.dumps(top_three, indent=2))
    print("process_discovery demo: OK")


if __name__ == "__main__":
    main()
