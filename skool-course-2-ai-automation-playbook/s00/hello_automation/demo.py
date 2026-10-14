"""s00 / hello_automation — one automated task end to end in under a minute.

Lesson mapping: Section 0, Lessons 1-2 (repo smoke test).
What it does: takes a messy batch of invoice filenames (inconsistent case,
spacing, duplicates) and produces one clean, deduplicated list — the smallest
possible "manual work -> autonomous system" loop.
"""

from __future__ import annotations

import time

# Fixture: 8 messy filenames that collapse to 5 unique documents.
MESSY_FILENAMES = [
    "INV-001  Acme Corp.pdf",
    "inv 002 acme corp.PDF",
    "INV-001 acme corp.pdf",        # duplicate of #1
    "Receipt - Globex (Mar).pdf",
    "receipt globex mar.pdf",       # duplicate of #4
    "INV-003 Initech LLC.pdf",
    "  inv-003   initech llc.PDF ",  # duplicate of #6
    "Contract_Soylent_v2 FINAL.pdf",
]

EXPECTED_UNIQUE = 5


def normalize(name: str) -> str:
    """Canonical form: lowercase, no extension, punctuation -> spaces, single spaces."""
    n = name.strip().lower().replace(".pdf", "")
    n = "".join(ch if ch.isalnum() or ch == " " else " " for ch in n)
    return " ".join(n.split())


def automate(filenames: list[str]) -> list[str]:
    """The automation: normalize + deduplicate, keeping first-seen order."""
    seen: dict[str, str] = {}
    for raw in filenames:
        key = normalize(raw)
        if key not in seen:
            seen[key] = raw
    return list(seen)


def main() -> None:
    started = time.perf_counter()
    result = automate(MESSY_FILENAMES)
    elapsed = time.perf_counter() - started

    assert len(MESSY_FILENAMES) == 8, "fixture changed"
    assert len(result) == EXPECTED_UNIQUE, f"expected {EXPECTED_UNIQUE}, got {result}"
    assert "inv 001 acme corp" in result
    assert elapsed < 60, "smoke test must finish in under a minute"

    print("hello_automation: normalized + deduplicated 8 messy filenames")
    for key in result:
        print(f"  - {key}")
    print(f"unique documents: {len(result)} (elapsed {elapsed * 1000:.1f} ms)")
    print("hello_automation demo: OK")


if __name__ == "__main__":
    main()
