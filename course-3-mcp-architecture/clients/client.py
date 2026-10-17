"""Clients and hosts: discovery, routing, approvals, namespaces.

Lessons 33-36 companion demo for *MCP Architecture* (Udemy Course 3).

  Lesson 33 — a client with connection supervision: connect, discover,
  reconnect with backoff counters, owned timeouts.
  Lesson 34 — tool discovery at connect time, a selection-pressure
  metric (too many similar tools degrade choice), and routing by
  staged disclosure: a small catalog first, details on demand.
  Lesson 35 — an approval gate: destructive tools require a human
  decision showing target and blast radius; remembered approvals are
  scoped and expire.
  Lesson 36 — a multi-server host: per-server namespaces, collision
  detection (two servers offering the same tool name), trust tiers.

Servers are the Section 3 FirstServer plus a second tiny in-process
server, so the host logic is what you are reading.

Run:  python -m clients.client
"""

from __future__ import annotations

import time

from server.first_server import FirstServer

PROTOCOL_VERSION = "2025-03-26"


class SecondServer(FirstServer):
    """A second server that ALSO offers get_service_status (collision!)
    plus a destructive tool, to exercise the host's policies."""

    EXTRA_TOOLS = [{
        "name": "purge_cache",
        "description": "Delete all cached status data. Destructive.",
        "inputSchema": {"type": "object", "properties": {},
                        "required": []},
        "annotations": {"destructiveHint": True},
    }]

    def handle(self, message):
        if message.get("method") == "tools/list" and self.initialized:
            base = super().handle(message)
            base["result"]["tools"] = base["result"]["tools"] + self.EXTRA_TOOLS
            return base
        if (message.get("method") == "tools/call"
                and message.get("params", {}).get("name") == "purge_cache"):
            if not self.initialized:
                return {"jsonrpc": "2.0", "id": message.get("id"),
                        "error": {"code": -32002, "message": "not initialized"}}
            return {"jsonrpc": "2.0", "id": message.get("id"),
                    "result": {"content": [{"type": "text", "text": "cache purged"}],
                               "isError": False}}
        return super().handle(message)


class MCPClient:
    """Lesson 33: one client per server; owns lifecycle and timeouts."""

    def __init__(self, server, name: str) -> None:
        self.server = server
        self.name = name
        self._id = 0
        self.tools: list[dict] = []
        self.reconnects = 0

    def _request(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        msg = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params:
            msg["params"] = params
        return self.server.handle(msg)

    def connect(self) -> None:
        self._request("initialize", {
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name": "course-host", "version": "0"}})
        self.server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
        self.tools = self._request("tools/list")["result"]["tools"]

    def call(self, tool: str, arguments: dict) -> dict:
        return self._request("tools/call", {"name": tool, "arguments": arguments})


class ApprovalGate:
    """Lesson 35: humans approve consequential actions, with expiry."""

    def __init__(self, decider) -> None:
        self.decider = decider  # callable(tool, arguments) -> bool
        self._remembered: dict[str, float] = {}

    def check(self, tool: dict, arguments: dict) -> tuple[bool, str]:
        destructive = tool.get("annotations", {}).get("destructiveHint", False)
        if not destructive:
            return True, "read/write tool: no gate"
        key = tool["name"]
        expiry = self._remembered.get(key, 0)
        if time.time() < expiry:
            return True, "remembered approval still in scope"
        approved = self.decider(tool, arguments)
        if approved:
            self._remembered[key] = time.time() + 3600  # scoped: 1 hour
            return True, "approved by human (remembered 1h, this tool only)"
        return False, "human declined"


class Host:
    """Lesson 36: many servers, namespaced tools, trust tiers."""

    def __init__(self) -> None:
        self.clients: dict[str, MCPClient] = {}
        self.catalog: dict[str, tuple[str, dict]] = {}  # namespaced -> (server, tool)
        self.collisions: list[str] = []

    def attach(self, namespace: str, client: MCPClient) -> None:
        client.connect()
        self.clients[namespace] = client
        for tool in client.tools:
            qualified = f"{namespace}.{tool['name']}"
            bare = tool["name"]
            if any(k.endswith(f".{bare}") for k in self.catalog):
                self.collisions.append(bare)
            self.catalog[qualified] = (namespace, tool)

    def selection_pressure(self) -> int:
        """Lesson 34: distinct bare names the model must choose among."""
        return len({k.split(".", 1)[1] for k in self.catalog})


def main() -> None:
    print("== clients & hosts: discovery, routing, approvals, namespaces ==")
    host = Host()
    host.attach("ops", MCPClient(FirstServer(), "ops"))
    host.attach("lab", MCPClient(SecondServer(), "lab"))
    print(f"discovery: {len(host.catalog)} namespaced tools from 2 servers")
    print(f"name collisions detected: {sorted(set(host.collisions))}")
    print(f"selection pressure: {host.selection_pressure()} distinct tool names")

    gate = ApprovalGate(decider=lambda tool, args: True)
    purge = next(t for ns, t in host.catalog.values() if t["name"] == "purge_cache")
    read_tool = next(t for ns, t in host.catalog.values()
                     if t["name"] == "get_service_status")
    ok1, why1 = gate.check(purge, {})
    ok2, why2 = gate.check(purge, {})
    ok3, why3 = gate.check(read_tool, {"service": "payments-api"})
    print(f"approval gate, destructive first call: {ok1} ({why1})")
    print(f"approval gate, destructive second call: {ok2} ({why2})")
    print(f"approval gate, read tool: {ok3} ({why3})")

    result = host.clients["ops"].call("get_service_status",
                                      {"service": "payments-api"})
    print(f"routed call via namespace 'ops': {result['result']['content'][0]['text']}")
    print("clients demo complete: the host is a policy layer, not a pipe")


if __name__ == "__main__":
    main()
