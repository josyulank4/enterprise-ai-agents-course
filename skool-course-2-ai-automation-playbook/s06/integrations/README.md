# integrations (s06)

**Section 6 — Integrations and APIs · Lessons 22–25**

Choose the communication shape, and survive the legacy system.

## Run

```bash
python demo.py
```

## What it does

1. **Mechanism comparison** — one "order created" event modeled three ways
   (Lesson 23–24): REST polling (45s latency, misses during poller downtime),
   webhooks (1.2s, lost if the receiver is down), event bus (0.3s, consumer
   lag under spikes). No single winner — the table makes the trade-off
   explicit.
2. **Swappable legacy adapter** (Lesson 25) — `LegacyAdapter` (odd field
   names, cents) and `NewApiAdapter` (clean names, dollars) both satisfy the
   adapter interface. The workflow `process_order` is written once against
   the interface; swapping adapters produces **byte-identical workflow
   output** — the zero-change assertion.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 22 — API-First Design | workflow coded to the adapter interface |
| 23 — REST, Webhooks, Events | three-mechanism model |
| 24 — Integration Patterns | latency/cost/failure trade-off table |
| 25 — Legacy Connectors | `LegacyAdapter` → `NewApiAdapter` swap |

When you replace a real legacy connector, keep the workflow untouched and
assert output equality exactly like this demo.
