"""Governance and the capstone: catalogs, review boards, readiness.

Lessons 50-53 companion demo for *MCP Architecture* (Udemy Course 3).

  Lesson 50 — the internal tool catalog: every entry carries an owner,
  a review status, and a trust tier; a review board applies admission
  checks (security review present, owner named, no duplicate of an
  existing tool, cost estimated) as policy-as-code.
  Lesson 52/53 — the capstone design pack, scored by the production
  readiness checklist from Lesson 2: owners and go/no-go criteria per
  line; the readiness review returns a verdict with blockers named.

Run:  python -m governance.governance
"""

from __future__ import annotations

TRUST_TIERS = ["experimental", "team", "organization", "regulated"]


class CatalogEntry:
    def __init__(self, name: str, owner: str, tier: str,
                 security_reviewed: bool, cost_per_1k_calls: float,
                 description: str) -> None:
        self.name = name
        self.owner = owner
        self.tier = tier
        self.security_reviewed = security_reviewed
        self.cost_per_1k_calls = cost_per_1k_calls
        self.description = description


class ReviewBoard:
    """Lesson 50: admission checks as code, not as meetings."""

    def __init__(self, catalog: list[CatalogEntry]) -> None:
        self.catalog = catalog

    def review(self, entry: CatalogEntry) -> tuple[bool, list[str]]:
        findings = []
        if not entry.owner:
            findings.append("no accountable owner named")
        if not entry.security_reviewed:
            findings.append("security review not completed")
        if entry.cost_per_1k_calls <= 0:
            findings.append("no cost estimate provided")
        for existing in self.catalog:
            if existing.name == entry.name:
                findings.append(f"duplicates existing catalog tool '{entry.name}'")
        if entry.tier == "regulated" and not entry.security_reviewed:
            findings.append("regulated tier requires completed security review")
        return (not findings), findings

    def admit(self, entry: CatalogEntry) -> tuple[bool, list[str]]:
        ok, findings = self.review(entry)
        if ok:
            self.catalog.append(entry)
        return ok, findings


# --- Lessons 52/53: capstone design pack + readiness review ---

READINESS_SECTIONS = [
    "server inventory and tool surfaces",
    "transport and topology decisions",
    "enterprise connection plan",
    "client and host design",
    "security pack",
    "evaluation plan",
    "operations pack",
    "governance design",
]


def readiness_review(pack: dict) -> dict:
    """Each section needs content AND an owner; go requires all eight."""
    lines = []
    for section in READINESS_SECTIONS:
        entry = pack.get(section, {})
        has_content = bool(entry.get("summary"))
        has_owner = bool(entry.get("owner"))
        status = "GO" if (has_content and has_owner) else "BLOCKER"
        lines.append({"section": section, "status": status,
                      "has_content": has_content, "has_owner": has_owner})
    blockers = [l["section"] for l in lines if l["status"] == "BLOCKER"]
    return {"lines": lines, "blockers": blockers,
            "verdict": "GO" if not blockers else "NO-GO"}


def sample_pack(complete: bool) -> dict:
    owners = {
        "server inventory and tool surfaces": "platform team",
        "transport and topology decisions": "platform team",
        "enterprise connection plan": "integrations lead",
        "client and host design": "host team",
        "security pack": "security engineering",
        "evaluation plan": "AI quality lead",
        "operations pack": "SRE",
        "governance design": "AI governance board",
    }
    pack = {s: {"summary": f"{s}: designed and evidenced", "owner": o}
            for s, o in owners.items()}
    if not complete:
        pack["security pack"] = {"summary": "threat model drafted", "owner": ""}
        pack["evaluation plan"] = {"summary": "", "owner": "AI quality lead"}
    return pack


def main() -> None:
    print("== governance: catalog, review board, readiness review ==")
    catalog = [CatalogEntry("get_service_status", "platform team",
                            "organization", True, 0.40,
                            "Operational status for one service")]
    board = ReviewBoard(catalog)
    good = CatalogEntry("search_tickets", "support platform", "team",
                        True, 1.20, "Search tickets by state and team")
    ok, findings = board.admit(good)
    print(f"admission, complete entry: {ok} (catalog now {len(catalog)} tools)")
    weak = CatalogEntry("purge_everything", "", "regulated",
                        False, 0.0, "Deletes archives")
    ok, findings = board.admit(weak)
    print(f"admission, unowned unreviewed entry: {ok}")
    for finding in findings:
        print(f"  board finding: {finding}")

    review = readiness_review(sample_pack(complete=True))
    print(f"capstone readiness, complete pack: {review['verdict']} "
          f"({len(review['lines'])}/8 sections GO)")
    review = readiness_review(sample_pack(complete=False))
    print(f"capstone readiness, incomplete pack: {review['verdict']}")
    for blocker in review["blockers"]:
        print(f"  blocker: {blocker}")
    print("governance demo complete: a protocol is only as good as its discipline")


if __name__ == "__main__":
    main()
