# MCP Architecture — Course Code

Companion code for **MCP Architecture: Production-Grade Model Context
Protocol Systems** (Udemy Course 3) by Naveen Kumar Josyula.

Every demo is small, self-contained, and runs **offline with no API
keys**: Python standard library only. The protocol demos model the real
Model Context Protocol message flow (JSON-RPC 2.0) faithfully, so what
you read here is what a production SDK puts on the wire.

## Requirements

- Python 3.11+
- No third-party packages (`requirements.txt` is intentionally empty:
  the standard library is the whole dependency list)

## How to run each demo

Run from the repo root:

| Section | Command | What it shows |
|---|---|---|
| Protocol (Lesson 1) | `python -m protocol.mini_mcp` | A complete MCP-style session: initialize handshake, capability exchange, tools/list discovery, two tools/call invocations, ping |
| S3 · First server | `python -m server.first_server` | Server anatomy (transport, dispatcher, handlers, registry); one tool end to end; Lesson 13's three failure modes (missing argument, wrong type, upstream failure) with errors as values |
| S4 · Tools in depth | `python -m tools.tool_design` | Schema validation that teaches the model to retry; argument-validity measurement; idempotency keys and dry-run previews; long-running job handles with progress and cancellation |
| S5 · Resources & prompts | `python -m resources.resources_prompts` | Resource tree with URI templates, subscriptions, pagination and a read audit log; versioned prompt templates with completion; bounded sampling/elicitation; roots |
| S6 · Transports | `python -m transports.transports` | The same server core over real stdio (child process; diagnostics on stderr) and streamable HTTP (session header, Origin check) |
| S7 · Enterprise | `python -m enterprise.enterprise` | Legacy facade pattern; allow-listed parameterized database queries with row caps and audit; a paginated SaaS ticketing API wrapped into clean tools; document boundary scanning; credential vault + redaction + per-tool delegation |
| S8 · Clients & hosts | `python -m clients.client` | Client lifecycle and discovery; multi-server host with namespaces, collision detection, selection pressure; approval gate with scoped, expiring remembered approvals |
| S9 · Security | `python -m security.security` | Tool-description poisoning scan; definition pinning vs rug pulls; OAuth-style token hygiene (audience, scopes, expiry; confused-deputy refused); sandbox policy; the Lesson 41 prompt-injection demo through the full defense stack |
| S10 · Evaluation | `python -m evaluation.harness` | Contract tests, golden tasks with metrics (selection accuracy, argument validity, completion), a baseline comparison, and a pass/fail release gate; failure-trace classification |
| S11 · Operations | `python -m operations.operations` | Per-call telemetry with correlation ids and latency percentiles; latency/cost budgets as contracts; mechanical schema-evolution classification (additive vs breaking); kill switches and an incident flow |
| S12 · Governance | `python -m governance.governance` | Tool catalog with trust tiers; review-board admission as policy-as-code; the capstone production-readiness review with go/no-go verdicts |

## Validation

`python validate.py` runs every demo end to end as a subprocess, checks
the expected output markers, and adds direct assertions per section
(handshake ordering, error taxonomy, no-leak guarantees, gate behavior,
readiness verdicts). It exits non-zero if anything fails. Current
status: **PASS (74 checks)**.
