"""s04 / workflow_orchestration — reliability patterns that survive chaos.

Lesson mapping: Section 4, Lessons 14-17 (orchestration, idempotency/retries/
sagas, observability, first reliable workflow).
What it does: a mini orchestrator with idempotent steps, exponential-backoff
retries with jitter, saga compensation and run-ID tracing. Chaos mode fires
duplicate messages at a flaky debit step; the ledger must still balance, the
debit must apply exactly once, and the always-failing notify step must land
in the dead-letter queue.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class Orchestrator:
    seed: int = 7
    processed: dict[str, object] = field(default_factory=dict)  # idempotency keys
    dead_letter: list[dict] = field(default_factory=list)
    trace: list[str] = field(default_factory=list)
    ledger: dict[str, float] = field(default_factory=lambda: {"A": 1000.0, "B": 0.0})
    debit_applications: int = 0

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)

    def _log(self, run_id: str, msg: str) -> None:
        self.trace.append(f"[{run_id}] {msg}")

    def run_step(self, run_id: str, name: str, fn, key: str,
                 max_retries: int = 3, compensate=None):
        """Idempotent step with exponential-backoff + jitter retries.

        A repeated idempotency key returns the recorded result without
        re-executing (duplicate-message safety). Exhausted retries go to the
        dead-letter queue; the saga compensation runs first.
        """
        if key in self.processed:
            self._log(run_id, f"{name}: duplicate delivery ignored (key={key})")
            return self.processed[key]
        attempt = 0
        while True:
            try:
                result = fn(attempt)
                self.processed[key] = result
                self._log(run_id, f"{name}: ok on attempt {attempt + 1}")
                return result
            except Exception as exc:  # noqa: BLE001 - orchestrator records everything
                self._log(run_id, f"{name}: attempt {attempt + 1} failed ({exc})")
                attempt += 1
                if attempt > max_retries:
                    if compensate is not None:
                        compensate()
                        self._log(run_id, f"{name}: saga compensation ran")
                    self.dead_letter.append(
                        {"run_id": run_id, "step": name, "key": key,
                         "error": str(exc), "attempts": attempt})
                    self._log(run_id, f"{name}: moved to dead-letter queue")
                    raise
                backoff = (2 ** attempt) + self.rng.random()  # exponential + jitter
                self._log(run_id, f"{name}: backing off {backoff:.2f}s")


def flaky_debit(attempt: int, orch: Orchestrator, amount: float):
    def _fn(_attempt: int):
        if _attempt < 2:
            raise ConnectionError("ledger service flaked")
        orch.ledger["A"] -= amount
        orch.debit_applications += 1
        return {"debited": amount}
    return _fn


def credit(orch: Orchestrator, amount: float):
    def _fn(_attempt: int):
        orch.ledger["B"] += amount
        return {"credited": amount}
    return _fn


def always_fail(_attempt: int):
    raise TimeoutError("notify webhook unreachable")


def main() -> None:
    orch = Orchestrator()

    # --- chaos run: duplicate debit message + flaky ledger service ----------
    run_id = "run-chaos-001"
    debit = orch.run_step(run_id, "debit", flaky_debit(0, orch, 100.0),
                          key="debit:run-chaos-001", max_retries=3)
    duplicate = orch.run_step(run_id, "debit", flaky_debit(0, orch, 100.0),
                              key="debit:run-chaos-001", max_retries=3)  # duplicate!
    assert duplicate == debit, "duplicate must return the recorded result"
    orch.run_step(run_id, "credit", credit(orch, 100.0),
                  key="credit:run-chaos-001", max_retries=3)

    # --- ledger-balance assertion: exactly one debit, balanced books --------
    assert orch.debit_applications == 1, "double charge detected!"
    assert abs(orch.ledger["A"] - 900.0) < 1e-9, orch.ledger
    assert abs(orch.ledger["B"] - 100.0) < 1e-9, orch.ledger

    # --- saga run: credit always fails -> compensation refunds the debit ---
    run_id2 = "run-saga-002"
    orch.run_step(run_id2, "debit", flaky_debit(0, orch, 50.0),
                  key="debit:run-saga-002", max_retries=3)

    def refund() -> None:
        orch.ledger["A"] += 50.0

    try:
        orch.run_step(run_id2, "credit", always_fail,
                      key="credit:run-saga-002", max_retries=2,
                      compensate=refund)
        raise AssertionError("credit should have failed")
    except TimeoutError:
        pass
    assert abs(orch.ledger["A"] - 900.0) < 1e-9, "saga compensation failed"
    assert abs(orch.ledger["B"] - 100.0) < 1e-9

    # --- dead letter populated ----------------------------------------------
    assert len(orch.dead_letter) == 1, orch.dead_letter
    assert orch.dead_letter[0]["step"] == "credit"
    assert orch.dead_letter[0]["run_id"] == "run-saga-002"

    print("workflow_orchestration: chaos run trace")
    for line in orch.trace[:8]:
        print(" ", line)
    print(f"  ... ({len(orch.trace)} trace lines total)")
    print(f"ledger after chaos + saga: A=${orch.ledger['A']:.0f} B=${orch.ledger['B']:.0f}")
    print(f"debit applied exactly {orch.debit_applications}x across both runs "
          f"(1 ok + 1 compensated)")
    print(f"dead-letter queue: {len(orch.dead_letter)} item "
          f"({orch.dead_letter[0]['step']} @ {orch.dead_letter[0]['run_id']})")
    print("workflow_orchestration demo: OK")


if __name__ == "__main__":
    main()
