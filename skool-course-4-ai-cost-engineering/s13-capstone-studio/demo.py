"""s13 / capstone-studio — the capstone audit pack, scored and dated.

Lesson mapping: Section 13, Lessons 49-50.
What it does:
  1. Defines the five-part capstone audit pack (Lesson 49) and
     checks a pack for completeness: an empty pack fails with all
     five parts named as missing; the filled sample passes.
  2. Scores an estate against the book's Appendix A cost-readiness
     checklist, area by area — the rubric the capstone is graded
     with.
  3. Builds the roadmap (Lesson 50): first audit date, first three
     levers in order, first budget tree — dated commitments, with
     the course's five durable formulas beside them.
"""

from __future__ import annotations

PACK_PARTS = (
    "workload and key register",
    "attribution views",
    "one-page report",
    "remediation plan",
    "checklist score",
)

# Appendix A readiness checklist, sample answers (True = in place).
CHECKLIST = {
    "metering": {"per-request cost recorded": True,
                 "per-step agent metering": True,
                 "token counts in code review": False,
                 "invoice decomposed monthly": True},
    "attribution": {"every request tagged": False,
                    "untagged share under 5%": False,
                    "four views reviewed monthly": True,
                    "owners named per workload": True},
    "budgets": {"budget tree by team/feature/env": True,
                "burn-rate alerts wired": True,
                "soft and hard limits set": False,
                "degradation paths written": True},
    "optimisation": {"router thresholds swept": True,
                     "cache break-even computed": True,
                     "batch windows for async work": True,
                     "bloat table reviewed": False},
    "governance": {"policy checks in CI": True,
                   "monthly review held": False,
                   "quarterly re-audit scheduled": True,
                   "savings ledger kept": True},
}

FIVE_FORMULAS = (
    "request cost = input tokens x input price + output tokens x output price",
    "conversation cost grows with re-billed context: price the path, not the call",
    "break-even volume = fixed cost / (api unit cost - self-host unit cost)",
    "cache break-even hit rate = infrastructure / (traffic x uncached cost)",
    "forecast = users x sessions per user x tokens per session x price per token",
)


def blank_pack() -> dict:
    """The five-part capstone pack, empty (Lesson 49's template)."""
    return {part: None for part in PACK_PARTS}


def fill_sample_pack() -> dict:
    """A filled sample pack: every part present and non-empty."""
    pack = blank_pack()
    pack["workload and key register"] = "7 workloads, 4 unclaimed"
    pack["attribution views"] = "feature / team / tenant / model"
    pack["one-page report"] = "three numbers, six findings, owners"
    pack["remediation plan"] = "6 items, dated, savings stated"
    pack["checklist score"] = "see score_checklist"
    return pack


def check_pack(pack: dict):
    """(complete, missing): a pack is complete when every one of the
    five parts is present and non-empty — complete enough for a peer
    to re-run the audit from the pack alone."""
    missing = [part for part in PACK_PARTS if not pack.get(part)]
    return (not missing, missing)


def score_checklist(answers=CHECKLIST) -> dict:
    """Per-area and overall readiness from Appendix A's checklist."""
    areas = {}
    yes = total = 0
    for area, items in answers.items():
        a_yes = sum(1 for v in items.values() if v)
        areas[area] = round(a_yes / len(items), 4)
        yes += a_yes
        total += len(items)
    return {"areas": areas, "overall": round(yes / total, 4),
            "passed_items": yes, "total_items": total}


def roadmap_plan(first_audit_date: str, first_levers,
                 budget_tree_cells: int) -> list:
    """Lesson 50's committed roadmap: dated, ordered, owned by dates
    the author is willing to be held to."""
    plan = [{"commitment": "first full cost audit",
             "date": first_audit_date}]
    for i, lever in enumerate(first_levers, 1):
        plan.append({"commitment": f"lever {i}: {lever}",
                     "date": first_audit_date})
    plan.append({"commitment":
                 f"first budget tree live ({budget_tree_cells} cells)",
                 "date": first_audit_date})
    plan.append({"commitment": "quarterly re-audit rhythm begins",
                 "date": first_audit_date})
    return plan


def main() -> None:
    complete, missing = check_pack(blank_pack())
    print(f"Empty pack: complete={complete}, missing "
          f"{len(missing)} parts — the template refuses to pretend")
    sample = fill_sample_pack()
    ok, _ = check_pack(sample)
    print(f"Filled sample pack: complete={ok} "
          f"({len(PACK_PARTS)} parts present)")
    score = score_checklist()
    print(f"Appendix A readiness: {score['passed_items']}/"
          f"{score['total_items']} items, overall "
          f"{100 * score['overall']:.0f}%")
    for area, frac in score["areas"].items():
        print(f"  {area:<13} {100 * frac:.0f}%")
    plan = roadmap_plan("2026-11-02",
                        ["context diet", "tier routing",
                         "prompt caching"], 4)
    print(f"Roadmap: {len(plan)} dated commitments from "
          f"{plan[0]['date']} — a roadmap without dates is a wish")
    print("The five durable formulas:")
    for formula in FIVE_FORMULAS:
        print(f"  {formula}")
    print("capstone-studio demo: OK")


if __name__ == "__main__":
    main()
