"""Enterprise connections: facade, safe data access, wrapped APIs.

Lessons 28-32 companion demo for *MCP Architecture* (Udemy Course 3).

  Lesson 28 — the facade pattern: MCP tools in front of a 'legacy'
  system whose native API is awkward, versioned, and untouchable.
  Lesson 29 — database access without the database: named, allow-listed,
  parameterized queries over sqlite3; row limits; an audit trail.
  Lesson 30 — DEMO: wrapping a REST/SaaS ticketing API (paginated,
  rate-limited, quirky) into three clean tools: create, search, update.
  Lesson 31 — documents as resources, with a boundary scan flagging
  secrets/PII before content ever reaches a model.
  Lesson 32 — credentials live in a vault pattern; tool results and
  logs are redacted; per-user delegation is decided per tool.

Run:  python -m enterprise.enterprise
"""

from __future__ import annotations

import re
import sqlite3

# --- Lesson 28: the legacy system and its facade ---

class LegacyCRM:
    """Awkward native API: terse codes, no search, version quirks."""

    def __init__(self) -> None:
        self._accounts = {
            "AC-100": {"nm": "Northwind Traders", "tier_cd": "G", "ar_bal": 12400.0},
            "AC-200": {"nm": "Contoso Retail", "tier_cd": "S", "ar_bal": 0.0},
        }
        self.version = "v7 (frozen)"

    def acct_get(self, acct_id: str) -> dict:
        return self._accounts[acct_id]


_TIERS = {"G": "gold", "S": "silver", "B": "bronze"}


def facade_account_summary(account_id: str) -> dict:
    """Model-friendly tool over the legacy shape: names, not codes."""
    raw = LegacyCRM().acct_get(account_id)
    return {
        "account_id": account_id,
        "name": raw["nm"],
        "tier": _TIERS.get(raw["tier_cd"], "unknown"),
        "balance_due": raw["ar_bal"],
        "summary": f"{raw['nm']} ({_TIERS.get(raw['tier_cd'], '?')} tier), "
                   f"balance due ${raw['ar_bal']:,.2f}",
    }


# --- Lesson 29: allow-listed database access over sqlite3 ---

_QUERIES = {
    "open_tickets_by_team": (
        "SELECT id, title, priority FROM tickets "
        "WHERE team = ? AND status = 'open' ORDER BY id LIMIT ?"),
    "ticket_counts_by_status": (
        "SELECT status, COUNT(*) FROM tickets GROUP BY status"),
}

MAX_ROWS = 50


class SafeDatabase:
    """The model can name a query and fill parameters — never write SQL."""

    def __init__(self) -> None:
        self._db = sqlite3.connect(":memory:")
        self._db.execute(
            "CREATE TABLE tickets (id INTEGER, title TEXT, team TEXT, "
            "status TEXT, priority TEXT)")
        rows = [(i, f"Ticket {i}", "network" if i % 2 else "identity",
                 "open" if i % 3 else "closed",
                 ["low", "normal", "high"][i % 3]) for i in range(1, 13)]
        self._db.executemany("INSERT INTO tickets VALUES (?,?,?,?,?)", rows)
        self.audit: list[str] = []

    def run(self, query_name: str, user: str, **params) -> dict:
        if query_name not in _QUERIES:
            return {"isError": True,
                    "text": f"Query '{query_name}' is not allow-listed."}
        sql = _QUERIES[query_name]
        limit = min(int(params.get("limit", MAX_ROWS)), MAX_ROWS)
        bound = (params.get("team"), limit) if "team" in params else ()
        cursor = self._db.execute(sql, bound)
        results = [list(row) for row in cursor.fetchall()]
        self.audit.append(f"{user} ran {query_name} -> {len(results)} rows")
        return {"isError": False, "rows": results, "row_count": len(results)}


# --- Lesson 30 [DEMO]: wrapping a paginated, rate-limited SaaS API ---

class FakeTicketingAPI:
    """Stands in for a vendor REST API, quirks included."""

    PAGE_SIZE = 2

    def __init__(self) -> None:
        self._tickets = [
            {"id": 501, "subject": "VPN drops hourly", "state": "open"},
            {"id": 502, "subject": "Laptop refresh", "state": "open"},
            {"id": 503, "subject": "SSO loop on mobile", "state": "pending"},
            {"id": 504, "subject": "Printer floor 3", "state": "open"},
            {"id": 505, "subject": "Expired cert warning", "state": "closed"},
        ]
        self.calls = 0

    def list(self, page: int) -> dict:
        self.calls += 1
        chunk = self._tickets[page * self.PAGE_SIZE:(page + 1) * self.PAGE_SIZE]
        return {"results": chunk,
                "next_page": page + 1 if len(chunk) == self.PAGE_SIZE else None}

    def create(self, subject: str) -> dict:
        self.calls += 1
        ticket = {"id": 506 + len(self._tickets), "subject": subject, "state": "open"}
        self._tickets.append(ticket)
        return ticket

    def update(self, ticket_id: int, state: str) -> dict:
        self.calls += 1
        for t in self._tickets:
            if t["id"] == ticket_id:
                t["state"] = state
                return t
        raise KeyError(ticket_id)


class TicketingTools:
    """The facade: vendor pagination and quirks never reach the model."""

    def __init__(self) -> None:
        self.api = FakeTicketingAPI()

    def search_tickets(self, state: str | None = None) -> list[dict]:
        found, page = [], 0
        while True:
            payload = self.api.list(page)
            found.extend(t for t in payload["results"]
                         if state is None or t["state"] == state)
            if payload["next_page"] is None:
                return found
            page = payload["next_page"]

    def create_ticket(self, subject: str) -> dict:
        return self.api.create(subject)

    def update_ticket(self, ticket_id: int, state: str) -> dict:
        return self.api.update(ticket_id, state)


# --- Lesson 31: documents behind a boundary scan ---

_SECRET_PATTERNS = {
    "private key block": re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    "email address (PII)": re.compile(r"[\w.]+@[\w.]+\.[a-z]{2,}"),
    "api token shape": re.compile(r"\bsk-[A-Za-z0-9]{8,}\b"),
}


def scan_document(text: str) -> list[str]:
    return [name for name, pat in _SECRET_PATTERNS.items() if pat.search(text)]


# --- Lesson 32: vault pattern + redaction + per-tool delegation ---

class Vault:
    """Secrets are fetched at call time and never returned to callers."""

    def __init__(self) -> None:
        self._secrets = {"ticketing_api_key": "sk-demo-0000000000"}

    def get(self, name: str) -> str:
        return self._secrets[name]


def redact(text: str, vault: Vault) -> str:
    for secret in vault._secrets.values():
        text = text.replace(secret, "[REDACTED]")
    return text


DELEGATION = {"search_tickets": "service account (read-only, shared)",
              "update_ticket": "per-user delegated token",
              "purge_archive": "per-user delegated token + approval"}


def main() -> None:
    print("== enterprise: facade, safe data, wrapped API, credentials ==")
    summary = facade_account_summary("AC-100")
    print(f"facade over legacy v7: {summary['summary']}")

    db = SafeDatabase()
    res = db.run("open_tickets_by_team", user="ops-agent", team="network", limit=500)
    print(f"allow-listed query: {res['row_count']} rows "
          f"(requested limit 500, capped at {MAX_ROWS})")
    blocked = db.run("raw_sql_drop", user="ops-agent")
    print(f"non-allow-listed query refused: isError={blocked['isError']}")
    print(f"audit trail: {db.audit}")

    tools = TicketingTools()
    open_tickets = tools.search_tickets(state="open")
    print(f"wrapped API search: {len(open_tickets)} open tickets across "
          f"{tools.api.calls} vendor calls (pagination hidden)")
    created = tools.create_ticket("New hire laptop")
    updated = tools.update_ticket(503, "open")
    print(f"wrapped API create/update: #{created['id']} created, "
          f"#{updated['id']} -> {updated['state']}")

    clean = "VPN reset runbook: check the gateway pool first."
    dirty = "Contact admin@corp.example or use sk-live99999999 to bypass."
    print(f"document scan clean: findings={scan_document(clean)}")
    print(f"document scan dirty: findings={scan_document(dirty)}")

    vault = Vault()
    log_line = redact(f"calling vendor with key {vault.get('ticketing_api_key')}", vault)
    print(f"redacted log line: {log_line}")
    print(f"delegation decided per tool: {DELEGATION['update_ticket']}")
    print("enterprise demo complete: the model sees tools, never the estate")


if __name__ == "__main__":
    main()
