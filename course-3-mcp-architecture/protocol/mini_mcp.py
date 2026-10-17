"""A miniature Model Context Protocol exchange, in one file.

Lesson 1 companion demo for *MCP Architecture: Production-Grade Model
Context Protocol Systems* (Udemy Course 3).

This is a teaching model of the real protocol, not a production SDK. It
implements the exact shape of an MCP session using JSON-RPC 2.0 messages:

    client -> server   initialize            (handshake + capabilities)
    client -> server   notifications/initialized
    client -> server   tools/list            (discovery)
    client -> server   tools/call            (invocation)
    client -> server   ping                  (liveness)

The server exposes two tools over a tiny fictional enterprise knowledge
base. Everything runs in-process with the Python standard library only —
no network, no API keys — so the message flow is fully visible.

Run it exactly as a student would:

    python -m protocol.mini_mcp
"""

from __future__ import annotations

import json

PROTOCOL_VERSION = "2025-03-26"

# --- Fictional enterprise data (written for this course; no real systems) ---

DEPLOYMENT_POLICIES = {
    "payments-api": (
        "Deployment policy for payments-api: production deploys run on "
        "Tuesdays and Thursdays, 14:00-16:00 UTC, require two approvals, "
        "and must pass the full contract-test suite before promotion."
    ),
    "search-service": (
        "Deployment policy for search-service: production deploys are "
        "continuous after the 09:00 UTC index rebuild, require one "
        "approval, and roll back automatically if error rate exceeds 2%."
    ),
}

SERVICE_STATUS = {
    "payments-api": "operational (p99 latency 180 ms, error rate 0.1%)",
    "search-service": "degraded (elevated index lag: 14 minutes)",
}

TOOLS = [
    {
        "name": "get_deployment_policy",
        "description": (
            "Return the production deployment policy for a named service. "
            "Read-only: never changes any system."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "enum": sorted(DEPLOYMENT_POLICIES),
                    "description": "Service name, exactly as listed.",
                }
            },
            "required": ["service"],
        },
    },
    {
        "name": "get_service_status",
        "description": (
            "Return the current operational status summary for a named "
            "service. Read-only."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "enum": sorted(SERVICE_STATUS),
                    "description": "Service name, exactly as listed.",
                }
            },
            "required": ["service"],
        },
    },
]


def _result(req_id, payload: dict) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "result": payload}


def _error(req_id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


class MiniMCPServer:
    """A minimal MCP-style server: handshake, discovery, invocation."""

    def __init__(self) -> None:
        self.initialized = False

    def handle(self, message: dict) -> dict | None:
        """Handle one JSON-RPC message. Notifications return None."""
        method = message.get("method")
        req_id = message.get("id")

        if method == "initialize":
            params = message.get("params", {})
            offered = params.get("protocolVersion", "unknown")
            self.initialized = True
            return _result(req_id, {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "enterprise-knowledge", "version": "1.0.0"},
                "_meta": {"clientOfferedVersion": offered},
            })

        if method == "notifications/initialized":
            return None  # notifications never get a response

        if method == "ping":
            return _result(req_id, {})

        if method == "tools/list":
            if not self.initialized:
                return _error(req_id, -32002, "Server not initialized")
            return _result(req_id, {"tools": TOOLS})

        if method == "tools/call":
            if not self.initialized:
                return _error(req_id, -32002, "Server not initialized")
            return self._call_tool(req_id, message.get("params", {}))

        return _error(req_id, -32601, f"Method not found: {method}")

    def _call_tool(self, req_id, params: dict) -> dict:
        name = params.get("name")
        arguments = params.get("arguments", {}) or {}
        tool = next((t for t in TOOLS if t["name"] == name), None)
        if tool is None:
            return _error(req_id, -32602, f"Unknown tool: {name}")

        required = tool["inputSchema"].get("required", [])
        missing = [field for field in required if field not in arguments]
        if missing:
            # A tool-level error: the call was well-formed, the arguments
            # were not. MCP reports this inside the result, with isError.
            return _result(req_id, {
                "content": [{
                    "type": "text",
                    "text": f"Missing required argument(s): {', '.join(missing)}",
                }],
                "isError": True,
            })

        service = arguments["service"]
        if name == "get_deployment_policy":
            text = DEPLOYMENT_POLICIES.get(service)
        else:
            text = SERVICE_STATUS.get(service)
        if text is None:
            return _result(req_id, {
                "content": [{"type": "text", "text": f"No data for service: {service}"}],
                "isError": True,
            })
        return _result(req_id, {
            "content": [{"type": "text", "text": text}],
            "isError": False,
        })


class MiniMCPClient:
    """A minimal client that runs one full session against the server."""

    def __init__(self, server: MiniMCPServer) -> None:
        self.server = server
        self._next_id = 0

    def request(self, method: str, params: dict | None = None) -> dict:
        self._next_id += 1
        message = {"jsonrpc": "2.0", "id": self._next_id, "method": method}
        if params is not None:
            message["params"] = params
        print(f"  -> {method} (id={self._next_id})")
        response = self.server.handle(message)
        return response

    def notify(self, method: str) -> None:
        print(f"  -> {method} (notification, no response expected)")
        response = self.server.handle({"jsonrpc": "2.0", "method": method})
        assert response is None, "notifications must not be answered"


def main() -> None:
    print("== mini MCP session: one full protocol round-trip ==")
    server = MiniMCPServer()
    client = MiniMCPClient(server)

    print("[1] initialize handshake")
    init = client.request("initialize", {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {},
        "clientInfo": {"name": "course-demo-host", "version": "0.1.0"},
    })
    negotiated = init["result"]["protocolVersion"]
    server_name = init["result"]["serverInfo"]["name"]
    print(f"    initialize -> protocolVersion: {negotiated}, server: {server_name}")

    client.notify("notifications/initialized")

    print("[2] tools/list discovery")
    listing = client.request("tools/list")
    tools = listing["result"]["tools"]
    print(f"    tools/list -> {len(tools)} tools: {', '.join(t['name'] for t in tools)}")

    print("[3] tools/call get_deployment_policy")
    call = client.request("tools/call", {
        "name": "get_deployment_policy",
        "arguments": {"service": "payments-api"},
    })
    text = call["result"]["content"][0]["text"]
    print(f"    tools/call -> {text}")

    print("[4] tools/call get_service_status")
    call2 = client.request("tools/call", {
        "name": "get_service_status",
        "arguments": {"service": "search-service"},
    })
    print(f"    tools/call -> {call2['result']['content'][0]['text']}")

    print("[5] ping")
    client.request("ping")
    print("    ping -> ok")

    print("session complete: handshake, discovery, two tool calls, ping")
    print()
    print("Raw transcript of message shapes (JSON-RPC 2.0):")
    sample = {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
              "params": {"name": "get_deployment_policy",
                         "arguments": {"service": "payments-api"}}}
    print(json.dumps(sample, indent=2))


if __name__ == "__main__":
    main()
