"""Tools in depth: schemas models can fill, and retries that are safe.

Lessons 16-19 companion demo for *MCP Architecture* (Udemy Course 3).

Three ideas from the section, made executable:

  Lesson 17 — a small JSON-Schema validator whose error messages teach
  the model how to fix its arguments, plus an argument-validity
  measurement over a batch of model-style attempts.

  Lesson 18 — side-effect classification and an idempotent executor:
  the same idempotency key never executes twice, and destructive tools
  support dry-run previews before the real call.

  Lesson 19 — a long-running tool pattern: start returns a job handle,
  progress is reported honestly, cancellation stops the work.

Run:  python -m tools.tool_design
"""

from __future__ import annotations

import time

# --- Lesson 17: validation that teaches ---

CREATE_TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 5,
                  "description": "Short summary, e.g. 'VPN drops hourly'."},
        "priority": {"type": "string", "enum": ["low", "normal", "high", "urgent"],
                     "description": "Business impact, not requester mood."},
        "assignee_team": {"type": "string", "enum": ["network", "identity", "apps"]},
        "due_days": {"type": "integer", "minimum": 1, "maximum": 30},
    },
    "required": ["title", "priority", "assignee_team"],
}

_TYPE_CHECKS = {"string": str, "integer": int, "number": (int, float), "boolean": bool}


def validate_arguments(schema: dict, arguments: dict) -> list[str]:
    """Return teaching errors: each one says what to change, not just 'bad'."""
    errors: list[str] = []
    props = schema.get("properties", {})
    for field in schema.get("required", []):
        if field not in arguments:
            errors.append(
                f"Missing '{field}'. It is required; "
                f"expected: {props.get(field, {}).get('description', 'see schema')}."
            )
    for field, value in arguments.items():
        if field not in props:
            errors.append(f"Unknown argument '{field}'. Allowed: {', '.join(props)}.")
            continue
        rule = props[field]
        expected = rule.get("type")
        if expected and not isinstance(value, _TYPE_CHECKS[expected]) or (
            expected == "integer" and isinstance(value, bool)
        ):
            errors.append(f"'{field}' must be of type {expected}; got {type(value).__name__}.")
            continue
        if "enum" in rule and value not in rule["enum"]:
            errors.append(f"'{field}' must be one of {rule['enum']}; got {value!r}.")
        if isinstance(value, str) and "minLength" in rule and len(value) < rule["minLength"]:
            errors.append(f"'{field}' needs at least {rule['minLength']} characters.")
        if isinstance(value, int) and "minimum" in rule and value < rule["minimum"]:
            errors.append(f"'{field}' must be >= {rule['minimum']}; got {value}.")
        if isinstance(value, int) and "maximum" in rule and value > rule["maximum"]:
            errors.append(f"'{field}' must be <= {rule['maximum']}; got {value}.")
    return errors


# --- Lesson 18: side effects, idempotency, dry-run ---

SIDE_EFFECTS = {"search_tickets": "read", "create_ticket": "write",
                "purge_ticket_archive": "destructive"}


class IdempotentExecutor:
    """Executes write/destructive tools at most once per idempotency key."""

    def __init__(self) -> None:
        self._results: dict[str, dict] = {}
        self.execution_count = 0

    def execute(self, tool: str, arguments: dict, key: str | None,
                dry_run: bool = False) -> dict:
        if SIDE_EFFECTS.get(tool) in ("write", "destructive"):
            if dry_run:
                return {"preview": True, "would_call": tool,
                        "arguments": arguments, "executed": False}
            if not key:
                return {"isError": True,
                        "text": f"{tool} changes state: an idempotency key is required."}
            if key in self._results:
                replay = dict(self._results[key])
                replay["idempotent_replay"] = True
                return replay
        self.execution_count += 1
        result = {"isError": False, "executed": True,
                  "text": f"{tool} executed (#{self.execution_count})"}
        if key:
            self._results[key] = result
        return result


# --- Lesson 19: long-running tools — job handle, progress, cancel ---

class Job:
    def __init__(self, total_steps: int) -> None:
        self.total = total_steps
        self.done = 0
        self.cancelled = False

    def step(self) -> None:
        if not self.cancelled and self.done < self.total:
            self.done += 1

    def progress(self) -> float:
        return self.done / self.total if self.total else 1.0

    def cancel(self) -> None:
        self.cancelled = True


def main() -> None:
    print("== tools in depth: schemas, idempotency, long-running jobs ==")

    attempts = [
        {"title": "VPN drops hourly", "priority": "high", "assignee_team": "network"},
        {"priority": "high", "assignee_team": "network"},
        {"title": "VPN drops hourly", "priority": "whenever", "assignee_team": "network"},
        {"title": "Ok", "priority": "low", "assignee_team": "apps", "due_days": 45},
        {"title": "Printer on floor 3", "priority": "normal", "assignee_team": "apps", "bogus": 1},
    ]
    valid = 0
    for i, args in enumerate(attempts, 1):
        errors = validate_arguments(CREATE_TICKET_SCHEMA, args)
        valid += 0 if errors else 1
        print(f"attempt {i}: {'VALID' if not errors else 'INVALID'}"
              + (f" -> {errors[0]}" if errors else ""))
    print(f"argument-validity rate: {valid}/{len(attempts)} = {valid/len(attempts):.0%}")

    ex = IdempotentExecutor()
    first = ex.execute("create_ticket", {"title": "VPN drops"}, key="req-123")
    retry = ex.execute("create_ticket", {"title": "VPN drops"}, key="req-123")
    print(f"idempotency: first executed={first['executed']}, "
          f"retry replayed={retry.get('idempotent_replay', False)}, "
          f"real executions={ex.execution_count}")
    preview = ex.execute("purge_ticket_archive", {"older_than_days": 365},
                         key="req-9", dry_run=True)
    print(f"dry-run destructive: preview={preview['preview']}, executed={preview['executed']}")
    refused = ex.execute("create_ticket", {"title": "x"}, key=None)
    print(f"write without key refused: isError={refused['isError']}")

    job = Job(total_steps=5)
    handle = {"job_id": "job-77", "status": "running"}
    print(f"long-running: started -> handle {handle['job_id']}")
    for _ in range(3):
        job.step()
    print(f"progress after 3 steps: {job.progress():.0%}")
    job.cancel()
    job.step()
    print(f"after cancel: progress frozen at {job.progress():.0%}, cancelled={job.cancelled}")
    print("tools demo complete: teach with errors, retry safely, report honestly")


if __name__ == "__main__":
    main()
