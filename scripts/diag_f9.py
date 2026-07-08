#!/usr/bin/env python3
"""F9 diagnostic: are unparseable_proposal rejections interpreter truncation?

Compares rejection rates between two runs and dumps raw op records from the
first rejected turns to see what the interpreter actually emitted.
"""
import glob
import json
import sys
from pathlib import Path

from inspect_ai.log import read_eval_log


def rej_rate(logdir: str) -> None:
    files = sorted(glob.glob(str(Path(logdir) / "*.eval")))
    log = read_eval_log(files[-1])
    print(f"\n=== {logdir} ===")
    for s in log.samples or []:
        gl = s.store.get("game_log") or {}
        ops = gl.get("ops", [])
        rej = [o for o in ops if o.get("rejection_reason")]
        print(f"{s.id}: {len(rej)}/{len(ops)} rejected "
              f"({', '.join(sorted(set(str(o.get('rejection_reason')) for o in rej)) ) or 'none'})")


def dump_ops(logdir: str, n: int = 2) -> None:
    files = sorted(glob.glob(str(Path(logdir) / "*.eval")))
    log = read_eval_log(files[-1])
    s = log.samples[0]
    gl = s.store.get("game_log") or {}
    ops = gl.get("ops", [])
    rejected = [o for o in ops if o.get("rejection_reason")][:n]
    print(f"\n=== raw rejected ops from {s.id} ===")
    for o in rejected:
        print(json.dumps({k: (str(v)[:220] if v is not None else None) for k, v in o.items()}, indent=1))


if __name__ == "__main__":
    dirs = sys.argv[1:] or ["logs/validation-f8", "logs/glm-overnight-f8"]
    for d in dirs:
        rej_rate(d)
    dump_ops(dirs[-1], n=4)
