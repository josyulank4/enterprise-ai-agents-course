"""The MCP test stack and the evaluation harness with release gates.

Lessons 42-45 companion demo for *MCP Architecture* (Udemy Course 3).

  Lesson 42 — layered tests: contract tests (schema conformance for the
  server under test), integration tests against a fake upstream, and
  end-to-end task tests with a scripted stand-in for the model.
  Lesson 43 — golden tasks: realistic jobs with verifiable outcomes;
  metrics are selection accuracy, argument validity, completion, cost.
  Lesson 44 — DEMO: the harness runs the golden set, scores it, compares
  against the previous run, and applies a pass/fail release gate.
  Lesson 45 — a failure trace, classified by the course taxonomy and
  replayed deterministically.

The server under test is the Section 3 FirstServer (wrapped so one
golden task can use the ticketing facade from Section 7).

Run:  python -m evaluation.harness
"""

from __future__ import annotations

from server.first_server import FirstServer
from tools.tool_design import CREATE_TICKET_SCHEMA, validate_arguments

PROTOCOL_VERSION = "2025-03-26"


def fresh_server() -> FirstServer:
    server = FirstServer()
    server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": PROTOCOL_VERSION,
                              "capabilities": {},
                              "clientInfo": {"name": "harness", "version": "0"}}})
    return server


# --- Lesson 42: contract tests ---

def contract_tests() -> list[tuple[str, bool]]:
    server = fresh_server()
    listing = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    tools = listing["result"]["tools"]
    checks = [
        ("every tool has name/description/inputSchema",
         all("name" in t and "description" in t and "inputSchema" in t for t in tools)),
        ("inputSchema is an object schema",
         all(t["inputSchema"].get("type") == "object" for t in tools)),
        ("required fields exist in properties",
         all(set(t["inputSchema"].get("required", []))
             <= set(t["inputSchema"].get("properties", {})) for t in tools)),
        ("unknown method returns -32601",
         server.handle({"jsonrpc": "2.0", "id": 3, "method": "x/y"})["error"]["code"] == -32601),
    ]
    return checks


# --- Lesson 43: golden tasks with a scripted model stand-in ---

class ScriptedModel:
    """Chooses tools the way the task script says a model would —
    including one deliberate mistake the metrics must catch."""

    def choose(self, task: dict) -> tuple[str, dict]:
        return task["attempt_tool"], task["attempt_args"]


GOLDEN_TASKS = [
    {"id": "gt-1", "ask": "Is payments-api healthy?",
     "expect_tool": "get_service_status",
     "attempt_tool": "get_service_status",
     "attempt_args": {"service": "payments-api"},
     "expect_error": False},
    {"id": "gt-2", "ask": "Status of the search service?",
     "expect_tool": "get_service_status",
     "attempt_tool": "get_service_status",
     "attempt_args": {"service": "search-service"},
     "expect_error": False},
    {"id": "gt-3", "ask": "Check billing worker (model omits argument)",
     "expect_tool": "get_service_status",
     "attempt_tool": "get_service_status",
     "attempt_args": {},
     "expect_error": True},
    {"id": "gt-4", "ask": "Delete the status cache (wrong tool entirely)",
     "expect_tool": "get_service_status",
     "attempt_tool": "purge_cache",
     "attempt_args": {},
     "expect_error": True},
]


def run_golden_tasks() -> dict:
    server = fresh_server()
    model = ScriptedModel()
    metrics = {"tasks": 0, "selection_ok": 0, "args_valid": 0, "completed": 0}
    for task in GOLDEN_TASKS:
        metrics["tasks"] += 1
        tool, args = model.choose(task)
        if tool == task["expect_tool"]:
            metrics["selection_ok"] += 1
        known = {t["name"] for t in
                 server.handle({"jsonrpc": "2.0", "id": 9,
                                "method": "tools/list"})["result"]["tools"]}
        if tool not in known:
            continue  # unknown tool: protocol error; nothing else scores
        schema = next(t["inputSchema"] for t in
                      server.handle({"jsonrpc": "2.0", "id": 10,
                                     "method": "tools/list"})["result"]["tools"]
                      if t["name"] == tool)
        required = schema.get("required", [])
        args_valid = all(f in args for f in required)
        metrics["args_valid"] += 1 if args_valid else 0
        resp = server.handle({"jsonrpc": "2.0", "id": 11, "method": "tools/call",
                              "params": {"name": tool, "arguments": args}})
        is_error = resp["result"]["isError"]
        if is_error == task["expect_error"]:
            metrics["completed"] += 1
    n = metrics["tasks"]
    metrics["selection_accuracy"] = metrics["selection_ok"] / n
    metrics["argument_validity"] = metrics["args_valid"] / n
    metrics["task_completion"] = metrics["completed"] / n
    return metrics


# --- Lesson 44: the release gate ---

GATE = {"selection_accuracy": 0.75, "argument_validity": 0.75,
        "task_completion": 0.90}

BASELINE = {"selection_accuracy": 0.75, "argument_validity": 0.75,
            "task_completion": 1.0}


def release_gate(metrics: dict, baseline: dict) -> tuple[bool, list[str]]:
    reasons = []
    for key, floor in GATE.items():
        if metrics[key] < floor:
            reasons.append(f"{key} {metrics[key]:.0%} below gate floor {floor:.0%}")
        if metrics[key] < baseline[key]:
            reasons.append(f"{key} regressed vs baseline ({baseline[key]:.0%} -> {metrics[key]:.0%})")
    return (not reasons), reasons


# --- Lesson 45: classify a failure from its trace ---

TAXONOMY = ["wrong tool", "bad arguments", "upstream fault",
            "policy block", "model misread"]


def classify_failure(trace: dict) -> str:
    if trace.get("blocked_by"):
        return "policy block"
    if trace.get("selected_tool") != trace.get("expected_tool"):
        return "wrong tool"
    if trace.get("argument_errors"):
        return "bad arguments"
    if trace.get("upstream_status", 200) >= 500:
        return "upstream fault"
    return "model misread"


def main() -> None:
    print("== evaluation: contract tests, golden tasks, release gate ==")
    checks = contract_tests()
    for name, ok in checks:
        print(f"contract: [{'PASS' if ok else 'FAIL'}] {name}")

    metrics = run_golden_tasks()
    print(f"golden tasks: {metrics['tasks']} run; "
          f"selection {metrics['selection_accuracy']:.0%}, "
          f"argument validity {metrics['argument_validity']:.0%}, "
          f"completion {metrics['task_completion']:.0%}")

    passed, reasons = release_gate(metrics, BASELINE)
    print(f"release gate: {'PASS — may ship' if passed else 'BLOCKED'}")
    for reason in reasons:
        print(f"  gate note: {reason}")

    schema_errors = validate_arguments(
        CREATE_TICKET_SCHEMA,
        {"title": "VPN", "priority": "whenever", "assignee_team": "network"})
    print(f"argument teaching check: {len(schema_errors)} teaching errors produced")

    trace = {"expected_tool": "get_service_status",
             "selected_tool": "get_service_status",
             "argument_errors": ["missing 'service'"], "upstream_status": 200}
    print(f"trace classification: {classify_failure(trace)} "
          f"(taxonomy: {', '.join(TAXONOMY)})")
    print("evaluation demo complete: measure the agent, gate the release")


if __name__ == "__main__":
    main()
