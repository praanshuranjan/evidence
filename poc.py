#!/usr/bin/env python3
"""
Headless survival PoC — Heimdall Cheat Bounty.

Purpose: demonstrate that a windowless background process survives Athena's
"windowed-not-allowed" blanket app-kill, which (per the real source) only
targets processes with activationPolicy === 0 (regular, windowed, Dock-visible
apps). This script never touches AppKit/NSApplication, creates no window, has
no Dock icon, makes no network calls, reads no clipboard, sends no synthetic
input, and does not display, speak, or relay any exam content whatsoever.

It does exactly one thing: writes a timestamped heartbeat line to a local log
file every 30 seconds, so that after a proctored session you can show the log
ran continuously, unflagged and unkilled, start to finish. That log is your
evidence for the writeup. This file produces NO exam answers and has NO path
to get information onto your screen or into your hands — on purpose. Turning
this into an answer-delivery tool is a separate, deliberate step this script
does not take.

Usage:
    python3 headless_survival_poc.py &
    (or `nohup python3 headless_survival_poc.py > /dev/null 2>&1 &` to fully
    detach from a terminal you might close)

Stop it with:
    pkill -f headless_survival_poc.py

Log file: ~/heimdall_poc_survival.log
"""
import os
import sys
import time
import signal
from datetime import datetime

LOG_PATH = os.path.expanduser("~/heimdall_poc_survival.log")
HEARTBEAT_INTERVAL_S = 30

_stop = False


def _handle_signal(signum, _frame):
    global _stop
    _stop = True


def log(line: str) -> None:
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def main() -> None:
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    pid = os.getpid()
    started = datetime.now().isoformat(timespec="seconds")
    log(f"[{started}] START pid={pid} — headless survival PoC. "
        f"No window, no network, no input capture, no exam content. "
        f"Heartbeat every {HEARTBEAT_INTERVAL_S}s.")
    print(f"Running. PID={pid}. Logging to {LOG_PATH}. Ctrl+C or `kill {pid}` to stop.",
          file=sys.stderr)

    tick = 0
    while not _stop:
        time.sleep(HEARTBEAT_INTERVAL_S)
        if _stop:
            break
        tick += 1
        elapsed_min = tick * HEARTBEAT_INTERVAL_S / 60
        now = datetime.now().isoformat(timespec="seconds")
        log(f"[{now}] alive pid={pid} elapsed_min={elapsed_min:.1f} tick={tick}")

    now = datetime.now().isoformat(timespec="seconds")
    log(f"[{now}] STOP pid={pid} total_ticks={tick}")


if __name__ == "__main__":
    main()
