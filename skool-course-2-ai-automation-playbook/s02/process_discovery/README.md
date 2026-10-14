# process_discovery (s02)

**Section 2 — Process Discovery and Task Mining · Lessons 6–9**

Let the data reveal the work: parse a sample event log into a discovered
process map, flag the top rework-driven candidate, and score candidates on
the automation scorecard.

## Run

```bash
python demo.py
```

## What it does

1. `discover_process_map` — counts direct activity transitions per case
   (the heart of process mining, Lesson 8).
2. `rework_counts` / `top_rework_candidate` — rework loops are the highest-
   signal automation candidates (Lesson 6). Fixture result:
   `manual_data_entry` with 3 loops.
3. `rank_candidates` — the automation scorecard (Lesson 9): volume,
   frequency, pain and rule-fit, weighted 30/30/20/20. Fixture top three:
   `manual_data_entry`, `email_triage`, `invoice_approval`, exported as JSON.

## Lesson mapping

| Lesson | Used in demo |
|--------|--------------|
| 6 — Where Candidates Hide | rework-loop flagging |
| 7 — Discovery in Practice | event-log fixture as shadowing data |
| 8 — Process/Task Mining | `discover_process_map` |
| 9 — Automation Scorecard | `rank_candidates` + top-three export |

Replace `EVENT_LOG` with your own system logs (case id, activity,
timestamp) and `CANDIDATES` with your shortlist.
