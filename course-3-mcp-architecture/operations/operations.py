"""Production operations: telemetry, budgets, versioning, incidents.

Lessons 46-49 companion demo for *MCP Architecture* (Udemy Course 3).

  Lesson 46 — the minimum viable telemetry set for a tool call:
  structured log line, counters, latency percentiles, one correlation
  id across host, server, and upstream.
  Lesson 47 — latency and cost budgets enforced as contracts: a call
  chain that would exceed its budget is flagged before it runs long.
  Lesson 48 — schema evolution classified mechanically: additive is
  safe, removing/renaming/retyping breaks running clients; kill
  switches for tools that misbehave.
  Lesson 49 — incident response for a misbehaving tool: detect,
  contain (disable first), communicate, and file the golden task.

Run:  python -m operations.operations
"""

from __future__ import annotations

import json
import time

# --- Lesson 46: telemetry ---

class Telemetry:
    def __init__(self) -> None:
        self.events: list[dict] = []
        self.latencies: list[float] = []

    def record(self, correlation_id: str, tool: str, side: str,
               latency_ms: float, outcome: str) -> None:
        event = {"ts": round(time.time(), 3), "corr": correlation_id,
                 "tool": tool, "side": side, "ms": latency_ms,
                 "outcome": outcome}
        self.events.append(event)
        if side == "server":
            self.latencies.append(latency_ms)

    def percentile(self, pct: float) -> float:
        if not self.latencies:
            return 0.0
        ordered = sorted(self.latencies)
        idx = min(len(ordered) - 1, int(pct / 100 * len(ordered)))
        return ordered[idx]

    def error_classes(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self.events:
            if e["outcome"] != "ok":
                counts[e["outcome"]] = counts.get(e["outcome"], 0) + 1
        return counts


# --- Lesson 47: budgets as contracts ---

BUDGET = {"max_latency_ms": 4000, "max_tool_calls": 6, "max_result_tokens": 8000}


def check_budget(plan: dict) -> list[str]:
    violations = []
    if plan["estimated_latency_ms"] > BUDGET["max_latency_ms"]:
        violations.append(
            f"latency {plan['estimated_latency_ms']}ms > budget {BUDGET['max_latency_ms']}ms")
    if plan["tool_calls"] > BUDGET["max_tool_calls"]:
        violations.append(
            f"tool calls {plan['tool_calls']} > budget {BUDGET['max_tool_calls']}")
    if plan["estimated_result_tokens"] > BUDGET["max_result_tokens"]:
        violations.append(
            f"result tokens {plan['estimated_result_tokens']} > budget "
            f"{BUDGET['max_result_tokens']} (verbosity is a cost center)")
    return violations


# --- Lesson 48: schema evolution + kill switches ---

def classify_schema_change(old: dict, new: dict) -> tuple[str, list[str]]:
    """Additive changes are safe; removals and retypes break clients."""
    notes: list[str] = []
    breaking = False
    old_props = set(old.get("properties", {}))
    new_props = set(new.get("properties", {}))
    for removed in old_props - new_props:
        breaking = True
        notes.append(f"BREAKING: property '{removed}' removed")
    for added in new_props - old_props:
        if added in new.get("required", []):
            breaking = True
            notes.append(f"BREAKING: new required property '{added}'")
        else:
            notes.append(f"additive: optional property '{added}' added")
    for common in old_props & new_props:
        if old["properties"][common].get("type") != new["properties"][common].get("type"):
            breaking = True
            notes.append(f"BREAKING: property '{common}' changed type")
    if set(new.get("required", [])) - set(old.get("required", [])) & old_props:
        breaking = True
        notes.append("BREAKING: an existing property became required")
    return ("BREAKING" if breaking else "SAFE"), notes


class KillSwitch:
    """Lesson 48/49: disable a tool fleet-wide in one move."""

    def __init__(self) -> None:
        self.disabled: set[str] = set()

    def disable(self, tool: str, reason: str) -> str:
        self.disabled.add(tool)
        return f"{tool} disabled: {reason}"

    def allowed(self, tool: str) -> bool:
        return tool not in self.disabled


# --- Lesson 49: incident flow ---

def incident_flow(switch: KillSwitch, tool: str) -> list[str]:
    return [
        f"detect: telemetry anomaly on {tool} (error class spike)",
        f"contain: {switch.disable(tool, 'incident INC-2041')}",
        "degrade: host falls back to cached status page",
        "communicate: status note posted; affected calls listed from telemetry",
        "post-incident: failing trace converted into a golden task",
    ]


def main() -> None:
    print("== operations: telemetry, budgets, versioning, incidents ==")
    tel = Telemetry()
    for i, (tool, ms, outcome) in enumerate([
            ("get_service_status", 42, "ok"), ("get_service_status", 61, "ok"),
            ("get_service_status", 130, "ok"), ("create_ticket", 240, "ok"),
            ("get_service_status", 890, "upstream_timeout")]):
        tel.record(f"corr-{100+i}", tool, "server", ms, outcome)
        tel.record(f"corr-{100+i}", tool, "host", ms + 5, outcome)
    print(f"telemetry: {len(tel.events)} events, server p50={tel.percentile(50):.0f}ms "
          f"p95={tel.percentile(95):.0f}ms, error classes={tel.error_classes()}")
    print(f"sample log line: {json.dumps(tel.events[0], sort_keys=True)}")

    lean = {"estimated_latency_ms": 1800, "tool_calls": 3, "estimated_result_tokens": 2400}
    heavy = {"estimated_latency_ms": 9500, "tool_calls": 14, "estimated_result_tokens": 42000}
    print(f"budget, lean plan violations: {check_budget(lean)}")
    print(f"budget, heavy plan violations: {len(check_budget(heavy))} "
          f"(first: {check_budget(heavy)[0]})")

    old = {"type": "object",
           "properties": {"service": {"type": "string"},
                          "verbose": {"type": "boolean"}},
           "required": ["service"]}
    evolved = {"type": "object",
               "properties": {"service": {"type": "string"},
                              "verbose": {"type": "boolean"},
                              "region": {"type": "string"}},
               "required": ["service"]}
    verdict, notes = classify_schema_change(old, evolved)
    print(f"schema evolution (add optional): {verdict} — {notes}")
    broken = {"type": "object",
              "properties": {"service": {"type": "integer"}},
              "required": ["service"]}
    verdict, notes = classify_schema_change(old, broken)
    print(f"schema evolution (retype + remove): {verdict} — {notes[0]}")

    switch = KillSwitch()
    for step in incident_flow(switch, "get_service_status"):
        print(f"incident: {step}")
    print(f"kill switch holds: get_service_status allowed={switch.allowed('get_service_status')}")
    print("operations demo complete: instrument everything, budget honestly")


if __name__ == "__main__":
    main()
