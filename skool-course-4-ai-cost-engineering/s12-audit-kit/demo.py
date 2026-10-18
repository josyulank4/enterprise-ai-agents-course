"""s12 / audit-kit — the full audit over the Harborline estate.

Lesson mapping: Section 12, Lessons 46-48.
What it does:
  1. Builds the inventory register from the Harborline sample data:
     seven workloads — three the org chart knew, four it had
     forgotten (Lesson 46). Unclaimed rows are flagged, not filed.
  2. Attributes ninety days of spend and measures the untagged
     share: about a fifth of the money carries no name.
  3. Ranks the six findings by recoverable spend per unit of risk,
     each with its evidence (Lesson 47), and renders the one-page
     report: three numbers at the top, owners on every row.
  4. Emits the remediation plan — owner, date, expected saving —
     ordered so quick wins fund the structural work (Lesson 48).
"""

from __future__ import annotations

# Harborline's register: (workload, owner or "", 90-day spend USD)
REGISTER = (
    ("support-copilot", "A. Rao", 54200.0),
    ("doc-search", "M. Chen", 21800.0),
    ("ticket-triage", "A. Rao", 9400.0),
    ("legacy-summarizer", "", 6100.0),
    ("forgotten-etl-script", "", 4800.0),
    ("test-tenant-runner", "", 3900.0),
    ("shadow-dashboard", "", 2600.0),
)

# (title, recoverable USD/quarter, risk 1-5, owner, due, evidence)
FINDINGS = (
    ("spend nobody had tagged", 6100.0, 1, "M. Chen", "2026-11-06",
     "four register rows carry no owner; their keys still spend"),
    ("retries nobody owned", 5200.0, 1, "A. Rao", "2026-11-13",
     "retry share 11% of copilot calls, no cap, no backoff"),
    ("frontier model on trivial questions", 8900.0, 2, "A. Rao",
     "2026-11-27", "71% of frontier calls score difficulty <= 2"),
    ("repetition nobody cached", 7600.0, 2, "M. Chen", "2026-12-04",
     "38% of doc-search prompts repeat verbatim inside 24h"),
    ("capacity nobody switched off", 4300.0, 1, "M. Chen",
     "2026-11-06", "test-tenant runner idles at full size nights"),
    ("an unbounded agent", 0.0, 5, "A. Rao", "2026-12-18",
     "no step, token, or cost ceiling; priced as exposure, not "
     "saving — the ceiling is the finding"),
)


def inventory(register=REGISTER) -> dict:
    """The register with its claimed/unclaimed split (Lesson 46)."""
    unclaimed = [r for r in register if not r[1]]
    return {"workloads": len(register),
            "claimed": len(register) - len(unclaimed),
            "unclaimed": len(unclaimed),
            "unclaimed_names": [r[0] for r in unclaimed],
            "total_90d": round(sum(r[2] for r in register), 2),
            "unclaimed_spend": round(sum(r[2] for r in unclaimed), 2)}


def untagged_share(register=REGISTER) -> float:
    """Unclaimed spend as a share of the whole estate."""
    inv = inventory(register)
    return round(inv["unclaimed_spend"] / inv["total_90d"], 4)


def ranked_findings(findings=FINDINGS) -> list:
    """Findings ranked by recoverable spend per unit of risk."""
    rows = [{"title": t, "recoverable": rec, "risk": risk,
             "owner": owner, "due": due, "evidence": ev,
             "score": round(rec / risk, 2)}
            for t, rec, risk, owner, due, ev in findings]
    return sorted(rows, key=lambda r: -r["score"])


def recoverable_total(findings=FINDINGS) -> float:
    return round(sum(f[1] for f in findings), 2)


def one_page_report(register=REGISTER, findings=FINDINGS) -> str:
    """Lesson 47's one-pager: three numbers at the top, then the
    ranked findings with owners — readable in one sitting."""
    inv = inventory(register)
    lines = [
        "HARBORLINE AI COST AUDIT — ONE-PAGE REPORT",
        f"90-day spend: ${inv['total_90d']:,.0f} | untagged share: "
        f"{100 * untagged_share(register):.1f}% | recoverable per "
        f"quarter: ${recoverable_total(findings):,.0f}",
        f"Register: {inv['workloads']} workloads, {inv['unclaimed']} "
        f"unclaimed ({', '.join(inv['unclaimed_names'])})",
        "Findings, ranked by recoverable spend per unit of risk:",
    ]
    for i, f in enumerate(ranked_findings(findings), 1):
        lines.append(f"  {i}. {f['title']} — ${f['recoverable']:,.0f} "
                     f"recoverable, risk {f['risk']}, owner "
                     f"{f['owner']}, due {f['due']}")
    return "\n".join(lines)


def remediation_plan(findings=FINDINGS) -> list:
    """Owners, dates, expected savings — in ranked order (Lesson 48)."""
    return [{"action": f["title"], "owner": f["owner"],
             "due": f["due"], "expected_saving": f["recoverable"]}
            for f in ranked_findings(findings)]


def main() -> None:
    print(one_page_report())
    plan = remediation_plan()
    print(f"Remediation plan: {len(plan)} items, every one with an "
          f"owner and a date; quarterly re-audit set before the file "
          f"closes (Lesson 48)")
    print("audit-kit demo: OK")


if __name__ == "__main__":
    main()
