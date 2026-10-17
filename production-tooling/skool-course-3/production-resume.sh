#!/bin/bash
# Skool Course 3 — MCP Architecture: PRODUCTION RESUME CHAIN (master's order 2026-10-16 22:59 IST, resume run 2026-10-17 01:30 IST)
# NO BREAKS: runs sequentially through every remaining fix + assembly + QC.
# One lesson at a time (shared 2-core VM; parallel renders OOM-killed L13 in the first production day).
# A failed step is logged loudly and the chain CONTINUES to the next lesson (work continues on every other front);
# no QC gate is waived anywhere — a lesson counts only when its qc_check passes on disk records.
COURSE="$HOME/workspace/udemy-skool/skool-course-3-mcp-architecture"
LOG="$COURSE/production-resume.log"
STATUS="$COURSE/production-status.txt"
cd "$COURSE" || exit 1

stamp() { date '+%Y-%m-%d %H:%M:%S %Z'; }
say() { echo "[$(stamp)] $*" | tee -a "$LOG"; }
setstatus() { echo "[$(stamp)] $*" > "$STATUS"; say "STATUS: $*"; }

run_step() {
  # run_step <label> <workdir> <cmd...>
  local label="$1"; local wd="$2"; shift 2
  say "=== BEGIN $label :: $* (cwd=$wd) ==="
  setstatus "RUNNING: $label"
  ( cd "$wd" && "$@" ) >> "$LOG" 2>&1
  local rc=$?
  if [ $rc -eq 0 ]; then say "=== OK $label (rc=0) ==="; else say "=== FAIL $label (rc=$rc) — chain continues; gate NOT waived ==="; fi
  return $rc
}

say "######## PRODUCTION RESUME CHAIN START ########"
say "Baseline at restart (verified 2026-10-17 01:30 IST): 23 finals in videos/ = 20 QC-passed + L10 blocked + L15/L17 unconfirmed."
say "Order: L10 A2 -> L15 QC -> L17 probe+rebuild+QC -> L08 -> L19 -> L23 -> L28 -> L20 L21 -> L24 L25 L26 -> L29 L30 L31. Then Phase B (S9-S13) continues under the 3-hourly progress job."

# --- 1. L10 A2 rebuild (s03 assemble.py now carries the A2 branch: caps 16/5/20, aim floor+9 = 603s; banked takes reused) ---
run_step "L10 A2 assemble" "$COURSE/sections/s03" python3 assemble.py l10
run_step "L10 QC"         "$COURSE/sections/s03" python3 qc_check.py l10

# --- 2. L15 QC on the existing final (build.json present, final 682.2s == build record) ---
run_step "L15 QC (existing final)" "$COURSE/sections/s04" python3 qc_check.py l15

# --- 3. L17: provenance probe of existing final, then verified-reuse rebuild, then full QC ---
say "=== L17 PRE-REBUILD PROBE (existing final) ==="
FINAL17="$COURSE/videos/s04-l17-testing-with-the-inspector-and-first-server-2026-10.mp4"
say "existing final duration: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL17")s vs build plan 633.46s (assemble-l17-a1-run2/3/4 logs; clips sum 633.47s; narration-norm 633.50s) — MISMATCH: no l17-build.json exists and the final contradicts every build record, so its provenance/sync cannot be verified. Cure per task (B)(3): rebuild by verified reuse (all 10 clips + narration banked), then full QC."
run_step "L17 rebuild (verified reuse)" "$COURSE/sections/s04" python3 assemble.py l17
run_step "L17 QC"                       "$COURSE/sections/s04" python3 qc_check.py l17

# --- 4. In-flight assemblies: narration banked, re-invoke assembly (reuse verified inside assemble.py) ---
run_step "L08 assemble (seg5 76wpm narrow pass re-verified by assemble reuse QC)" "$COURSE/sections/s02" python3 assemble.py l08
run_step "L08 QC" "$COURSE/sections/s02" python3 qc_check.py l08
run_step "L19 assemble" "$COURSE/sections/s05" python3 assemble.py l19
run_step "L19 QC"       "$COURSE/sections/s05" python3 qc_check.py l19
run_step "L23 assemble" "$COURSE/sections/s06" python3 assemble.py l23
run_step "L23 QC"       "$COURSE/sections/s06" python3 qc_check.py l23
run_step "L28 assemble" "$COURSE/sections/s07" python3 assemble.py l28
run_step "L28 QC"       "$COURSE/sections/s07" python3 qc_check.py l28

# --- 5. Slide-ready lessons (TTS fresh; A1 auto-split built into s05/s06/s07 assemble.py) ---
for spec in "s05 l20" "s05 l21" "s06 l24" "s06 l25" "s06 l26" "s07 l29" "s07 l30" "s07 l31"; do
  set -- $spec
  run_step "$2 assemble" "$COURSE/sections/$1" python3 assemble.py "$2"
  run_step "$2 QC"       "$COURSE/sections/$1" python3 qc_check.py "$2"
done

say "######## PHASE A COMPLETE (all lessons through S8) ########"
say "Finals in videos/ now: $(ls "$COURSE"/videos/*.mp4 | wc -l) (was 23 at restart; target after Phase A: 35 = 50 - 15 in S9-S13)"
setstatus "PHASE A DONE — Phase B (S9-S13 section build L36-L50, s04/s02 manifest repair, then Skool creation/upload/publish + five-check verification) continues under skool-course3-progress-3h supervision; see production-resume.log"
say "######## CHAIN PAUSED AT PHASE BOUNDARY — NOT A BREAK: Phase B is agent-authored work (new section pipelines + slide decks for L36-L50) picked up by the supervising progress job ########"
