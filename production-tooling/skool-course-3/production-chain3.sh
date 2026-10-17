#!/bin/bash
# Skool Course 3 — MCP Architecture: PRODUCTION CHAIN v3 (restart after VM/systemd kill 2026-10-17 02:44 IST)
# Master's binding orders: NO BREAKS once started; FIX ALL ISSUES in the same pass.
# IDEMPOTENT: every lesson is skipped when its on-disk QC json passes ALL gates
# (duration_ok + decode_ok + blackdetect_clean + loudness -17..-15 LUFS + 7/7 frames sync).
# A relaunch after any kill therefore resumes exactly where the chain died. One lesson at a
# time (2-core VM; parallel renders OOM-killed a lesson on day one). A failed lesson is
# logged loudly and the chain CONTINUES — no gate is ever waived.
COURSE="$HOME/workspace/udemy-skool/skool-course-3-mcp-architecture"
LOG="$COURSE/production-chain3.log"
STATUS="$COURSE/production-status.txt"
cd "$COURSE" || exit 1

stamp() { date '+%Y-%m-%d %H:%M:%S %Z'; }
say() { echo "[$(stamp)] $*" | tee -a "$LOG"; }
setstatus() { echo "[$(stamp)] $*" > "$STATUS"; say "STATUS: $*"; }

passed() { # passed <section> <lesson>
  python3 - "$1" "$2" <<'PYEOF'
import json, sys, os
sec, les = sys.argv[1], sys.argv[2]
base = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections')
try:
    d = json.load(open(os.path.join(base, sec, les + '-qc.json')))
except Exception:
    sys.exit(1)
ok = bool(d.get('duration_ok')) and bool(d.get('decode_ok')) and bool(d.get('blackdetect_clean'))
li = d.get('loudness_i')
ok = ok and li is not None and -17.0 <= float(li) <= -15.0
fr = d.get('frames') or []
ok = ok and len(fr) == 7 and all(f.get('sync') for f in fr)
sys.exit(0 if ok else 1)
PYEOF
}

count_passed() {
  local n=0 spec sec les
  for spec in s01:l01 s01:l02 s01:l03 s01:l04 s02:l05 s02:l06 s02:l07 s02:l08 \
              s03:l09 s03:l10 s03:l11 s03:l12 s04:l13 s04:l14 s04:l15 s04:l16 s04:l17 \
              s05:l18 s05:l19 s05:l20 s05:l21 s06:l22 s06:l23 s06:l24 s06:l25 s06:l26 \
              s07:l27 s07:l28 s07:l29 s07:l30 s07:l31 s08:l32 s08:l33 s08:l34 s08:l35 \
              s09:l36 s09:l37 s09:l38 s10:l39 s10:l40 s10:l41 s10:l42 \
              s11:l43 s11:l44 s11:l45 s11:l46 s12:l47 s12:l48 s13:l49 s13:l50; do
    sec="${spec%%:*}"; les="${spec##*:}"
    if passed "$sec" "$les"; then n=$((n+1)); fi
  done
  echo "$n"
}

run() { # run <label> <workdir> <cmd...>
  local label="$1"; local wd="$2"; shift 2
  say "=== BEGIN $label :: $* (cwd=$wd) ==="
  setstatus "RUNNING: $label"
  ( cd "$wd" && "$@" ) >> "$LOG" 2>&1
  local rc=$?
  if [ $rc -eq 0 ]; then say "=== OK $label (rc=0) ==="; else say "=== FAIL $label (rc=$rc) — chain continues; gate NOT waived ==="; fi
  return $rc
}

qc_only() { # qc_only <section> <lesson> <label>
  if passed "$1" "$2"; then say "SKIP $3 — QC json already passes all gates"; return 0; fi
  run "$3 QC" "$COURSE/sections/$1" python3 qc_check.py "$2"
  if passed "$1" "$2"; then say "PASS $3 — all gates green ($(count_passed)/50)"; else say "STILL FAILING $3 — see qc log in sections/$1 (NOT counted, NOT waived)"; fi
}

full() { # full <section> <lesson> <label>
  if passed "$1" "$2"; then say "SKIP $3 — QC json already passes all gates"; return 0; fi
  run "$3 assemble" "$COURSE/sections/$1" python3 assemble.py "$2"
  run "$3 QC" "$COURSE/sections/$1" python3 qc_check.py "$2"
  if passed "$1" "$2"; then say "PASS $3 — all gates green ($(count_passed)/50)"; else say "STILL FAILING $3 — see logs in sections/$1 (NOT counted, NOT waived)"; fi
}

say "######## PRODUCTION CHAIN v3 START (idempotent restart) ########"
say "QC-passed at chain entry: $(count_passed)/50 (finals in videos/: $(ls "$COURSE"/videos/*.mp4 2>/dev/null | wc -l))"
rm -f "$COURSE/sections/s08/l33-build.lock"  # stale lock housekeeping (L33 already QC-passed)

# --- 1. L17 QC first (rebuild finished 633.47s before the kill; its QC died mid-run) ---
qc_only s04 l17 "L17"

# --- 2. In-flight assemblies: narration banked, verified reuse ---
full s02 l08 "L08"
full s05 l19 "L19"
full s06 l23 "L23"
full s07 l28 "L28"

# --- 3. Slide-ready lessons (fresh TTS; A1 auto-split built into assemble.py) ---
full s05 l20 "L20"
full s05 l21 "L21"
full s06 l24 "L24"
full s06 l25 "L25"
full s06 l26 "L26"
full s07 l29 "L29"
full s07 l30 "L30"
full s07 l31 "L31"

# --- 4. Phase B: sections S9–S13 (authored pipelines; skipped cleanly until they exist) ---
for spec in s09:l36 s09:l37 s09:l38 s10:l39 s10:l40 s10:l41 s10:l42 \
            s11:l43 s11:l44 s11:l45 s11:l46 s12:l47 s12:l48 s13:l49 s13:l50; do
  sec="${spec%%:*}"; les="${spec##*:}"
  if [ -f "$COURSE/sections/$sec/assemble.py" ]; then
    full "$sec" "$les" "$(echo "$les" | tr a-z A-Z)"
  else
    say "PHASE B NOT AUTHORED YET: sections/$sec missing — chain ends here; relaunch (same command) after authoring to continue idempotently"
    setstatus "CHAIN v3 WAITING: Phase A done or in logs; sections/$sec (Phase B) not yet authored — relaunch production-chain3.sh after authoring; QC-passed so far: $(count_passed)/50"
    exit 0
  fi
done

say "######## PRODUCTION CHAIN v3 COMPLETE — QC-passed: $(count_passed)/50 ########"
setstatus "PRODUCTION COMPLETE: $(count_passed)/50 QC-passed — next: Skool creation/upload/publish + five-check verification (see PHASE-B-QUEUE.md steps 6-7)"
