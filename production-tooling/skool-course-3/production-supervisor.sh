#!/bin/bash
# Skool Course 3 — production SUPERVISOR (self-recovery, written 2026-10-17
# after the chain was killed twice by runtime/VM restarts: 02:44 IST and
# ~09:25 IST / 03:55 UTC).
#
# systemd user services are UNAVAILABLE on this VM — verified 2026-10-17:
# `systemctl --user` -> "Failed to connect to bus", and starting user@0 fails
# a dependency job, so no user manager ever runs. Resilience therefore =
# this detached supervisor + the IDEMPOTENT chain (production-chain4.sh,
# which skips every QC-passed lesson) + the one-line relaunch below.
#
# ONE-LINE RELAUNCH (if this supervisor is dead too):
#   cd ~/workspace/udemy-skool/skool-course-3-mcp-architecture && setsid nohup bash production-supervisor.sh >> production-supervisor.out 2>&1 &
#
# Behavior: run the chain; if it exits WITHOUT writing a terminal line
# (CHAIN v4 COMPLETE / CHAIN v4 WAITING) during THAT run, it was killed —
# relaunch after 30s, up to 40 attempts. On a terminal line, exit: what
# remains then is the recorded closing pass (see RECOVERY.md), not the chain.
COURSE="$HOME/workspace/udemy-skool/skool-course-3-mcp-architecture"
LOG="$COURSE/production-chain4.log"
SLOG="$COURSE/production-supervisor.log"
cd "$COURSE" || exit 1
stamp() { date '+%Y-%m-%d %H:%M:%S %Z'; }
attempt=0
while [ $attempt -lt 40 ]; do
  attempt=$((attempt + 1))
  before=$(wc -l < "$LOG" 2>/dev/null || echo 0)
  echo "[$(stamp)] SUPERVISOR: launching production-chain4.sh (attempt $attempt)" >> "$SLOG"
  bash production-chain4.sh >> "$COURSE/production-chain4.out" 2>&1
  rc=$?
  if tail -n +$((before + 1)) "$LOG" 2>/dev/null | grep -q "PRODUCTION CHAIN v4 COMPLETE\|CHAIN v4 WAITING"; then
    echo "[$(stamp)] SUPERVISOR: chain reached a terminal state (rc=$rc) — supervisor exiting" >> "$SLOG"
    exit 0
  fi
  echo "[$(stamp)] SUPERVISOR: chain exited without a terminal state (rc=$rc) — presumed killed; relaunching in 30s" >> "$SLOG"
  sleep 30
done
echo "[$(stamp)] SUPERVISOR: 40 attempts exhausted — supervisor exiting" >> "$SLOG"
