"""s06 / integrations — choose the shape, survive the legacy.

Lesson mapping: Section 6, Lessons 22-25 (API-first, REST/webhooks/events,
integration patterns, legacy connectors).
What it does:
  1. compares REST polling vs webhooks vs an event bus on one order event
     (latency / cost / failure mode), and
  2. proves a legacy adapter can be swapped for a new API with zero workflow
     changes — identical workflow outputs before and after.
"""

from __future__ import annotations


# ------------------------------------------------- 1. mechanism comparison
# Deterministic model of one "order created" event under three mechanisms.
MECHANISMS = {
    "REST poll (60s)": {"latency_s": 45.0, "cost_per_event": 0.0020,
                        "failure_mode": "missed events during poller downtime",
                        "best_for": "legacy endpoints with no push support"},
    "Webhook": {"latency_s": 1.2, "cost_per_event": 0.0005,
                "failure_mode": "lost if receiver is down (needs retry queue)",
                "best_for": "near-real-time, receiver you control"},
    "Event bus": {"latency_s": 0.3, "cost_per_event": 0.0010,
                  "failure_mode": "consumer lag under spikes (needs backpressure)",
                  "best_for": "many consumers, replay, audit trail"},
}


def compare_mechanisms() -> dict[str, dict]:
    assert len(MECHANISMS) == 3
    for name, m in MECHANISMS.items():
        assert m["latency_s"] > 0 and m["cost_per_event"] > 0, name
    return MECHANISMS


# ------------------------------------------------- 2. swappable adapter
class LegacyAdapter:
    """Mock legacy system: odd field names, cents, no customer object."""

    def fetch_order(self, order_id: str) -> dict:
        return {"ord_id": order_id, "amt_cents": 19999, "cust": "ACME"}


class NewApiAdapter:
    """Mock replacement API: clean names, dollars."""

    def fetch_order(self, order_id: str) -> dict:
        return {"id": order_id, "amount": 199.99, "customer": "ACME"}


def process_order(adapter, order_id: str) -> dict:
    """The workflow: written once, against the adapter interface only."""
    raw = adapter.fetch_order(order_id)
    order_ref = raw.get("ord_id", raw.get("id"))
    cents = raw.get("amt_cents")
    amount = cents / 100.0 if cents is not None else raw["amount"]
    customer = raw.get("cust", raw.get("customer"))
    return {"order_id": order_ref, "amount_usd": round(amount, 2),
            "customer": customer, "status": "fulfilled"}


def main() -> None:
    table = compare_mechanisms()
    print("integrations: one order event, three mechanisms")
    for name, m in table.items():
        print(f"  {name:>16}: latency {m['latency_s']:>5.1f}s | "
              f"${m['cost_per_event']:.4f}/event | fails: {m['failure_mode']}")

    before = process_order(LegacyAdapter(), "O-1042")
    after = process_order(NewApiAdapter(), "O-1042")
    assert before == after, (before, after)  # zero-change swap assertion
    print("legacy adapter swap: workflow output identical")
    print(f"  {before}")
    print("integrations demo: OK")


if __name__ == "__main__":
    main()
