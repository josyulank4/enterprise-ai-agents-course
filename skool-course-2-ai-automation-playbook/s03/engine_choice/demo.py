"""s03 / engine_choice — pick the right engine for the work.

Lesson mapping: Section 3, Lessons 10-13 (RPA, AI-native, head-to-head, hybrid).
What it does:
  1. judgment-boundary classifier: scriptable / judgment / human-only
  2. engine-decision tool: five-axis scoring -> recommended engine + reasoning
  3. RPA maintenance estimator: the hidden cost of UI-driven automation
"""

from __future__ import annotations

# ------------------------------------------------------- 1. classifier
# A step: structured_input (bool), variability 0-10, judgment (bool),
# regulated/safety_critical (bool).
FIXTURE_STEPS = [
    {"name": "copy PO number into ERP", "structured_input": True, "variability": 1,
     "judgment": False, "regulated": False, "expected": "scriptable"},
    {"name": "nightly CSV export", "structured_input": True, "variability": 0,
     "judgment": False, "regulated": False, "expected": "scriptable"},
    {"name": "triage support ticket", "structured_input": False, "variability": 8,
     "judgment": True, "regulated": False, "expected": "judgment"},
    {"name": "parse invoice PDF line items", "structured_input": False, "variability": 6,
     "judgment": True, "regulated": False, "expected": "judgment"},
    {"name": "approve wire transfer > $50k", "structured_input": True, "variability": 2,
     "judgment": True, "regulated": True, "expected": "human-only"},
]


def classify(step: dict) -> str:
    """The judgment boundary: regulated/safety work never automates fully;
    judgment or unstructured/variable work needs AI; the rest is scriptable."""
    if step.get("regulated") or step.get("safety_critical"):
        return "human-only"
    if step["judgment"] or not step["structured_input"] or step["variability"] >= 7:
        return "judgment"
    return "scriptable"


# ------------------------------------------------- 2. engine decision
AXES = ("input_structure", "volume", "variability", "exception_rate", "judgment_need")


def score_engines(axes: dict[str, float]) -> dict[str, float]:
    s = axes["input_structure"]
    v = axes["volume"]
    var = axes["variability"]
    exc = axes["exception_rate"]
    j = axes["judgment_need"]
    return {
        "RPA": 0.40 * s + 0.25 * v + 0.15 * (10 - var) + 0.10 * (10 - exc) + 0.10 * (10 - j),
        "Workflow script": 0.45 * s + 0.10 * v + 0.20 * (10 - var) + 0.15 * (10 - exc) + 0.10 * (10 - j),
        "AI agent": 0.15 * s + 0.20 * v + 0.20 * var + 0.15 * exc + 0.30 * j,
        "Human (no automation)": 0.50 * j + 0.30 * exc + 0.20 * var,
    }


ENGINE_REASONING = {
    "RPA": "structured, high-volume, low-variability UI work",
    "Workflow script": "structured, stable work with an API available",
    "AI agent": "variable inputs needing judgment within guardrails",
    "Human (no automation)": "judgment or regulated work humans must own",
}


def recommend_engine(axes: dict[str, float]) -> tuple[str, dict[str, float], str]:
    scores = score_engines(axes)
    winner = max(scores, key=scores.get)
    return winner, scores, ENGINE_REASONING[winner]


# High-volume structured invoice coding -> RPA is the expected recommendation.
DECISION_FIXTURE = {"input_structure": 9, "volume": 9, "variability": 2,
                    "exception_rate": 2, "judgment_need": 1}
EXPECTED_ENGINE = "RPA"


# ------------------------------------------------- 3. RPA maintenance
def rpa_annual_maintenance(ui_changes_per_year: int, hours_per_fix: float,
                           loaded_wage: float, license_cost: float) -> float:
    """RPA's hidden tax: every UI change breaks selectors; each break costs a fix."""
    return ui_changes_per_year * hours_per_fix * loaded_wage + license_cost


def main() -> None:
    labels = {s["name"]: classify(s) for s in FIXTURE_STEPS}
    for step in FIXTURE_STEPS:
        assert labels[step["name"]] == step["expected"], (step["name"], labels[step["name"]])

    engine, scores, reasoning = recommend_engine(DECISION_FIXTURE)
    assert engine == EXPECTED_ENGINE, scores

    maint = rpa_annual_maintenance(ui_changes_per_year=12, hours_per_fix=6,
                                   loaded_wage=75.0, license_cost=8000.0)
    assert abs(maint - 13400.0) < 1e-6, maint  # 12*6*75 + 8000

    print("engine_choice: judgment-boundary classifier")
    for step in FIXTURE_STEPS:
        print(f"  {labels[step['name']]:>11}  {step['name']}")
    print("engine decision (five-axis scoring):")
    for name, score in sorted(scores.items(), key=lambda kv: -kv[1]):
        print(f"  {name:>22}: {score:5.2f}")
    print(f"  -> recommended: {engine} ({reasoning})")
    print(f"RPA maintenance estimate: ${maint:,.0f}/yr (12 UI breaks x 6h x $75 + $8k license)")
    print("engine_choice demo: OK")


if __name__ == "__main__":
    main()
