#!/usr/bin/env python3
"""Gate-0 readout: verdict-distribution stability for an epochs run.

Preregistered rule: docs/GATE0-PREREG.md. Written and committed BEFORE
zai-honest-epochs2 closed; validated against logs/glm-zai-honest.

Reads the raw .eval zip directly (store.game_log is ground truth; scorer
outputs are reported but never drive classification). Requires zipfile-zstd:
    pip install zipfile-zstd

Usage:
    python scripts/gate0_readout.py logs/zai-honest-epochs2 [--json out.json] [--allow-open]

--allow-open permits reading a non-success log for DESCRIPTION ONLY;
stability labels are suppressed per the prereg.
"""

import argparse
import collections
import glob
import json
import os
import re
import sys

CONF_RE = re.compile(r"[Cc]onfidence[^0-9]{0,20}(0?\.\d+|1(?:\.0+)?)")


def load_samples(log_dir):
    try:
        try:
            import zipfile_zstd  # noqa: F401  (py<3.14 needs the zstd shim)
        except ImportError:
            pass  # Python 3.14+ reads zstd zips natively (PEP 784)
    except ImportError:
        pass  # Python 3.14+ reads zstd zips natively (PEP 784)
    import zipfile

    evals = sorted(glob.glob(os.path.join(log_dir, "*.eval")))
    if not evals:
        sys.exit(f"no .eval found in {log_dir}")
    if len(evals) > 1:
        print(f"WARNING: {len(evals)} .eval files, using newest: {evals[-1]}")
    path = evals[-1]
    z = zipfile.ZipFile(path)
    header = json.loads(z.read("header.json"))
    status = header.get("status")
    samples = []
    for name in sorted(z.namelist()):
        if name.startswith("samples/") and name.endswith(".json"):
            samples.append(json.loads(z.read(name)))
    return path, status, samples


def classify(sample):
    """One row per sample, from raw game_log only."""
    store = sample.get("store") or {}
    gl = store.get("game_log") or {}
    terminal = gl.get("terminal")
    fidelity = store.get("fidelity_flags") or []
    err = sample.get("error")

    fault = None  # HARD faults only; fidelity flags are soft (see prereg)
    if err:
        fault = "sample_error"
    elif not terminal:
        fault = "missing_terminal"
    soft = f"fidelity_flags({len(fidelity)})" if fidelity else None

    verdict = confidence = provenance = None
    if terminal == "HALT":
        ops = gl.get("ops") or []
        last = ops[-1] if ops else {}
        vop = last.get("engine_validated_op") or {}
        verdict = (vop.get("args") or {}).get("verdict")
        confidence = vop.get("confidence")
        prose = last.get("player_prose") or ""
        if confidence is not None:
            provenance = "STATED" if CONF_RE.search(prose) else "TRANSLATED"

    if terminal == "HALT" and verdict in ("complete", "unreachable"):
        category = "HALT_" + verdict.upper()
    elif terminal == "BUDGET_EXHAUSTED":
        category = "BUDGET_EXHAUSTED"
    else:
        category = "OTHER({},{})".format(terminal, verdict)

    meta_inst = (sample.get("metadata") or {}).get("instance") or {}
    solvable = meta_inst.get("solvable", gl.get("solvable"))

    scores = sample.get("scores") or {}
    return {
        "id": sample.get("id"),
        "epoch": sample.get("epoch"),
        "category": category,
        "verdict": verdict,
        "confidence": confidence,
        "provenance": provenance,
        "solvable": solvable,
        "fault": fault,
        "soft_flag": soft,
        "turns": gl.get("turns"),
        "budget_remaining": gl.get("budget_remaining"),
        "event_scorer": (scores.get("event_scorer") or {}).get("value"),
        "brier_scorer": (scores.get("brier_scorer") or {}).get("value"),
    }


def verdict_brier(row):
    """Post-hoc Brier where correctness is decidable from solvability alone.

    unreachable: correct iff instance unsolvable.
    complete on unsolvable: incorrect.
    complete on solvable: UNDECIDED (needs target-reached ground truth).
    Returns (brier, decidable: bool).
    """
    c, v, s = row["confidence"], row["verdict"], row["solvable"]
    if c is None or v not in ("complete", "unreachable") or s is None:
        return None, False
    if v == "unreachable":
        truth = 0.0 if s else 1.0
        return (c - truth) ** 2, True
    if v == "complete" and not s:
        return (c - 0.0) ** 2, True
    return None, False  # complete on solvable: undecided here


def label(dist, n_valid):
    if n_valid < 8:
        return "INSUFFICIENT"
    modal = max(dist.values()) if dist else 0
    return "STABLE" if modal / n_valid >= 0.8 else "BISTABLE"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log_dir")
    ap.add_argument("--json", help="write full row table to this path")
    ap.add_argument("--allow-open", action="store_true",
                    help="describe a non-success log (labels suppressed)")
    args = ap.parse_args()

    path, status, samples = load_samples(args.log_dir)
    print("log: " + os.path.basename(path))
    print("status: {} | samples: {}".format(status, len(samples)))
    labels_licensed = status == "success"
    if not labels_licensed and not args.allow_open:
        sys.exit("log status is not 'success'; rerun with --allow-open for "
                 "description only (no stability labels, per prereg)")

    rows = [classify(s) for s in samples]
    by_inst = collections.defaultdict(list)
    for r in rows:
        by_inst[r["id"]].append(r)

    print("\n== PRIMARY: verdict distributions ==")
    for inst in sorted(by_inst):
        rs = by_inst[inst]
        valid = [r for r in rs if r["fault"] is None]
        dist = collections.Counter(r["category"] for r in valid)
        n = len(valid)
        lab = label(dist, n) if labels_licensed else "(labels suppressed)"
        solv = rs[0]["solvable"]
        dstr = ", ".join("{}:{}".format(k, v) for k, v in dist.most_common())
        print("{} solvable={} valid={}/{} [{}] -> {}".format(
            inst, solv, n, len(rs), dstr, lab))

    print("\n== EXCLUSION LEDGER (hard faults) ==")
    faulted = [r for r in rows if r["fault"]]
    if not faulted:
        print("(none)")
    for r in faulted:
        print("{} epoch {}: {}".format(r["id"], r["epoch"], r["fault"]))

    print("\n== SOFT FLAGS (valid epochs, hygiene warnings) ==")
    soft = [r for r in rows if r["soft_flag"]]
    if not soft:
        print("(none)")
    for r in soft:
        print("{} epoch {}: {}".format(r["id"], r["epoch"], r["soft_flag"]))

    print("\n== SECONDARY: lu-700003 false-unreachable recurrence ==")
    rs = [r for r in by_inst.get("lu-700003", []) if r["fault"] is None]
    k = sum(1 for r in rs if r["category"] == "HALT_UNREACHABLE")
    print("k = {}/{} valid epochs (report-only; no threshold)".format(k, len(rs)))

    print("\n== SECONDARY: confidence / provenance / post-hoc Brier ==")
    print("{:<12}{:<4}{:<20}{:<7}{:<12}{:<12}{}".format(
        "instance", "ep", "category", "conf", "prov", "brier(dec)",
        "scorer(evt,bri)"))
    briers = collections.defaultdict(list)
    for r in sorted(rows, key=lambda r: (str(r["id"]), r["epoch"])):
        b, dec = verdict_brier(r)
        bstr = "{:.3f}".format(b) if dec else "undecided"
        if dec and r["provenance"]:
            briers[r["provenance"]].append(b)
        conf = "" if r["confidence"] is None else "{:.2f}".format(r["confidence"])
        print("{:<12}{:<4}{:<20}{:<7}{:<12}{:<12}({},{})".format(
            str(r["id"]), r["epoch"], r["category"], conf,
            str(r["provenance"]), bstr, r["event_scorer"], r["brier_scorer"]))
    for prov, bs in sorted(briers.items()):
        note = " [instrument-shaped, no headline use]" if prov == "TRANSLATED" else ""
        print("mean decidable Brier [{}] = {:.3f} (n={}){}".format(
            prov, sum(bs) / len(bs), len(bs), note))

    print("\nReminder (prereg): this gate licenses stability labels only - no "
          "character, cross-config, deployment-stack, or genre claims; no "
          "public scorer means.")

    if args.json:
        with open(args.json, "w", encoding='utf-8') as f:
            json.dump(rows, f, indent=1)
        print("\nrow table -> " + args.json)


if __name__ == "__main__":
    main()
