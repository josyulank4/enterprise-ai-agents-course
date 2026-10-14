"""s11 / rollout — land it without breaking the org.

Lesson mapping: Section 11, Lessons 42-45 (rollout strategy, stakeholders,
training/docs, adoption measurement).
What it does: prints the rollout-plan, stakeholder-map and runbook templates,
then runs an adoption dashboard over simulated 90-day data that flags the
planted work-around team.
"""

from __future__ import annotations

# ------------------------------------------------- templates
ROLLOUT_PLAN = """\
ROLLOUT PLAN — {name}
Phase 1 PILOT (weeks 1-4): one team, one process, kill criterion set.
  Exit: outcome metric moves >= target AND override rate < 15%.
Phase 2 EXPAND (weeks 5-10): three more teams; runbook v1; on-call rotation.
  Exit: adoption >= 60% on all teams, no HIGH blast-radius incidents.
Phase 3 STANDARDIZE (weeks 11+): default for the process org-wide; old manual
  path retired; quarterly review against the business case.
"""

STAKEHOLDER_MAP = """\
STAKEHOLDER MAP — {name}
Sponsor:      ______________ (budget + air cover; weekly 15-min review)
Process owner: ______________ (accepts the outcome metric)
IT/Security:  ______________ (integration + secrets sign-off)
End users:    ______________ (pilot team first; train before expand)
Skeptic:      ______________ (loudest critic -> co-designer, not opponent)
"""

RUNBOOK = """\
RUNBOOK — {name}
Normal ops:  monitor dashboard daily; review queue SLA 4h; weekly error-budget check.
Degraded:    error rate > 2x baseline -> freeze auto-approve, route all to reviewers.
Rollback:    one-command revert to manual path; RTO 30 min; notify sponsor.
On-call:     primary ______, secondary ______; page on dead-letter growth.
"""


# ------------------------------------------------- adoption dashboard
# Simulated 90-day data per team: usage_rate, override_rate, satisfaction /10.
TEAMS_90D = {
    "team-atlas":   {"usage_rate": 0.82, "override_rate": 0.08, "satisfaction": 8.6},
    "team-beacon":  {"usage_rate": 0.71, "override_rate": 0.14, "satisfaction": 7.9},
    "team-cipher":  {"usage_rate": 0.64, "override_rate": 0.19, "satisfaction": 7.2},
    # Planted work-around team: barely uses the automation, overrides constantly.
    "team-phoenix": {"usage_rate": 0.12, "override_rate": 0.78, "satisfaction": 4.1},
}


def flag_workarounds(teams: dict[str, dict]) -> list[str]:
    """Flags teams with low usage AND high overrides: automation theater."""
    return [name for name, m in teams.items()
            if m["usage_rate"] < 0.30 and m["override_rate"] > 0.50]


def adoption_summary(teams: dict[str, dict]) -> dict:
    n = len(teams)
    return {"avg_usage": round(sum(m["usage_rate"] for m in teams.values()) / n, 3),
            "avg_override": round(sum(m["override_rate"] for m in teams.values()) / n, 3),
            "avg_satisfaction": round(sum(m["satisfaction"] for m in teams.values()) / n, 2)}


def main() -> None:
    name = "invoice-coding automation"
    for template in (ROLLOUT_PLAN, STAKEHOLDER_MAP, RUNBOOK):
        rendered = template.format(name=name)
        assert "{name}" not in rendered and name in rendered

    flagged = flag_workarounds(TEAMS_90D)
    assert flagged == ["team-phoenix"], flagged
    summary = adoption_summary(TEAMS_90D)

    print("rollout: templates")
    print(ROLLOUT_PLAN.format(name=name))
    print(STAKEHOLDER_MAP.format(name=name))
    print(RUNBOOK.format(name=name))
    print("adoption dashboard (simulated 90-day data):")
    for team, m in TEAMS_90D.items():
        mark = "  <-- WORK-AROUND TEAM" if team in flagged else ""
        print(f"  {team:>13}: usage {m['usage_rate']:.0%} | "
              f"override {m['override_rate']:.0%} | sat {m['satisfaction']}/10{mark}")
    print(f"  portfolio: usage {summary['avg_usage']:.0%} | "
          f"override {summary['avg_override']:.0%} | sat {summary['avg_satisfaction']}/10")
    print(f"flagged work-around teams: {flagged}")
    print("rollout demo: OK")


if __name__ == "__main__":
    main()
