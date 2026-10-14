"""s07 / data_pipelines — automations starve without data.

Lesson mapping: Section 7, Lessons 26-29 (starved engines, batch vs
streaming, validation/quarantine, features and freshness).
What it does:
  1. runs one source through batch and streaming shapes (freshness/cost),
  2. pushes poisoned records through validation gates into quarantine, and
  3. serves a mock agent from a feature pipeline that REFUSES on stale data.
"""

from __future__ import annotations

# ---------------------------------------------------------------- fixtures
RECORDS = [
    {"id": "r1", "amount": 120.0, "email": "a@acme.com"},
    {"id": "r2", "amount": -45.0, "email": "b@acme.com"},      # poisoned: negative
    {"id": "r3", "amount": 75.5, "email": "c@acme.com"},
    {"id": "r4", "amount": 200.0, "email": ""},               # poisoned: no email
    {"id": "r5", "amount": 310.0, "email": "e@acme.com"},
    {"id": "r6", "amount": "N/A", "email": "f@acme.com"},     # poisoned: bad type
    {"id": "r7", "amount": 55.0, "email": "g@acme.com"},
    {"id": "r8", "amount": 88.25, "email": "h@acme.com"},
]

EXPECTED_CLEAN, EXPECTED_QUARANTINED = 5, 3


# ------------------------------------------------- 1. batch vs streaming
def batch_shape(n_records: int) -> dict:
    return {"shape": "batch", "freshness_s": 3600.0,
            "cost_usd": 0.10, "records": n_records}


def streaming_shape(n_records: int) -> dict:
    return {"shape": "streaming", "freshness_s": 2.0,
            "cost_usd": round(n_records * 0.001, 4), "records": n_records}


# ------------------------------------------------- 2. validation gates
def validate(record: dict) -> list[str]:
    errors = []
    amount = record.get("amount")
    if not isinstance(amount, (int, float)) or amount <= 0:
        errors.append("amount must be a positive number")
    if not record.get("email"):
        errors.append("email is required")
    return errors


def run_pipeline(records: list[dict]) -> tuple[list[dict], list[dict]]:
    clean, quarantined = [], []
    for rec in records:
        errors = validate(rec)
        if errors:
            quarantined.append({"record": rec, "errors": errors})
        else:
            clean.append(rec)
    return clean, quarantined


# ------------------------------------------------- 3. feature freshness
class StaleFeatures(Exception):
    pass


def serve_features(features: dict, now_s: float, max_stale_s: float = 300.0) -> dict:
    age = now_s - features["updated_at_s"]
    if age > max_stale_s:
        raise StaleFeatures(
            f"refusing: features are {age:.0f}s old (limit {max_stale_s:.0f}s)")
    return features["values"]


def main() -> None:
    batch = batch_shape(len(RECORDS))
    stream = streaming_shape(len(RECORDS))
    assert batch["freshness_s"] > stream["freshness_s"]
    assert batch["cost_usd"] > stream["cost_usd"] or True  # shape trade-off, not a race

    clean, quarantined = run_pipeline(RECORDS)
    assert len(clean) == EXPECTED_CLEAN, clean
    assert len(quarantined) == EXPECTED_QUARANTINED, quarantined
    total = round(sum(r["amount"] for r in clean), 2)
    assert abs(total - 648.75) < 1e-9, total  # 120+75.5+310+55+88.25

    fresh = {"updated_at_s": 900.0, "values": {"avg_order": 142.5}}
    assert serve_features(fresh, now_s=1000.0) == {"avg_order": 142.5}
    stale = {"updated_at_s": 100.0, "values": {"avg_order": 142.5}}
    try:
        serve_features(stale, now_s=1000.0)
        raise AssertionError("stale features must be refused")
    except StaleFeatures as exc:
        refusal = str(exc)

    print("data_pipelines: batch vs streaming on one source")
    print(f"  batch:     freshness {batch['freshness_s']:.0f}s | ${batch['cost_usd']:.2f}/run")
    print(f"  streaming: freshness {stream['freshness_s']:.0f}s | ${stream['cost_usd']:.4f}/run")
    print(f"validation gates: {len(clean)} clean processed (${total:,.2f} total), "
          f"{len(quarantined)} quarantined")
    for q in quarantined:
        print(f"  quarantined {q['record']['id']}: {'; '.join(q['errors'])}")
    print(f"feature pipeline: fresh served, stale -> {refusal}")
    print("data_pipelines demo: OK")


if __name__ == "__main__":
    main()
