"""Your first MCP server, structured the way production servers are.

Lessons 11-15 companion demo for *MCP Architecture: Production-Grade
Model Context Protocol Systems* (Udemy Course 3).

The anatomy from Lesson 11, made literal:

    transport     -- moves raw JSON-RPC messages (here: in-process lines,
                     exactly what a stdio transport carries)
    dispatcher    -- routes by method, enforces session state
    handlers      -- one function per method family
    registry      -- the tool catalog: name -> declaration + handler

Lesson 12's first tool (get_service_status) is implemented end to end:
schema, handler, shaped result. Lesson 13's three failure modes are
demonstrated on purpose: a missing argument, a wrong-typed argument, and
an upstream failure — each reported the way the course teaches:
tool errors inside the result (isError), protocol errors as JSON-RPC
error objects.

Run it exactly as a student would:

    python -m server.first_server
"""

from __future__ import annotations

import json

PROTOCOL_VERSION = "2025-03-26"

# --- Fictional upstream system (stands in for an ops status service) ---

UPSTREAM_STATUS = {
    "payments-api": {"state": "operational", "p99_ms": 180, "error_rate": 0.001},
    "search-service": {"state": "degraded", "p99_ms": 640, "error_rate": 0.021},
    "billing-worker": {"state": "operational", "p99_ms": 95, "error_rate": 0.0},
}


class UpstreamError(Exception):
    """The upstream system failed; the tool must translate, not leak."""


def upstream_get_status(service: str) -> dict:
    """Simulated upstream call. 'legacy-cron' is our failing service."""
    if service == "legacy-cron":
        raise UpstreamError("connection refused by status.internal:8443")
    return UPSTREAM_STATUS[service]


# --- Registry (Lesson 11): declaration + handler, side by side ---

def tool_get_service_status(arguments: dict) -> dict:
    """Handler contract (Lesson 12): validate, execute, shape."""
    service = arguments.get("service")
    if service is None:
        return _tool_error(
            "Missing required argument 'service'. "
            f"Known services: {', '.join(sorted(UPSTREAM_STATUS))}."
        )
    if not isinstance(service, str):
        return _tool_error(
            "Argument 'service' must be a string naming one known service, "
            f"e.g. 'payments-api'. Received: {type(service).__name__}."
        )
    if service not in UPSTREAM_STATUS and service != "legacy-cron":
        return _tool_error(
            f"Unknown service '{service}'. "
            f"Known services: {', '.join(sorted(UPSTREAM_STATUS))}."
        )
    try:
        status = upstream_get_status(service)
    except UpstreamError:
        # Lesson 13: translate upstream failure; never leak internals
        # (hostnames, ports, stack traces) into a tool result.
        return _tool_error(
            f"Status for '{service}' is temporarily unavailable. "
            "The operations team has been notified. Retry in a few minutes."
        )
    text = (
        f"{service}: {status['state']} "
        f"(p99 {status['p99_ms']} ms, error rate {status['error_rate']:.1%})"
    )
    return {
        "content": [{"type": "text", "text": text}],
        "structuredContent": {"service": service, **status},
        "isError": False,
    }


def _tool_error(message: str) -> dict:
    """A tool-level error: well-formed call, failed execution (Lesson 13)."""
    return {"content": [{"type": "text", "text": message}], "isError": True}


REGISTRY = {
    "get_service_status": {
        "declaration": {
            "name": "get_service_status",
            "description": (
                "Return the current operational status of one enterprise "
                "service: state, p99 latency, error rate. Read-only."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "enum": sorted(UPSTREAM_STATUS),
                        "description": "Service name, exactly as listed.",
                    }
                },
                "required": ["service"],
            },
        },
        "handler": tool_get_service_status,
    },
}


# --- Dispatcher + handlers (Lesson 11) ---

def _result(req_id, payload):
    return {"jsonrpc": "2.0", "id": req_id, "result": payload}


def _error(req_id, code, message):
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


class FirstServer:
    """Transport-agnostic server core: messages in, messages out."""

    def __init__(self) -> None:
        self.initialized = False

    def handle(self, message: dict) -> dict | None:
        method = message.get("method")
        req_id = message.get("id")
        params = message.get("params", {}) or {}

        if method == "initialize":
            self.initialized = True
            return _result(req_id, {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "first-server", "version": "1.0.0"},
            })
        if method == "notifications/initialized":
            return None
        if method == "ping":
            return _result(req_id, {})
        if not self.initialized:
            return _error(req_id, -32002, "Server not initialized")
        if method == "tools/list":
            return _result(req_id, {
                "tools": [entry["declaration"] for entry in REGISTRY.values()]
            })
        if method == "tools/call":
            return self._dispatch_tool(req_id, params)
        return _error(req_id, -32601, f"Method not found: {method}")

    def _dispatch_tool(self, req_id, params: dict) -> dict:
        name = params.get("name")
        entry = REGISTRY.get(name)
        if entry is None:
            # Unknown tool name is a protocol-level problem (Lesson 13).
            return _error(req_id, -32602, f"Unknown tool: {name}")
        return _result(req_id, entry["handler"](params.get("arguments", {}) or {}))


def run_session(lines: list[dict]) -> list[dict | None]:
    """The 'transport' for this demo: a list of messages, in order."""
    server = FirstServer()
    return [server.handle(message) for message in lines]


def main() -> None:
    print("== first server: anatomy, one tool, three failure modes ==")
    req = lambda i, m, p=None: {"jsonrpc": "2.0", "id": i, "method": m, **({"params": p} if p else {})}

    session = [
        req(1, "initialize", {"protocolVersion": PROTOCOL_VERSION,
                              "capabilities": {},
                              "clientInfo": {"name": "inspector-by-hand", "version": "0"}}),
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        req(2, "tools/list"),
        req(3, "tools/call", {"name": "get_service_status",
                              "arguments": {"service": "payments-api"}}),
    ]
    out = run_session(session)
    print(f"initialize -> server: {out[0]['result']['serverInfo']['name']}")
    print(f"tools/list -> {[t['name'] for t in out[2]['result']['tools']]}")
    print(f"tools/call -> {out[3]['result']['content'][0]['text']}")
    print(f"structured -> {json.dumps(out[3]['result']['structuredContent'], sort_keys=True)}")

    print()
    print("Lesson 13 demo — breaking the tool three ways:")
    server = FirstServer()
    server.handle(session[0])

    missing = server.handle(req(4, "tools/call", {"name": "get_service_status", "arguments": {}}))
    print(f"[1] missing argument -> isError={missing['result']['isError']}: "
          f"{missing['result']['content'][0]['text'][:64]}...")

    wrong_type = server.handle(req(5, "tools/call", {"name": "get_service_status",
                                                     "arguments": {"service": 42}}))
    print(f"[2] wrong type      -> isError={wrong_type['result']['isError']}: "
          f"{wrong_type['result']['content'][0]['text'][:64]}...")

    upstream = server.handle(req(6, "tools/call", {"name": "get_service_status",
                                                   "arguments": {"service": "legacy-cron"}}))
    leaked = "status.internal" in upstream["result"]["content"][0]["text"]
    print(f"[3] upstream failure -> isError={upstream['result']['isError']}, "
          f"internals leaked: {leaked}")

    unknown = server.handle(req(7, "tools/call", {"name": "nope", "arguments": {}}))
    print(f"[+] unknown tool    -> protocol error {unknown['error']['code']}")
    print("first server session complete: validate, execute, shape — errors as values")


if __name__ == "__main__":
    main()
