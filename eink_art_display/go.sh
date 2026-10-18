#!/bin/bash
# Run from cron, see example_crontab. Works on both displays, find_art.py
# detects which panel it is on. Extra args go to find_art.py (e.g. --clean).
# Expects .env next to this script and a venv made from requirements.txt.
cd "$(dirname "$0")" || exit 1
LOG="$HOME/art.log"
# Keep the log small, one old copy is plenty
if [ -f "$LOG" ] && [ "$(stat -c %s "$LOG")" -gt 1000000 ]; then
    mv "$LOG" "$LOG.1"
fi
exec >>"$LOG" 2>&1
echo "=== $(date '+%F %T') $*"
source .env
exec venv/bin/python find_art.py "$@"
