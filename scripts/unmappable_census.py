#!/usr/bin/env python3
"""UNMAPPABLE census, one counter, both series (hostile attack 11).

The attack: "UNMAPPABLE 33 (series 2) -> 0 (Gate 2) unexplained." But the
two figures may come from DIFFERENT counters: s2_readout counts turn-level
interpreter friction (ops with rejection_reason == "unmappable_action");
g2_readout's UNMAPPABLE line counts halt-stamp confidence_provenance. This
script applies BOTH counters uniformly to every log so the drift question
is grounded in one metric before it is explained.

Per log it reports:
  A. turn-level UNMAPPABLE ops (rejection_reason == "unmappable_action"):
     total, games affected, per-instance distribution, and the FULL player
     prose of every such op (the ground truth of what the interpreter
     refused to map).
  B. halt-stamp provenance counter (None / UNMAPPABLE / stated /
     translated) over HALT games.
  C. denominators: valid games, total ops.

Usage: python scripts/unmappable_census.py LOGDIR_OR_EVAL [...]
For dirs with launch debris (g2-meter) pass the .eval file directly.
"""
import glob
import json
import os
import sys

try:
    import zipfile_zstd  # noqa: F401  (py<3.14 zstd shim)
except ImportError:
    pass  # PEP 784: py3.14+ native
import zipfile
import collections


def resolve(path):
    if path.endswith(".eval"):
        return path
    evs = sorted(glob.glob(os.path.join(path, "*.eval")))
    if not evs:
        sys.exit(f"no .eval in {path}")
    if len(evs) > 1:
        print(f"  WARNING: {len(evs)} evals in {path}, using newest "
              f"({os.path.basename(evs[-1])}) — pass a file to override")
    return evs[-1]


def census(path):
    ev = resolve(path)
    z = zipfile.ZipFile(ev)
    h = json.loads(z.read("header.json"))
    ta = (h.get("eval") or {}).get("task_args") or {}
    cell = "{}/{}".format(ta.get("skin", "-"), ta.get("budget_render", "-"))
    status = h.get("status")
    samples = [json.loads(z.read(n)) for n in sorted(z.namelist())
               if n.startswith("samples/") and n.endswith(".json")]
    print(f"\n=== {ev}\n    cell={cell} status={status} samples={len(samples)}")

    unmap_ops = []           # (id, epoch, turn_idx, player_prose)
    prov = collections.Counter()
    total_ops = valid = halts = 0
    per_inst = collections.Counter()
    for s in samples:
        gl = (s.get("store") or {}).get("game_log") or {}
        if s.get("error") or not gl.get("terminal"):
            continue
        valid += 1
        ops = gl.get("ops") or []
        total_ops += len(ops)
        for i, o in enumerate(ops):
            if o.get("rejection_reason") == "unmappable_action":
                unmap_ops.append((s.get("id"), s.get("epoch"), i,
                                  (o.get("player_prose") or "")))
                per_inst[s.get("id")] += 1
        if gl.get("terminal") == "HALT":
            halts += 1
            vop = (ops[-1] if ops else {}).get("engine_validated_op") or {}
            prov[str(vop.get("confidence_provenance"))] += 1

    print(f"    valid={valid} halts={halts} total_ops={total_ops}")
    print(f"    A. turn-level UNMAPPABLE ops: {len(unmap_ops)} "
          f"in {len(per_inst)} games "
          f"(rate {len(unmap_ops)/total_ops:.4f}/op)" if total_ops else "")
    if per_inst:
        print(f"       per-instance: {dict(per_inst)}")
    print(f"    B. halt-stamp provenance: {dict(prov)}")
    for gid, ep, ti, prose in unmap_ops:
        print(f"\n    -- {gid} ep{ep} turn{ti} PLAYER PROSE:\n{prose}")
    return len(unmap_ops), dict(prov), valid, total_ops


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    grand = 0
    for p in sys.argv[1:]:
        n, _, _, _ = census(p)
        grand += n
    print(f"\nGRAND turn-level UNMAPPABLE total: {grand}")
