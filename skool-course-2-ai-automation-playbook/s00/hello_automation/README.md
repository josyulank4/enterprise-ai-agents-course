# hello_automation (s00)

**Section 0 — Welcome · Lessons 1–2**

One automated task end to end in under a minute — the repository smoke test.

## What it does

Takes 8 messy invoice filenames (inconsistent case, spacing, duplicates) and
produces one clean, deduplicated list of 5 documents. The smallest possible
"manual work → autonomous system" loop.

## Run

```bash
python demo.py
```

Finishes in milliseconds and prints `hello_automation demo: OK`.

## Key ideas (Lesson 2)

- Every automation is input → transform → verifiable output.
- The `assert` statements are the contract: if the fixture changes, the demo
  fails loudly instead of silently drifting.
- Copy this shape (`normalize` + `automate` + `main` with assertions) as the
  skeleton for your own first automation.
