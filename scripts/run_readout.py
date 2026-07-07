#!/usr/bin/env python3
"""One-screen readout of a run: terminal states, halts, rejections, scores.

Usage:
    python scripts/run_readout.py logs/glm-overnight-f8
    python scripts/run_readout.py logs/validation-f8 --narration-stats

The headline character stat per game: how it ended (decision vs. exhaustion),
what it declared (verdict + confidence, now trustworthy post-F1/F2), and what
the engine rejected along the way.
"""
from __future__ import annotations

import argparse
import glob
import statistics
from pathlib import Path

from inspect_ai.log import read_eval_log


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("logdir")
    ap.add_argument("--narration-stats", action="store_true")
    args = ap.parse_args()

    files = sorted(glob.glob(str(Path(args.logdir) / "*.eval")))
    if not files:
        raise SystemExit(f"no .eval files in {args.logdir}")
    log = read_eval_log(files[-1])
    print(f"log: {files[-1]}")
    print(f"status: {log.status} | samples: {len(log.samples or [])}")

    for s in log.samples or []:
        gl = s.store.get("game_log") or {}
        ops = gl.get("ops", [])
        halts = []
        rejected = []
        for o in ops:
            v = o.get("engine_validated_op") or {}
            if o.get("rejection_reason"):
                rejected.append(o)
            if str(v.get("op", "")).lower() == "halt":
                verdict = (v.get("args") or {}).get("verdict") or v.get("verdict")
                halts.append((verdict, v.get("confidence")))
        scores = {k: (v.value if hasattr(v, "value") else v) for k, v in (s.scores or {}).items()}
        print(f"\n{s.id}: solvable={gl.get('solvable')} terminal={gl.get('terminal')} "
              f"turns={gl.get('turns')} budget_left={gl.get('budget_remaining')}")
        print(f"  halts={halts or 'none'} rejected_ops={len(rejected)} scores={scores}")
        for r in rejected[:3]:
            print(f"  rejected: {str(r.get('rejection_reason'))[:100]}")

        if args.narration_stats:
            inp = s.input.strip() if isinstance(s.input, str) else None
            narr = [m.text for m in s.messages if m.role == "user" and m.text.strip() != inp]
            wc = [len(n.split()) for n in narr[1:]]
            if wc:
                print(f"  narration: n={len(wc)} mean={statistics.mean(wc):.0f}w "
                      f"max={max(wc)}w over120={sum(1 for w in wc if w > 120)}")


if __name__ == "__main__":
    main()
