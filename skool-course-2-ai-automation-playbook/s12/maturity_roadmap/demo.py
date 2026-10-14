"""s12 / maturity_roadmap — the autonomous enterprise, staged.

Lesson mapping: Section 12, Lessons 46-50 (maturity journey, autonomous
enterprise, three-year roadmap, capstone).
What it does: scores a five-stage maturity questionnaire into a domain map
with evidence gaps, prints the accountability-map and three-year-roadmap
templates, then runs the capstone checklist verifying every section artifact
in this repo is present.
"""

from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

STAGES = ["Manual", "Assisted", "Automated", "Orchestrated", "Autonomous"]

# The 13 section demos — the capstone verifies each shipped its artifacts.
EXPECTED_DEMOS = [
    "hello_automation", "business_case", "process_discovery", "engine_choice",
    "workflow_orchestration", "agent_workforce", "integrations",
    "data_pipelines", "hitl", "reliability", "cost_security", "rollout",
    "maturity_roadmap",
]

# Five assessment domains: (domain, self-score 1-5, evidence on file?)
ASSESSMENT = [
    ("process_discovery", 3, True),
    ("orchestration", 4, True),
    ("agent_workforce", 2, True),
    ("data_foundations", 2, False),   # evidence gap: claimed but undocumented
    ("governance", 1, False),         # evidence gap
]


def assess(responses: list[tuple[str, int, bool]]) -> dict[str, dict]:
    domain_map = {}
    for domain, score, evidence in responses:
        assert 1 <= score <= 5, domain
        domain_map[domain] = {"stage": STAGES[score - 1], "score": score,
                              "evidence": evidence}
    return domain_map


def evidence_gaps(domain_map: dict[str, dict], target_stage: int = 3) -> list[str]:
    """Domains below target stage, or claiming a stage with no evidence."""
    return [d for d, m in domain_map.items()
            if m["score"] < target_stage or not m["evidence"]]


ACCOUNTABILITY_MAP = """\
ACCOUNTABILITY MAP — automation program
Program owner:      ______________ (owns the outcome metrics)
Domain leads:       ______________ (one per maturity domain)
Automation on-call: ______________ (dead letters, rollbacks)
Human reviewers:    ______________ (approval queues, exceptions)
Auditor:            ______________ (quarterly: artifacts, evidence, budget)
Rule: one name per box. A box with two names has no owner.
"""

ROADMAP = """\
THREE-YEAR ROADMAP
Year 1 — PROVE:  pilot 3 processes; reach Automated in 2 domains;
  error budgets and approval queues live; business case re-verified quarterly.
Year 2 — SCALE:  expand to 10 processes; reach Orchestrated in 3 domains;
  feature pipelines fresh; cost per task falling quarter over quarter.
Year 3 — AUTONOMY: lights-out for standard processes; humans on exceptions
  and judgment only; Autonomous in 2+ domains with evidence on file.
"""


def capstone_checklist(repo_root: Path = REPO_ROOT) -> dict:
    """Every section must have shipped demo.py + README.md."""
    missing, present = [], []
    for demo in EXPECTED_DEMOS:
        section = next(repo_root.glob(f"s*/{demo}"), None)
        if section and (section / "demo.py").is_file() and (section / "README.md").is_file():
            present.append(demo)
        else:
            missing.append(demo)
    return {"present": present, "missing": missing, "passed": not missing}


def main() -> None:
    domain_map = assess(ASSESSMENT)
    gaps = evidence_gaps(domain_map)
    assert domain_map["orchestration"]["stage"] == "Orchestrated"
    assert domain_map["governance"]["stage"] == "Manual"
    assert gaps == ["agent_workforce", "data_foundations", "governance"], gaps

    capstone = capstone_checklist()
    assert capstone["passed"], f"missing artifacts: {capstone['missing']}"
    assert len(capstone["present"]) == 13

    print("maturity_roadmap: five-stage assessment")
    for domain, m in domain_map.items():
        gap = "  <-- EVIDENCE GAP" if domain in gaps else ""
        print(f"  {domain:>18}: {m['stage']:<12} (score {m['score']}/5, "
              f"evidence={'yes' if m['evidence'] else 'NO'}){gap}")
    print()
    print(ACCOUNTABILITY_MAP)
    print(ROADMAP)
    print(f"capstone checklist: {len(capstone['present'])}/13 section artifacts "
          f"present — PASS")
    print("maturity_roadmap demo: OK")


if __name__ == "__main__":
    main()
