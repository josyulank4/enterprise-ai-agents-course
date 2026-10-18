"""Validation harness for the Skool Course 4 code repo.

16 numbered checks in the Course 3 style. Each demo runs end-to-end in
a fresh interpreter (so the demo's own assertions execute); key
behaviors are additionally re-verified at the API level against the
functions documented in each demo's README. On a full green run this
script writes RESULTS.md itself (check 16 verifies the docs; the
results file is written by main). Exit code 0 = green.

Usage:
    python validate.py
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

# (section dir, package name, success marker)
DEMOS = (
    ("s01-cost-meter", "cost-meter", "cost-meter demo: OK"),
    ("s02-bill-decomposer", "bill-decomposer", "bill-decomposer demo: OK"),
    ("s03-token-ledger", "token-ledger", "token-ledger demo: OK"),
    ("s04-model-router", "model-router", "model-router demo: OK"),
    ("s05-cache-lab", "cache-lab", "cache-lab demo: OK"),
    ("s06-bounded-agent", "bounded-agent", "bounded-agent demo: OK"),
    ("s07-breakeven", "breakeven", "breakeven demo: OK"),
    ("s08-attribution-pipeline", "attribution-pipeline",
     "attribution-pipeline demo: OK"),
    ("s09-budget-guard", "budget-guard", "budget-guard demo: OK"),
    ("s10-savings-planner", "savings-planner", "savings-planner demo: OK"),
    ("s11-unit-economics", "unit-economics", "unit-economics demo: OK"),
    ("s12-audit-kit", "audit-kit", "audit-kit demo: OK"),
    ("s13-capstone-studio", "capstone-studio", "capstone-studio demo: OK"),
)

results: list[tuple[str, str]] = []


def check(name: str, fn) -> None:
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 - harness reports the check + error
        results.append((name, f"FAIL: {exc}"))
    else:
        results.append((name, "PASS"))


def run_demo(section: str, marker: str) -> None:
    """Run `python demo.py` inside the demo directory."""
    proc = subprocess.run(
        [sys.executable, "demo.py"],
        cwd=REPO_ROOT / section,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, (
        f"{section}/demo.py exited {proc.returncode}\n"
        f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
    assert marker in proc.stdout, f"{section} missing marker {marker!r}:\n{proc.stdout}"


def load_demo(section: str, modname: str):
    """Import a demo.py by path (unique module name per demo)."""
    path = REPO_ROOT / section / "demo.py"
    spec = importlib.util.spec_from_file_location(modname, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module  # dataclasses resolve via sys.modules
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- checks
def check_01_structure() -> None:
    assert len(DEMOS) == 13, f"expected 13 demos, listed {len(DEMOS)}"
    for section, _, _ in DEMOS:
        d = REPO_ROOT / section
        assert (d / "demo.py").is_file(), f"missing {section}/demo.py"
        assert (d / "README.md").is_file(), f"missing {section}/README.md"
    for name in ("requirements.txt", ".gitignore", "LICENSE", "README.md",
                 "validate.py"):
        assert (REPO_ROOT / name).is_file(), f"missing root file {name}"


def check_02_s01() -> None:
    run_demo("s01-cost-meter", "cost-meter demo: OK")
    m = load_demo("s01-cost-meter", "s01_cm")
    assert m.price_request("frontier", 2400, 620) == 0.0825
    report = m.price_day()
    assert report["total"] == 500.07, report["total"]
    biggest = max(report["rows"], key=lambda r: r["cost"])
    assert biggest["workload"] == "support-copilot"
    assert biggest["cost"] == 346.50
    assert m.always_on_meters() == ["per-call"]
    assert m.always_on_meters(loops=True, retrieval=True, retries=True) == [
        "per-call", "per-step", "per-retrieval", "per-retry"]


def check_03_s02() -> None:
    run_demo("s02-bill-decomposer", "bill-decomposer demo: OK")
    m = load_demo("s02-bill-decomposer", "s02_bd")
    report = m.decompose()
    assert report["total"] == 18640.00, report["total"]
    assert len(report["categories"]) == 9
    assert report["categories"][0]["category"] == "model tokens"
    assert report["categories"][0]["amount"] == 10450.00
    shadow = m.shadow_spend()
    assert len(shadow) == 2, shadow
    assert sum(s["amount"] for s in shadow) == 2030.00
    metrics = m.task_metrics()
    assert metrics == {"mean": 0.273, "p50": 0.19, "p95": 0.28}, metrics


def check_04_s03() -> None:
    run_demo("s03-token-ledger", "token-ledger demo: OK")
    m = load_demo("s03-token-ledger", "s03_tl")
    assert m.count_tokens("Hello, world!") == 4
    assert m.request_cost(2000, 500) == 0.0135
    rows, total = m.conversation_cost()
    assert [r["input_tokens"] for r in rows] == [150, 290, 420], rows
    assert total == 0.00603, total
    assert m.check_budget("support-answer", 2840) == (False, 340)
    assert m.check_budget("support-answer", 2400) == (True, 0)
    assert m.diagnose({"context_share": 0.62, "reasoning_share": 0.23,
                       "retry_share": 0.15}) == "context_bloat"
    assert m.diagnose({"context_share": 0.10, "reasoning_share": 0.30,
                       "retry_share": 0.60}) == "retry_storm"


def check_05_s04() -> None:
    run_demo("s04-model-router", "model-router demo: OK")
    m = load_demo("s04-model-router", "s04_mr")
    assert len(m.GOLDEN_SET) == 100
    all_small = m.evaluate(0.0)
    assert all_small["total_cost"] == 0.20, all_small
    assert all_small["accuracy"] == 0.70, all_small
    cascade = m.evaluate(0.55)
    assert cascade["total_cost"] == 1.72, cascade
    assert cascade["accuracy"] == 1.00, cascade
    assert cascade["escalation_rate"] == 0.40, cascade
    assert m.evaluate(1.01)["total_cost"] == 4.00
    assert m.quality_gate(0.55)["certified"] is True
    assert m.quality_gate(0.0)["certified"] is False


def check_06_s05() -> None:
    run_demo("s05-cache-lab", "cache-lab demo: OK")
    m = load_demo("s05-cache-lab", "s05_cl")
    sim = m.simulate_exact(m.build_traffic())
    assert sim["requests"] == 200 and sim["hits"] == 80, sim
    assert sim["hit_rate"] == 0.40, sim
    assert sim["cached_cost"] == 2.48 and sim["saved"] == 1.52, sim
    assert m.prefix_saving(10000, 800) == 21.5978
    assert m.semantic_demo()["hits"] == 3
    danger = m.semantic_match("refund approved for order 9",
                              "refund denied for order 9")
    assert abs(danger - 4 / 6) < 1e-9, danger
    assert m.breakeven_hit_rate(300, 200000) == 0.075
    assert m.batch_savings(5000) == 50.00


def check_07_s06() -> None:
    run_demo("s06-bounded-agent", "bounded-agent demo: OK")
    m = load_demo("s06-bounded-agent", "s06_ba")
    assert m.step_cost() == 0.021
    unb = m.run_unbounded()
    assert unb["steps"] == 36 and unb["cost"] == 0.756, unb
    bnd = m.run_bounded()
    assert bnd["steps"] == 23 and bnd["cost"] == 0.483, bnd
    assert bnd["stop_reason"] == "max_cost_budget", bnd
    assert bnd["partial_result"] is True and bnd["completed"] is False
    table = m.context_bloat_table()
    assert table[(32000, 60)] == 5.76, table[(32000, 60)]
    assert table[(8000, 25)] == 0.60


def check_08_s07() -> None:
    run_demo("s07-breakeven", "breakeven demo: OK")
    m = load_demo("s07-breakeven", "s07_be")
    assert m.breakeven_volume() == 750000.00
    assert m.api_monthly(500000) == 10000.00
    assert m.selfhost_monthly(900000) == 15600.00
    util = m.weekly_utilisation()
    assert util["hours"] == 168 and util["peak"] == 900, util
    assert util["average"] == 412.5 and util["utilisation"] == 0.4583, util
    audit = m.hidden_cost_audit()
    assert audit["stated"] == 8600.00, audit
    assert len(audit["omissions"]) == 3, audit
    assert audit["adjusted_fixed"] == 13000.00, audit
    assert m.decision_memo(500000)["recommendation"] == "api"
    assert m.decision_memo(900000)["recommendation"] == "self-host"


def check_09_s08() -> None:
    run_demo("s08-attribution-pipeline", "attribution-pipeline demo: OK")
    m = load_demo("s08-attribution-pipeline", "s08_ap")
    records = m.emit_sample_month()
    assert len(records) == 2800, len(records)
    views = m.four_views(records)
    for key, view in views.items():
        assert round(sum(view.values()), 2) == 108.90, (key, view)
    assert views["feature"]["copilot"] == 58.50
    assert views["feature"][m.UNTAGGED] == 9.00
    assert m.untagged_share(records) == 0.0826
    rule = m.five_percent_rule(records)
    assert rule["passes"] is False and rule["limit"] == 0.05


def check_10_s09() -> None:
    run_demo("s09-budget-guard", "budget-guard demo: OK")
    m = load_demo("s09-budget-guard", "s09_bg")
    assert m.burn_projection(2100.0, 12) == 5250.00
    assert m.alert_level(900.0, 4000.0, 10) == "on_track"
    assert m.alert_level(2100.0, 4000.0, 12) == "warning"
    assert m.alert_level(3900.0, 4000.0, 20) == "soft"
    assert m.alert_level(4050.0, 4000.0, 24) == "hard"
    bad = {"max_tokens": None, "tags": {"team": "support"},
           "model": "frontier", "approval_ref": None}
    assert m.ci_check(bad) == ["unbounded max_tokens",
                               "missing attribution tag",
                               "frontier model without approval reference"]
    good = {"max_tokens": 4096, "tags": {"feature": "copilot"},
            "model": "frontier", "approval_ref": "COST-2026-114"}
    assert m.ci_check(good) == []
    status = m.cell_status(("support", "copilot", "prod"), 2100.0, 12)
    assert status["level"] == "warning" and status["owner"] == "A. Rao"


def check_11_s10() -> None:
    run_demo("s10-savings-planner", "savings-planner demo: OK")
    m = load_demo("s10-savings-planner", "s10_sp")
    ranked = m.rank_levers()
    assert ranked[0][0] == "context diet", ranked[0]
    assert ranked[-1][0] == "committed-use discount", ranked[-1]
    families = [m.FAMILY_ORDER[lv[1]] for lv in ranked]
    assert families == sorted(families), families
    rows = m.apply_portfolio(m.BASE_MONTHLY, ranked)
    assert rows[-2]["monthly_after"] == 31336.08, rows[-2]
    assert rows[-1]["monthly_after"] == 28515.83, rows[-1]
    plan = m.ninety_day_plan(ranked)
    assert len(plan) == 6 and plan[0]["start_week"] == 1, plan
    assert plan[-1]["lever"] == "committed-use discount"


def check_12_s11() -> None:
    run_demo("s11-unit-economics", "unit-economics demo: OK")
    m = load_demo("s11-unit-economics", "s11_ue")
    assert m.avg_tasks() == 77.0
    assert m.cost_per_user(77) == 10.78
    assert m.cost_per_user(380) == 53.20
    table = m.compare_pricing()
    assert table["seat"]["margin"] == 0.78, table["seat"]
    assert table["seat"]["heavy_user_margin"] == -0.0857, table["seat"]
    assert table["hybrid"]["revenue_per_user"] == 42.86, table["hybrid"]
    assert table["usage"]["margin"] == 0.60, table["usage"]
    assert m.forecast_bill(m.BASE_DRIVERS) == 1188.00
    quarters = m.forecast_quarters(m.BASE_DRIVERS, m.GROWTH)
    assert [q["bill"] for q in quarters] == [1321.53, 1470.07], quarters
    futures = m.three_futures()
    assert futures["slump"]["bill"] == 1009.80, futures["slump"]
    assert futures["committed_use_users"] == 680.00, futures


def check_13_s12() -> None:
    run_demo("s12-audit-kit", "audit-kit demo: OK")
    m = load_demo("s12-audit-kit", "s12_ak")
    inv = m.inventory()
    assert inv["workloads"] == 7 and inv["unclaimed"] == 4, inv
    assert inv["total_90d"] == 102800.00, inv
    assert m.untagged_share() == 0.1693
    assert m.recoverable_total() == 32100.00
    ranked = m.ranked_findings()
    assert ranked[0]["title"] == "spend nobody had tagged", ranked[0]
    assert ranked[-1]["title"] == "an unbounded agent", ranked[-1]
    report = m.one_page_report()
    assert report.startswith("HARBORLINE AI COST AUDIT"), report[:60]
    assert "$102,800" in report and "$32,100" in report
    plan = m.remediation_plan()
    assert len(plan) == 6
    assert all(p["owner"] and p["due"] for p in plan)


def check_14_s13() -> None:
    run_demo("s13-capstone-studio", "capstone-studio demo: OK")
    m = load_demo("s13-capstone-studio", "s13_cs")
    complete, missing = m.check_pack(m.blank_pack())
    assert complete is False
    assert set(missing) == set(m.PACK_PARTS), missing
    assert m.check_pack(m.fill_sample_pack()) == (True, [])
    score = m.score_checklist()
    assert score["passed_items"] == 14 and score["total_items"] == 20
    assert score["overall"] == 0.70, score
    assert score["areas"]["attribution"] == 0.50, score["areas"]
    plan = m.roadmap_plan("2026-11-02", ["context diet", "tier routing",
                                         "prompt caching"], 4)
    assert len(plan) == 6 and plan[0]["date"] == "2026-11-02", plan
    assert len(m.FIVE_FORMULAS) == 5


SECRET_PATTERNS = [re.compile(p, re.IGNORECASE) for p in (
    r"password\s*=\s*[\"'][^\"']+[\"']",
    r"passwd\s*=\s*[\"'][^\"']+[\"']",
    r"secret\s*=\s*[\"'][^\"']+[\"']",
    r"api[_-]?key\s*=\s*[\"'][^\"']+[\"']",
    r"token\s*=\s*[\"'][^\"']{8,}[\"']",
)]


def check_15_no_secrets() -> None:
    hits = []
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in {".py", ".md", ".txt", ".ini"}:
            continue
        if path.name in {"RESULTS.md"}:
            continue
        for i, line in enumerate(path.read_text().splitlines(), 1):
            if line.strip().startswith("#"):
                continue
            if any(p.search(line) for p in SECRET_PATTERNS):
                hits.append(f"{path.relative_to(REPO_ROOT)}:{i}: {line.strip()}")
    assert not hits, "hardcoded secrets found:\n" + "\n".join(hits)


def check_16_docs() -> None:
    """README documents every demo + lesson mapping (RESULTS.md is written
    by main() itself, right after this check passes)."""
    readme = (REPO_ROOT / "README.md").read_text()
    for section, pkg, _ in DEMOS:
        assert pkg in readme, f"README missing demo {pkg}"
        assert section in readme, f"README missing path {section}"
    assert readme.count("Lesson") >= 50, "README lesson mapping looks thin"


# ------------------------------------------------------------- RESULTS.md
def write_results() -> Path:
    ist = timezone(timedelta(hours=5, minutes=30))
    stamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M IST")
    py = sys.version.split()[0]
    failed = [n for n, s in results if s.startswith("FAIL")]
    lines = [
        "# Validation Results — Skool Course 4 Code Repo",
        "",
        "Course: **AI Cost Engineering: Control Production AI Spend** (Skool-exclusive)",
        "Repo: `~/workspace/udemy-skool/skool-course-4-ai-cost-engineering/code-repo/`",
        f"Date of validated run: {stamp}",
        f"Environment: Python {py}, standard library only (matches `requirements.txt`)",
        "",
        "## Command run",
        "",
        "```bash",
        "cd ~/workspace/udemy-skool/skool-course-4-ai-cost-engineering/code-repo",
        "python validate.py",
        "```",
        "",
        "`validate.py` runs each of the 13 demos end-to-end in a fresh interpreter",
        "(so every demo's own assertions execute), re-verifies key behaviors at the",
        "API level, runs the repo-wide secrets scan, and checks the docs. Exit",
        "code 0 = green. This file was written by the validation run itself.",
        "",
        "## Result: " + ("ALL GREEN" if not failed else "FAILURES PRESENT"),
        "",
        "```",
    ]
    for name, status in results:
        lines.append(f"[{status.split(':')[0]:4s}] {name}")
    if failed:
        lines.append(f"{len(failed)} CHECK(S) FAILED")
    else:
        lines.append(f"ALL CHECKS PASSED ({len(results)}/16 green)")
    lines += ["```", "",
              "Every demo was also run individually during development with",
              "`python demo.py` inside its directory; each ends with its own",
              "`\"<demo> demo: OK\"` marker.",
              "",
              "## What was NOT done",
              "",
              "- No videos built, no uploads, no publishing, no git",
              "  operations — code only, per the task.",
              "- No network or external API usage anywhere; every demo",
              "  computes from deterministic fixture data in-process.",
              "- No real secrets anywhere; the demos contain no",
              "  credentials at all — pricing fixtures are public-style",
              "  rate cards, not keys.",
              ""]
    out = REPO_ROOT / "RESULTS.md"
    out.write_text("\n".join(lines))
    return out


def main() -> None:
    checks = [
        ("01 repo structure (13 demos + root files)", check_01_structure),
        ("02 s01 cost-meter priced day + always-on meters", check_02_s01),
        ("03 s02 bill-decomposer drivers + shadow spend + task metrics",
         check_03_s02),
        ("04 s03 token-ledger formula + re-billing + budgets", check_04_s03),
        ("05 s04 model-router cascade + sweep + quality gate", check_05_s04),
        ("06 s05 cache-lab layers + break-even + batching", check_06_s05),
        ("07 s06 bounded-agent budgets + bloat table", check_07_s06),
        ("08 s07 breakeven curves + utilisation + hidden costs",
         check_08_s07),
        ("09 s08 attribution-pipeline four views + 5% rule", check_09_s08),
        ("10 s09 budget-guard alerts + degradation + CI policy",
         check_10_s09),
        ("11 s10 savings-planner ranking + Meridian replay", check_11_s10),
        ("12 s11 unit-economics margins + pricing + futures",
         check_12_s11),
        ("13 s12 audit-kit Harborline register + findings", check_13_s12),
        ("14 s13 capstone-studio pack gate + checklist score",
         check_14_s13),
        ("15 no hardcoded secrets", check_15_no_secrets),
        ("16 README documents demos + lesson mapping", check_16_docs),
    ]
    for name, fn in checks:
        check(name, fn)

    results_path = write_results()
    assert results_path.is_file()

    print()
    print("=" * 60)
    for name, status in results:
        print(f"[{status.split(':')[0]:4s}] {name}")
    failed = [n for n, s in results if s.startswith("FAIL")]
    if failed:
        print(f"\n{len(failed)} CHECK(S) FAILED")
        sys.exit(1)
    print(f"\nALL CHECKS PASSED ({len(results)}/16 green)")
    print(f"RESULTS.md written by this run: {results_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
