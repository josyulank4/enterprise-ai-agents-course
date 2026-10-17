"""Transports: the same server over stdio and over streamable HTTP.

Lessons 24-27 companion demo for *MCP Architecture* (Udemy Course 3).

Lesson 24 — stdio: the server runs as a CHILD PROCESS speaking newline-
delimited JSON-RPC on its stdin/stdout. The cardinal rule is enforced
structurally: all diagnostics go to stderr, never stdout, because stdout
is the protocol channel.

Lesson 25 — streamable HTTP: the identical server core behind an HTTP
endpoint (stdlib http.server): POST JSON-RPC, a session header after
initialize, and an Origin check (the transport's own threat list).

The server core is imported from the Section 3 module — the transport
changes, the server does not. That is the lesson.

Run:  python -m transports.transports
"""

from __future__ import annotations

import json
import subprocess
import sys
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from server.first_server import FirstServer

REPO_ROOT = Path(__file__).resolve().parent.parent
CHILD_FLAG = "--stdio-child"


def run_stdio_child() -> None:
    """The server as a child process. Logs -> stderr. Protocol -> stdout."""
    server = FirstServer()
    print("[child] ready on stdio (this line is stderr)", file=sys.stderr)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            print("[child] malformed line discarded", file=sys.stderr)
            continue
        response = server.handle(message)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


def stdio_session() -> dict:
    """Lesson 24: a host spawning and supervising a local server."""
    proc = subprocess.Popen(
        [sys.executable, "-m", "transports.transports", CHILD_FLAG],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
        cwd=str(REPO_ROOT),
    )
    def send(obj) -> dict | None:
        proc.stdin.write(json.dumps(obj) + "\n")
        proc.stdin.flush()
        if "id" not in obj:
            return None
        return json.loads(proc.stdout.readline())

    init = send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                 "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                            "clientInfo": {"name": "stdio-host", "version": "0"}}})
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    listing = send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    call = send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                 "params": {"name": "get_service_status",
                            "arguments": {"service": "search-service"}}})
    proc.stdin.close()
    proc.wait(timeout=10)
    stderr_text = proc.stderr.read()
    return {"server": init["result"]["serverInfo"]["name"],
            "tools": [t["name"] for t in listing["result"]["tools"]],
            "call": call["result"]["content"][0]["text"],
            "stderr_clean": "ready on stdio" in stderr_text,
            "exit": proc.returncode}


# --- Lesson 25: streamable HTTP over the same core ---

class MCPHttpHandler(BaseHTTPRequestHandler):
    server_core: FirstServer
    session_open = False

    def log_message(self, *args):  # keep stdout clean for the transcript
        pass

    def do_POST(self):
        origin = self.headers.get("Origin")
        if origin and origin not in ("https://host.example",):
            body = json.dumps({"jsonrpc": "2.0", "id": None, "error": {
                "code": -32000, "message": "Origin not allowed"}}).encode()
            self._reply(403, body)
            return
        length = int(self.headers.get("Content-Length", 0))
        message = json.loads(self.rfile.read(length) or b"{}")
        if message.get("method") == "initialize":
            type(self).session_open = True
        response = self.server_core.handle(message)
        headers = {}
        if type(self).session_open:
            headers["Mcp-Session-Id"] = "sess-demo-1"
        body = json.dumps(response).encode() if response is not None else b""
        self._reply(200 if response is not None else 202, body, headers)

    def _reply(self, code, body, headers=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body)


def http_session() -> dict:
    MCPHttpHandler.server_core = FirstServer()
    httpd = HTTPServer(("127.0.0.1", 0), MCPHttpHandler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    def post(payload, origin="https://host.example"):
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/mcp",
            data=json.dumps(payload).encode(), method="POST",
            headers={"Content-Type": "application/json", "Origin": origin})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status, dict(resp.headers), json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            return e.code, {}, json.loads(e.read() or b"{}")

    _, headers, init = post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                             "params": {"protocolVersion": "2025-03-26",
                                        "capabilities": {},
                                        "clientInfo": {"name": "http-host", "version": "0"}}})
    _, _, call = post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                       "params": {"name": "get_service_status",
                                  "arguments": {"service": "billing-worker"}}})
    bad_status, _, bad = post({"jsonrpc": "2.0", "id": 3, "method": "tools/list"},
                              origin="https://evil.example")
    httpd.shutdown()
    return {"server": init["result"]["serverInfo"]["name"],
            "session_header": headers.get("Mcp-Session-Id"),
            "call": call["result"]["content"][0]["text"],
            "bad_origin_status": bad_status,
            "bad_origin_error": bad["error"]["message"]}


def main() -> None:
    print("== transports: one server core, two transports ==")
    stdio = stdio_session()
    print(f"stdio: server={stdio['server']}, tools={stdio['tools']}")
    print(f"stdio: call -> {stdio['call']}")
    print(f"stdio: diagnostics stayed on stderr: {stdio['stderr_clean']}, "
          f"child exit={stdio['exit']}")
    http = http_session()
    print(f"http: server={http['server']}, session header={http['session_header']}")
    print(f"http: call -> {http['call']}")
    print(f"http: hostile Origin refused with {http['bad_origin_status']} "
          f"({http['bad_origin_error']})")
    print("transports demo complete: transport changes, the server does not")


if __name__ == "__main__":
    if CHILD_FLAG in sys.argv:
        run_stdio_child()
    else:
        main()
