#!/usr/bin/env python3
"""Stamp-audit sampler (hostile attack 11; rubric: docs/G2-STAMP-AUDIT.md).

Enumerates the frame — all valid HALT games across the five Gate-2 cells —
sorted by (cell, id, epoch), draws n=30 with random.Random(11107).sample,
and dumps each sampled game's FULL final player message plus the
engine_validated_op record (verdict, confidence, confidence_provenance)
for human/model reads. Also dumps the two DIRECTED reads (lu-900004u true
unreachables) outside the sample, labeled.

The frame ordering, seed, and draw are deterministic from the shipped
logs; anyone can reproduce the sample membership.

Usage: python scripts/stamp_audit_sample.py LOG_OR_EVAL... [--out FILE]
"""
import argparse
import glob
import json
import os
import random
import sys

try:
    import zipfile_zstd  # noqa: F401
except ImportError:
    pass
import zipfile

SEED = 11107
N = 30


def resolve(path):
    if path.endswith(".eval"):
        return path
    evs = sorted(glob.glob(os.path.join(path, "*.eval")))
    if not evs:
        sys.exit(f"no .eval in {path}")
    if len(evs) > 1:
        print(f"WARNING: {len(evs)} evals in {path}, using newest")
    return evs[-1]


def halts(path):
    z = zipfile.ZipFile(resolve(path))
    h = json.loads(z.read("header.json"))
    ta = (h.get("eval") or {}).get("task_args") or {}
    cell = "{}-{}".format(ta.get("skin", "-"), ta.get("budget_render", "-"))
    out = []
    for n in sorted(z.namelist()):
        if not (n.startswith("samples/") and n.endswith(".json")):
            continue
        s = json.loads(z.read(n))
        gl = (s.get("store") or {}).get("game_log") or {}
        if s.get("error") or gl.get("terminal") != "HALT":
            continue
        ops = gl.get("ops") or []
        last = ops[-1] if ops else {}
        vop = last.get("engine_validated_op") or {}
        out.append({
            "cell": cell, "id": s.get("id"), "epoch": s.get("epoch"),
            "verdict": (vop.get("args") or {}).get("verdict"),
            "confidence": vop.get("confidence"),
            "provenance": vop.get("confidence_provenance"),
            "final_player_message": last.get("player_prose") or "",
        })
    return out


def fmt(g, tag):
    return ("\n" + "=" * 72 +
            f"\n[{tag}] {g['cell']} {g['id']} ep{g['epoch']}"
            f"\nverdict={g['verdict']} confidence={g['confidence']}"
            f" provenance={g['provenance']}"
            f"\n--- FINAL PLAYER MESSAGE ---\n{g['final_player_message']}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="+")
    ap.add_argument("--out", default="tmp/stamp_audit_sample.txt")
    args = ap.parse_args()

    frame = []
    for p in args.logs:
        frame.extend(halts(p))
    frame.sort(key=lambda g: (g["cell"], str(g["id"]), g["epoch"]))
    print(f"frame: {len(frame)} HALT games "
          f"(cells: {sorted(set(g['cell'] for g in frame))})")

    rng = random.Random(SEED)
    idx = sorted(rng.sample(range(len(frame)), N))
    sample = [frame[i] for i in idx]

    directed = [g for g in frame
                if "900004u" in str(g["id"]) and g["verdict"] == "unreachable"]

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(f"frame={len(frame)} seed={SEED} n={N} indices={idx}\n")
        comp = {}
        for g in sample:
            comp[g["cell"]] = comp.get(g["cell"], 0) + 1
        f.write(f"per-cell composition: {comp}\n")
        for g in sample:
            f.write(fmt(g, "SAMPLE"))
        for g in directed:
            f.write(fmt(g, "DIRECTED lu-900004u"))
    print(f"wrote {args.out}: {N} sampled + {len(directed)} directed")
    print(f"per-cell: {comp}")


if __name__ == "__main__":
    main()
