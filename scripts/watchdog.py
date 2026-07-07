#!/usr/bin/env python3
"""Live-run watchdog (F9 checklist): polls a log dir, checks completed samples
against harness invariants, and alarms loudly if any break.

Complements the in-solver circuit breaker: the breaker catches faults WITHIN a
game at the turn they occur; the watchdog catches them BETWEEN games and
between runs, and catches fault classes the breaker doesn't know yet.

Invariants checked per completed sample:
  - unparseable_proposal count (interpreter health)
  - harness_fault store key (breaker trips)
  - eval status == error
  - narration length blowout (mean > 2x the ~120w discipline)

Usage:
    python scripts/watchdog.py logs/glm-overnight-f9              # poll forever
    python scripts/watchdog.py logs/glm-overnight-f9 --once      # single check
Exit codes (with --once): 0 healthy, 2 fault found.
Alarm: console banner + beeps (Windows) and process exit so a dead console is
itself the signal.
"""
from __future__ import annotations

import argparse
import glob
import statistics
import sys
import time
from pathlib import Path

from inspect_ai.log import read_eval_log

UNPARSEABLE_ALARM = 5
NARRATION_MEAN_ALARM = 240  # words; 2x the ~120w discipline


def beep() -> None:
    try:
        import winsound
        for _ in range(3):
            winsound.Beep(880, 400)
            winsound.Beep(440, 400)
    except Exception:
        print("\a" * 3, end="", flush=True)


def check(logdir: str) -> list[str]:
    """Returns a list of fault descriptions (empty = healthy so far)."""
    faults: list[str] = []
    files = sorted(glob.glob(str(Path(logdir) / "*.eval")))
    if not files:
        return faults  # nothing yet; not a fault
    try:
        log = read_eval_log(files[-1])
    except Exception as e:
        # live file mid-write; skip this cycle rather than false-alarm
        print(f"  (log not readable this cycle: {type(e).__name__})")
        return faults

    if log.status == "error":
        faults.append(f"eval status=error ({files[-1]})")

    for s in log.samples or []:
        fault_rec = s.store.get("harness_fault")
        if fault_rec:
            faults.append(f"{s.id}: BREAKER TRIPPED — {fault_rec}")
        gl = s.store.get("game_log") or {}
        ops = gl.get("ops", [])
        unparseable = sum(
            1 for o in ops
            if str(o.get("rejection_reason")) == "unparseable_proposal")
        if unparseable >= UNPARSEABLE_ALARM:
            faults.append(
                f"{s.id}: {unparseable} unparseable_proposal rejections "
                f"(interpreter health)")
        inp = s.input.strip() if isinstance(s.input, str) else None
        narr = [m.text for m in s.messages
                if m.role == "user" and m.text.strip() != inp]
        wc = [len(n.split()) for n in narr[1:]]
        if wc and statistics.mean(wc) > NARRATION_MEAN_ALARM:
            faults.append(
                f"{s.id}: narration mean {statistics.mean(wc):.0f}w "
                f"(discipline blowout)")
    return faults


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("logdir")
    ap.add_argument("--interval", type=int, default=300, help="seconds")
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()

    while True:
        stamp = time.strftime("%H:%M:%S")
        faults = check(args.logdir)
        if faults:
            print("\n" + "!" * 70)
            print(f"  WATCHDOG ALARM {stamp} — {args.logdir}")
            for f in faults:
                print(f"  {f}")
            print("!" * 70 + "\n")
            beep()
            return 2
        n_samples = len(glob.glob(str(Path(args.logdir) / '*.eval')))
        print(f"[{stamp}] healthy ({args.logdir}, {n_samples} log file(s))")
        if args.once:
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    return_code = main()
    sys.exit(return_code)
