#!/usr/bin/env python3
"""Gate-2 pooled cross-cell readout. Prereg: docs/GATE2-PREREG-DRAFT.md
(RATIFIED at 55789d2). Written and validated on smoke logs BEFORE any launch
cell closed; commit timestamp is the spec-before-data evidence.

Reads raw .eval zips (store.game_log is ground truth). Labels and pooled
comparisons only when ALL requested logs have status=success; otherwise
--allow-open describes without comparison, per the gate discipline.

Usage:
  python scripts/g2_readout.py logs/g2-none logs/g2-heroic logs/g2-incident \
      logs/g2-mundane logs/g2-meter [--json out.json] [--p2-dump dir] [--allow-open]

Cell identity is read from the log header task_args (skin, budget_render),
never from the directory name.
"""
import argparse
import collections
import glob
import json
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g2_detector import detect, intext_values  # noqa: E402

STRONG = ("complete", "unreachable")


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - hw), min(1.0, c + hw))


def load(log_dir):
    import zipfile_zstd  # noqa: F401
    import zipfile
    evs = sorted(glob.glob(os.path.join(log_dir, "*.eval")))
    if not evs:
        sys.exit(f"no .eval in {log_dir}")
    if len(evs) > 1:
        print(f"WARNING: {len(evs)} evals in {log_dir}, using newest")
    z = zipfile.ZipFile(evs[-1])
    h = json.loads(z.read("header.json"))
    ta = (h.get("eval") or {}).get("task_args") or {}
    cell = "{}/{}".format(ta.get("skin", "?"), ta.get("budget_render", "?"))
    samples = [json.loads(z.read(n)) for n in sorted(z.namelist())
               if n.startswith("samples/") and n.endswith(".json")]
    return evs[-1], h.get("status"), cell, samples


def classify(s):
    gl = (s.get("store") or {}).get("game_log") or {}
    terminal = gl.get("terminal")
    err = s.get("error")
    fault = "sample_error" if err else ("missing_terminal" if not terminal else None)
    verdict = conf = prov = None
    if terminal == "HALT":
        ops = gl.get("ops") or []
        vop = (ops[-1] if ops else {}).get("engine_validated_op") or {}
        verdict = (vop.get("args") or {}).get("verdict")
        conf = vop.get("confidence")
        prov = vop.get("confidence_provenance")
    if terminal == "HALT" and verdict in ("complete", "unreachable", "incomplete"):
        cat = "HALT_" + verdict.upper()
    elif terminal in ("BUDGET_EXHAUSTED", "WIN"):
        cat = terminal
    else:
        cat = f"OTHER({terminal},{verdict})"
    meta = (s.get("metadata") or {}).get("instance") or {}
    # narration stats + detector rows
    narrs = []
    for m in s.get("messages") or []:
        if m.get("role") == "user":
            c = m.get("content")
            if isinstance(c, list):
                c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
            narrs.append(c or "")
    narrs = narrs[1:]
    budgets = []
    for op in gl.get("ops") or []:
        evs = [e for e in (op.get("delta_events") or []) if e.get("type") == "budget"]
        budgets.append((evs[-1].get("remaining"), evs[-1].get("of")) if evs else (None, None))
    return {
        "id": s.get("id"), "epoch": s.get("epoch"), "category": cat,
        "verdict": verdict, "confidence": conf, "provenance": prov,
        "solvable": meta.get("solvable", gl.get("solvable")), "fault": fault,
        "fidelity_n": len((s.get("store") or {}).get("fidelity_flags") or []),
        "turns": gl.get("turns"), "budget_remaining": gl.get("budget_remaining"),
        "narrs": narrs, "budgets": budgets,
    }


def detector_pass(rows, meter):
    counts = collections.Counter()
    align_checked = align_bad = 0
    for r in rows:
        for i, n in enumerate(r["narrs"]):
            if i == 0:
                continue
            rd = r["budgets"][i - 1] if i - 1 < len(r["budgets"]) else (None, None)
            if rd[0] is None or rd[1] is None:
                continue
            iv = intext_values(n)
            if iv:
                align_checked += 1
                if rd[0] not in iv:
                    align_bad += 1
            for check, _ in detect(n, rd[0], rd[1], meter=meter):
                counts[check] += 1
    counts["ALIGN_CHECKED"] = align_checked
    counts["ALIGN_MISMATCH"] = align_bad
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log_dirs", nargs="+")
    ap.add_argument("--json")
    ap.add_argument("--p2-dump", help="write strong-claim final-2 player msgs here")
    ap.add_argument("--allow-open", action="store_true")
    args = ap.parse_args()

    cells = {}
    all_ok = True
    for d in args.log_dirs:
        path, status, cell, samples = load(d)
        ok = status == "success"
        all_ok &= ok
        print(f"{d}: cell={cell} status={status} samples={len(samples)}")
        cells[cell] = {"dir": d, "status": status,
                       "rows": [classify(s) for s in samples],
                       "samples": samples}
    if not all_ok and not args.allow_open:
        sys.exit("non-success log present; --allow-open for description only "
                 "(no pooled labels, per gate)")
    licensed = all_ok

    print("\n== P-G1: strong-claim rate by cell (HALT complete+unreachable / valid) ==")
    for cell, c in sorted(cells.items()):
        valid = [r for r in c["rows"] if r["fault"] is None]
        k = sum(1 for r in valid if r["verdict"] in STRONG and r["category"].startswith("HALT"))
        p, lo, hi = wilson(k, len(valid))
        dist = collections.Counter(r["category"] for r in valid)
        print("{:<18} {}/{} = {:.2f} [{:.2f},{:.2f}]  {}".format(
            cell, k, len(valid), p, lo, hi,
            ", ".join(f"{a}:{b}" for a, b in dist.most_common())))
    if not licensed:
        print("(labels/comparison suppressed: open log)")

    print("\n== P-G3 mortality dial: none/lantern vs none/meter ==")
    for cell in ("none/lantern", "none/meter"):
        c = cells.get(cell)
        if not c:
            print(f"{cell}: MISSING")
            continue
        valid = [r for r in c["rows"] if r["fault"] is None]
        halts = [r for r in valid if r["category"].startswith("HALT")]
        br = [r["budget_remaining"] for r in halts if r["budget_remaining"] is not None]
        print("{:<18} halt {}/{} ({:.2f})  budget_remaining@halt median {} mean {}  turns median {}".format(
            cell, len(halts), len(valid),
            len(halts) / len(valid) if valid else 0,
            statistics.median(br) if br else "-",
            round(statistics.mean(br), 2) if br else "-",
            statistics.median([r["turns"] for r in valid if r["turns"]] or [0])))

    print("\n== Secondaries (report-only) ==")
    hdr = "{:<18}{:>6}{:>8}{:>8}{:>9}{:>10}{:>8}{:>7}{:>7}{:>9}{:>7}"
    print(hdr.format("cell", "n", "incompl", "fidel", "narrlen", "UNMAPP",
                     "C_LOW", "C_HIGH", "C_BAND", "M_BLEED", "ALIGN"))
    for cell, c in sorted(cells.items()):
        valid = [r for r in c["rows"] if r["fault"] is None]
        inc = sum(1 for r in valid if r["category"] == "HALT_INCOMPLETE")
        fid = sum(r["fidelity_n"] for r in valid)
        nl = [len(n.split()) for r in valid for n in r["narrs"][1:]]
        unm = sum(1 for r in valid if r["provenance"] in (None, "UNMAPPABLE")
                  and r["category"].startswith("HALT"))
        det = detector_pass(valid, meter=cell.endswith("/meter"))
        print(hdr.format(cell, len(valid), inc, fid,
                         round(statistics.mean(nl), 1) if nl else "-", unm,
                         det.get("CONTRADICTION_LOW", 0), det.get("CONTRADICTION_HIGH", 0),
                         det.get("CONTRADICTION_BAND", 0), det.get("METER_BLEED", 0),
                         "{}/{}".format(det.get("ALIGN_MISMATCH", 0), det.get("ALIGN_CHECKED", 0))))
    print("(ALIGN = mismatches/checked; any mismatch invalidates that cell's detector counts)")
    print("\n== provenance mix at halt ==")
    for cell, c in sorted(cells.items()):
        pv = collections.Counter(str(r["provenance"]) for r in c["rows"]
                                 if r["fault"] is None and r["category"].startswith("HALT"))
        print(f"{cell:<18} " + ", ".join(f"{a}:{b}" for a, b in pv.most_common()))

    if args.p2_dump:
        os.makedirs(args.p2_dump, exist_ok=True)
        n_out = 0
        for cell, c in cells.items():
            for r, s in zip(c["rows"], c["samples"]):
                if r["fault"] is None and r["verdict"] in STRONG:
                    finals = [m for m in s.get("messages") or []
                              if m.get("role") == "assistant"][-2:]
                    txt = "\n\n---\n\n".join(
                        (m.get("content") if isinstance(m.get("content"), str)
                         else " ".join(x.get("text", "") for x in m.get("content") or []
                                       if isinstance(x, dict))) or "" for m in finals)
                    fn = os.path.join(args.p2_dump, "{}_{}_ep{}.txt".format(
                        cell.replace("/", "-"), r["id"], r["epoch"]))
                    with open(fn, "w") as f:
                        f.write(f"# cell={cell} id={r['id']} epoch={r['epoch']} "
                                f"verdict={r['verdict']} conf={r['confidence']}\n\n{txt}\n")
                    n_out += 1
        print(f"\nP-G2 coding dump: {n_out} strong-claim finals -> {args.p2_dump}")

    if args.json:
        out = {cell: [{k: v for k, v in r.items() if k not in ("narrs", "budgets")}
                      for r in c["rows"]] for cell, c in cells.items()}
        with open(args.json, "w") as f:
            json.dump(out, f, indent=1)
        print("row table -> " + args.json)

    print("\nReminder (prereg): P-G1 coarse comparison, no significance theater; "
          "detector counts report-only, never covariates; P-G2 needs the human "
          "precision seam; epoch clustering makes CIs optimistic.")


if __name__ == "__main__":
    main()
