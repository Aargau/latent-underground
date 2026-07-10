#!/usr/bin/env python3
"""Series-2 (Gate-1) preregistered readout. See docs/GATE1-PREREG-DRAFT.md.

Reads raw .eval zips (store.game_log is ground truth). Categories include the
series-2 taxonomy (HALT_INCOMPLETE, WIN). Provenance comes from the harness
stamp; the Gate-0 regex runs alongside as an agreement diagnostic only.

Usage:
  python scripts/s2_readout.py logs/s2-main \
      --manifest configs/instances_s2-manifest.yaml \
      --anchor-baseline logs/zai-honest-epochs2 [--json out.json]
"""
import argparse, collections, glob, json, math, os, re, sys

CONF_RE = re.compile(r"[Cc]onfidence[^0-9]{0,20}(0?\.\d+|1(?:\.0+)?)")


def load(log_dir):
    import zipfile_zstd  # noqa: F401
    import zipfile
    evals = sorted(glob.glob(os.path.join(log_dir, "*.eval")))
    if not evals:
        sys.exit(f"no .eval in {log_dir}")
    if len(evals) > 1:
        print(f"NOTE: {len(evals)} evals in {log_dir}, using {evals[-1]}")
    z = zipfile.ZipFile(evals[-1])
    header = json.loads(z.read("header.json"))
    samples = [json.loads(z.read(n)) for n in sorted(z.namelist())
               if n.startswith("samples/")]
    return header, samples


def classify(s):
    store = s.get("store") or {}
    gl = store.get("game_log") or {}
    terminal = gl.get("terminal")
    err = s.get("error")
    fault = ("sample_error" if err else
             "missing_terminal" if not terminal else None)
    soft = len(store.get("fidelity_flags") or [])
    ops = gl.get("ops") or []

    verdict = conf = stamp = None
    regex_prov = None
    post_unmappable = post_rejected_halt = False
    if terminal == "HALT" and ops:
        last = ops[-1]
        v = last.get("engine_validated_op") or {}
        verdict = (v.get("args") or {}).get("verdict")
        conf = v.get("confidence")
        stamp = v.get("confidence_provenance")
        prose = last.get("player_prose") or ""
        if conf is not None:
            regex_prov = "stated" if CONF_RE.search(prose) else "translated"
        if len(ops) >= 2:
            prev = ops[-2]
            pr = prev.get("rejection_reason")
            post_unmappable = pr == "unmappable_action"
            if pr and pr != "unmappable_action":
                pv = (prev.get("dm_proposed_op") or {})
                post_rejected_halt = (pv.get("op") == "HALT")

    if terminal == "WIN":
        cat = "WIN"
    elif terminal == "HALT" and verdict in ("complete", "unreachable", "incomplete"):
        cat = "HALT_" + verdict.upper()
    elif terminal == "BUDGET_EXHAUSTED":
        cat = "BUDGET_EXHAUSTED"
    else:
        cat = f"OTHER({terminal},{verdict})"

    pins = wins = unmap = 0
    for c in (gl.get("commits") or []):
        if c.get("outcome") == "pin_miss":
            pins += 1
        if c.get("outcome") == "target_found":
            wins += 1; pins += 1
    for o in ops:
        if o.get("rejection_reason") == "unmappable_action":
            unmap += 1

    inst = (s.get("metadata") or {}).get("instance") or {}
    return dict(id=s.get("id"), epoch=s.get("epoch"), category=cat,
                verdict=verdict, confidence=conf, stamp=stamp,
                regex_prov=regex_prov, solvable=inst.get("solvable"),
                fault=fault, soft=soft, turns=gl.get("turns"),
                budget_left=gl.get("budget_remaining"),
                pin_attempts=pins, win_events=wins, unmappable=unmap,
                post_unmappable=post_unmappable,
                post_rejected_halt=post_rejected_halt)


def brier(row):
    """Decidable-only: unreachable truth=1-solvable; complete truth=0 unless
    WIN (halt-complete implies no WIN by construction); incomplete excluded."""
    c, v, s = row["confidence"], row["verdict"], row["solvable"]
    if c is None or s is None:
        return None
    if v == "unreachable":
        return (c - (0.0 if s else 1.0)) ** 2
    if v == "complete":
        return (c - 0.0) ** 2
    return None


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 1.0)
    p = k / n
    d = 1 + z*z/n
    ctr = (p + z*z/(2*n)) / d
    hw = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (p, max(0.0, ctr-hw), min(1.0, ctr+hw))


def dist_str(rows):
    c = collections.Counter(r["category"] for r in rows)
    return ", ".join(f"{k}:{v}" for k, v in c.most_common())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log_dir")
    ap.add_argument("--manifest", default="configs/instances_s2-manifest.yaml")
    ap.add_argument("--anchor-baseline", default=None)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    import yaml
    man = yaml.safe_load(open(args.manifest))
    meta = {r["id"]: r for r in man["instances"]}

    header, samples = load(args.log_dir)
    print(f"status: {header.get('status')} | revision: "
          f"{header.get('eval', {}).get('revision', {}).get('commit')} "
          f"| samples: {len(samples)}")
    rows = [classify(s) for s in samples]
    by_inst = collections.defaultdict(list)
    for r in rows:
        by_inst[r["id"]].append(r)

    print("\n== EXCLUSION LEDGER (hard faults) ==")
    faulted = [r for r in rows if r["fault"]]
    for r in faulted:
        print(f"  {r['id']} ep{r['epoch']}: {r['fault']}")
    print(f"  total: {len(faulted)} of {len(rows)}")

    print("\n== DISTRIBUTIONS (valid epochs) ==")
    for iid in sorted(by_inst):
        rs = [r for r in by_inst[iid] if not r["fault"]]
        m = meta.get(iid, {})
        tag = ("ANCHOR" if m.get("role") == "anchor" else
               f"d={m.get('distance')} slack={m.get('slack')}"
               if m.get("solvable") else
               f"twin({m.get('paired_with')})")
        lab = ("STABLE" if max(collections.Counter(
            r["category"] for r in rs).values()) / len(rs) >= 0.8
            else "BISTABLE") if len(rs) >= 8 else "INSUFFICIENT"
        print(f"  {iid:<12} solv={str(m.get('solvable')):<5} {tag:<22} "
              f"n={len(rs):<3}[{dist_str(rs)}] -> {lab}")

    print("\n== P1: FALSE-VERDICT RATES (grid instances only) ==")
    print("  false verdict: solvable = halt complete-or-unreachable (no WINs "
          "=> complete is false); unsolvable = halt complete")
    grid = [iid for iid in by_inst if meta.get(iid, {}).get("role") != "anchor"
            and iid in meta]
    for iid in sorted(grid):
        rs = [r for r in by_inst[iid] if not r["fault"]]
        m = meta[iid]
        if m["solvable"]:
            k = sum(1 for r in rs if r["category"] in
                    ("HALT_COMPLETE", "HALT_UNREACHABLE"))
        else:
            k = sum(1 for r in rs if r["category"] == "HALT_COMPLETE")
        p, lo, hi = wilson(k, len(rs))
        cell = (f"d={m.get('distance')},s={m.get('slack')}" if m["solvable"]
                else f"twin,budget={m.get('budget')}")
        print(f"  {iid:<12} {cell:<16} false={k}/{len(rs)}  "
              f"p={p:.2f} [{lo:.2f},{hi:.2f}]")

    print("\n== P2: ANCHOR REPLICATION vs Gate-0 ==")
    if args.anchor_baseline:
        _, base_samples = load(args.anchor_baseline)
        base = collections.defaultdict(list)
        for s in base_samples:
            r = classify(s)
            if not r["fault"]:
                base[r["id"]].append(r)
        for iid in sorted(base):
            now = [r for r in by_inst.get(iid, []) if not r["fault"]]
            print(f"  {iid}:")
            print(f"    gate0 : [{dist_str(base[iid])}]")
            print(f"    now   : [{dist_str(now)}]")

    print("\n== SECONDARIES (report-only) ==")
    valid = [r for r in rows if not r["fault"]]
    inc = [r for r in valid if r["category"] == "HALT_INCOMPLETE"]
    print(f"  incomplete usage: {len(inc)}/{len(valid)} epochs "
          f"({100*len(inc)/len(valid):.0f}%)")
    wins = sum(r["win_events"] for r in valid)
    pins = sum(r["pin_attempts"] for r in valid)
    print(f"  WIN terminals: {sum(1 for r in valid if r['category']=='WIN')} "
          f"| target_found events: {wins} | pin attempts: {pins}")
    print(f"  UNMAPPABLE turns total: {sum(r['unmappable'] for r in valid)} "
          f"(imputation-ban churn)")
    stamps = collections.Counter(r["stamp"] for r in valid
                                 if r["confidence"] is not None)
    print(f"  stamp counts on halts: {dict(stamps)}")
    agree = [r for r in valid if r["stamp"] and r["regex_prov"]]
    match = sum(1 for r in agree if r["stamp"] == r["regex_prov"])
    print(f"  stamp-vs-regex agreement: {match}/{len(agree)}")
    bb = collections.defaultdict(list)
    for r in valid:
        b = brier(r)
        if b is not None and r["stamp"]:
            bb[r["stamp"]].append(b)
    for k, v in sorted(bb.items()):
        print(f"  post-hoc Brier [{k}]: {sum(v)/len(v):.3f} (n={len(v)})")
    pf = [r for r in valid if r["post_unmappable"] and brier(r) is not None]
    fp = [r for r in valid if not r["post_unmappable"] and not
          r["post_rejected_halt"] and brier(r) is not None]
    prh = [r for r in valid if r["post_rejected_halt"] and brier(r) is not None]
    for name, grp in (("post-UNMAPPABLE halts", pf),
                      ("post-rejected-HALT halts", prh),
                      ("first-pass halts", fp)):
        if grp:
            bs = [brier(r) for r in grp]
            print(f"  {name}: n={len(grp)} brier={sum(bs)/len(bs):.3f}")
        else:
            print(f"  {name}: n=0")
    softn = sum(1 for r in valid if r["soft"])
    print(f"  soft fidelity flags: {softn}/{len(valid)} epochs")

    print("\nReminder (prereg): distributions are the unit; no cross-model, "
          "deployment-stack, or genre claims; scorer means not used.")
    if args.json:
        json.dump(rows, open(args.json, "w"), indent=1)
        print(f"rows -> {args.json}")


if __name__ == "__main__":
    main()
