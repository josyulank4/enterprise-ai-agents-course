# Production Tooling — NOT student code

This folder holds the **production pipeline** used to build the course
videos — how the lessons are assembled and quality-checked before they are
published. It is kept in this repo so the working production code is under
version control alongside the courses it produces.

**Students: this is not course material.** Your code lives in the course
folders at the repo root — see the "Find your course" index in the
[root README](../README.md).

## What's here

### `skool-course-3/` — Skool Course 3 (MCP Architecture) pipeline

Root tooling:

| File | What it does |
|------|--------------|
| `production-chain4.sh` | The current chain runner: walks every lesson, skips any lesson whose QC record already passes all gates, assembles what's missing, then QC-checks it. Idempotent — safe to relaunch after any interruption. |
| `production-supervisor.sh` | Watchman wrapper: relaunches the chain shortly after any abnormal exit, so a killed render self-heals. |
| `production-chain3.sh` | The previous chain runner, kept for the record (its pass-counting under-read QC records; superseded by chain4). |
| `production-resume.sh` | One-shot relaunch helper used to restart production from a paused state. |
| `qc_record.py` | Re-measures a finished lesson against every QC gate (duration vs the curriculum window, full decode scan, blackdetect, loudness, 7-frame voice↔slide sync) and writes its QC record (JSON). Written because the s09–s13 `qc_check.py` scripts only printed gates without recording them. |

Per-section code (`sections/s01/` … `sections/s13/`, one folder per course
section):

| File | What it does |
|------|--------------|
| `build_slides.py` | Renders the section's slide decks (matplotlib) from the lesson scripts. |
| `assemble.py` | Builds each lesson video: narration + slides → clips → final MP4 via ffmpeg (1080p H.264 + AAC, loudnorm −16 LUFS), reusing already-verified clips instead of re-rendering them. |
| `qc_check.py` | The section's QC gate runner for each finished lesson. |
| Section extras | `s07/a1_build.py`, `s07/a1_fix_sub.py` — the verbatim sentence-boundary segment-split repair used on two lessons whose narration segments failed the speed gate; `s08/finish_l32.py`, `finish_l33.py`, `finish_l35.py` — per-lesson finish passes for Section 8. |

Production spec the pipeline enforces: Aria narration voice at the course
speed, loudnorm −16 LUFS, 1920×1080 H.264 + AAC 44.1 kHz stereo, and per
lesson a 7-frame voice↔slide sync check, a zero-error full decode,
blackdetect clean, and a final duration within ±10% of the curriculum
target. No gate is waived: a lesson that fails is re-made, never passed.

This is a faithful copy of the code as it runs on the build machine —
an archive of the working pipeline, not a packaged tool. Paths inside the
scripts assume the build machine's course-folder layout.
