"""Resources and prompts: governed context and reviewable workflows.

Lessons 20-23 companion demo for *MCP Architecture* (Udemy Course 3).

  Lesson 20/21 — a resource tree addressed by stable URIs, URI templates
  for parameterized reads, subscriptions that fire change notifications
  (no polling), and pagination for large collections.

  Lesson 22 — prompt templates shipped as versioned, reviewable assets
  with argument completion.

  Lesson 23 — the reverse direction, bounded: a sampling request the
  server may ask for (host decides), an elicitation request for one
  missing field, and roots that fence where the server may look.

Run:  python -m resources.resources_prompts
"""

from __future__ import annotations

# --- Lessons 20/21: resource tree, templates, subscriptions ---

_DOCUMENTS = {
    "handbook/leave-policy": "Leave policy v4: 24 days annual, carry-over capped at 5.",
    "handbook/travel-policy": "Travel policy v2: economy default, approval above $2,000.",
    "runbooks/vpn-reset": "VPN reset runbook: check gateway pool, then session table.",
    "runbooks/backup-restore": "Backup restore runbook: verify snapshot age before restore.",
}


class ResourceTree:
    """Resources are read, never executed; every read is auditable."""

    def __init__(self) -> None:
        self._docs = dict(_DOCUMENTS)
        self._subscribers: dict[str, list[str]] = {}
        self.notifications: list[tuple[str, str]] = []
        self.read_log: list[str] = []

    def list_resources(self, page_size: int = 2) -> list[list[str]]:
        uris = [f"docs://{path}" for path in sorted(self._docs)]
        return [uris[i:i + page_size] for i in range(0, len(uris), page_size)]

    def read(self, uri: str, reader: str) -> str:
        path = uri.removeprefix("docs://")
        if path not in self._docs:
            raise KeyError(f"unknown resource: {uri}")
        self.read_log.append(f"{reader} read {uri}")
        return self._docs[path]

    def read_template(self, template: str, reader: str, **params) -> str:
        """URI template, e.g. docs://handbook/{name} -> a concrete read."""
        return self.read(template.format(**params), reader)

    def subscribe(self, uri: str, subscriber: str) -> None:
        self._subscribers.setdefault(uri, []).append(subscriber)

    def update(self, uri: str, text: str) -> None:
        path = uri.removeprefix("docs://")
        self._docs[path] = text
        for sub in self._subscribers.get(uri, []):
            self.notifications.append((sub, uri))


# --- Lesson 22: prompts as governed, versioned assets ---

class PromptRegistry:
    def __init__(self) -> None:
        self._prompts: dict[str, dict] = {}

    def register(self, name: str, version: str, arguments: list[str],
                 template: str, reviewed_by: str) -> None:
        self._prompts[name] = {
            "version": version, "arguments": arguments,
            "template": template, "reviewed_by": reviewed_by,
        }

    def complete(self, name: str, argument: str, prefix: str) -> list[str]:
        """Argument completion: suggest values for one argument."""
        if argument == "severity":
            return [s for s in ["sev1", "sev2", "sev3"] if s.startswith(prefix)]
        return []

    def get(self, name: str, **args) -> dict:
        prompt = self._prompts[name]
        missing = [a for a in prompt["arguments"] if a not in args]
        if missing:
            raise ValueError(f"prompt '{name}' missing arguments: {missing}")
        return {"name": name, "version": prompt["version"],
                "text": prompt["template"].format(**args)}


# --- Lesson 23: reverse requests, bounded by the host ---

def sampling_request(prompt: str, max_tokens: int) -> dict:
    """A server asking the HOST's model for a completion. The host may
    refuse, cap, or audit — the server never calls a model directly."""
    return {"method": "sampling/createMessage",
            "params": {"maxTokens": min(max_tokens, 500),
                       "messages": [{"role": "user", "content": prompt}],
                       "note": "host decides; server has no model credentials"}}


def elicitation_request(field: str, schema: dict) -> dict:
    """Ask the user for exactly one missing piece of information."""
    return {"method": "elicitation/create",
            "params": {"message": f"One more detail is needed: {field}",
                       "requestedSchema": {"type": "object",
                                           "properties": {field: schema}}}}


def roots() -> list[str]:
    """Where this server is allowed to look — nothing outside these."""
    return ["docs://handbook", "docs://runbooks"]


def main() -> None:
    print("== resources & prompts: governed context, reviewable workflows ==")
    tree = ResourceTree()
    pages = tree.list_resources()
    print(f"resources/list paginated: {len(pages)} pages, "
          f"{sum(len(p) for p in pages)} resources")
    text = tree.read_template("docs://handbook/{name}", reader="support-host",
                              name="leave-policy")
    print(f"template read -> {text[:52]}...")

    tree.subscribe("docs://handbook/leave-policy", "support-host")
    tree.update("docs://handbook/leave-policy",
                "Leave policy v5: 25 days annual, carry-over capped at 5.")
    print(f"subscription notification (no polling): {tree.notifications}")
    print(f"read audit log: {tree.read_log}")

    prompts = PromptRegistry()
    prompts.register(
        "incident_summary", version="1.2.0",
        arguments=["service", "severity"],
        template="Summarize the {severity} incident on {service}: impact, "
                 "timeline, current status, next action.",
        reviewed_by="sre-review-board")
    rendered = prompts.get("incident_summary", service="payments-api", severity="sev2")
    print(f"prompt v{rendered['version']} -> {rendered['text'][:60]}...")
    print(f"completion for severity 'se': {prompts.complete('incident_summary', 'severity', 'se')}")

    sample = sampling_request("Draft a status note", max_tokens=5000)
    print(f"sampling request capped by host policy: maxTokens={sample['params']['maxTokens']}")
    elic = elicitation_request("cost_center", {"type": "string"})
    print(f"elicitation asks for one field: {list(elic['params']['requestedSchema']['properties'])}")
    print(f"roots fence the server to: {roots()}")
    print("resources demo complete: read with governance, prompt with versions")


if __name__ == "__main__":
    main()
