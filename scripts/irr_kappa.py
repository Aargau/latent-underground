#!/usr/bin/env python3
"""Human inter-rater reliability: expert judge (Justin, frozen JUSTIN-P
prompt) vs independent second coder (rules-only workbench screens).

CONVENTIONS — FROZEN BEFORE THE SECOND CODER'S LABELS WERE READ:
K1 PRIMARY: two-category Cohen's kappa (Y vs N) over pairs where both
   raters ruled Y or N. Second-coder O ("cannot decide") excluded
   pairwise, count reported. (The judge's cache contains only Y/N.)
K2 SECONDARY: three-category kappa (Y/N/O) if any O present.
K3 Per-marker raw agreement for (a)/(b)/(c); kappa only where n permits
   (pooled and (a); (b) n=3 and (c) n=7 report raw agreement only).
K4 Pre-stated comparisons: model-family raw agreement with the judge was
   terra .72 and GLM .70; the robustness hierarchy predicts (a) most
   agreed, (c) most contested; mundane (a) floor should surface as
   N-agreement on any mundane (a) cases.
K5 Report second-coder timing (median s/case, flip count) as workbench
   metadata.
K6 Small-n honesty: n=28; kappa 95% CI by large-sample SE is
   approximate; report counts alongside every rate.

Usage: python scripts/irr_kappa.py tmp/adj_cache.txt "tmp/joeg export.json" tmp/rater_cases_irr.json
"""
import json
import math
import statistics
import sys


def load_judge(path):
    j = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        f = parts[0]
        for seg in parts[1:]:
            m, tag, v = seg.split(":")
            j[f"{f}::{m}"] = {"v": v, "tag": tag}
    return j


def kappa(pairs, cats):
    n = len(pairs)
    po = sum(1 for a, b in pairs if a == b) / n
    pe = 0.0
    for c in cats:
        pa = sum(1 for a, _ in pairs if a == c) / n
        pb = sum(1 for _, b in pairs if b == c) / n
        pe += pa * pb
    if pe == 1.0:
        return po, pe, float("nan"), (float("nan"), float("nan"))
    k = (po - pe) / (1 - pe)
    se = math.sqrt(po * (1 - po) / n) / (1 - pe)  # approximate
    return po, pe, k, (k - 1.96 * se, k + 1.96 * se)


def main():
    judge_path, second_path, cases_path = sys.argv[1], sys.argv[2], sys.argv[3]
    judge = load_judge(judge_path)
    second = json.load(open(second_path, encoding="utf-8"))
    cases = json.load(open(cases_path, encoding="utf-8"))
    R = second["rulings"]

    rows = []
    for c in cases:
        cid = c["id"]
        assert cid in judge, f"case {cid} missing from judge cache"
        assert cid in R, f"case {cid} missing from second coder"
        rows.append({"id": cid, "marker": c["marker"], "file": c["file"],
                     "judge": judge[cid]["v"], "tag": judge[cid]["tag"],
                     "second": R[cid]["v"], "note": R[cid].get("note", "")})

    print(f"mapped {len(rows)}/28 cases; rater field: {second.get('rater')}")
    o_rows = [r for r in rows if r["second"] == "O"]
    yn = [r for r in rows if r["second"] in ("Y", "N")]
    print(f"second-coder O rulings: {len(o_rows)} "
          f"({[r['id'] for r in o_rows]})")

    print("\n== K1 PRIMARY: two-category kappa (O excluded pairwise) ==")
    pairs = [(r["judge"], r["second"]) for r in yn]
    po, pe, k, ci = kappa(pairs, ["Y", "N"])
    a = sum(1 for x, y in pairs if x == y)
    yy = sum(1 for x, y in pairs if x == "Y" and y == "Y")
    nn = sum(1 for x, y in pairs if x == "N" and y == "N")
    jy_sn = sum(1 for x, y in pairs if x == "Y" and y == "N")
    jn_sy = sum(1 for x, y in pairs if x == "N" and y == "Y")
    print(f"n={len(pairs)} agree={a} ({po:.3f}) | Y/Y {yy}, N/N {nn}, "
          f"judgeY/secondN {jy_sn}, judgeN/secondY {jn_sy}")
    print(f"pe={pe:.3f} kappa={k:.3f} approx95CI=({ci[0]:.3f},{ci[1]:.3f})")

    if o_rows:
        print("\n== K2 SECONDARY: three-category kappa ==")
        pairs3 = [(r["judge"], r["second"]) for r in rows]
        po3, pe3, k3, ci3 = kappa(pairs3, ["Y", "N", "O"])
        print(f"n={len(pairs3)} po={po3:.3f} pe={pe3:.3f} kappa={k3:.3f} "
              f"approx95CI=({ci3[0]:.3f},{ci3[1]:.3f})")

    print("\n== K3 per-marker ==")
    for m in "abc":
        mr = [r for r in rows if r["marker"] == m]
        myn = [r for r in mr if r["second"] in ("Y", "N")]
        ag = sum(1 for r in myn if r["judge"] == r["second"])
        line = f"({m}) n={len(mr)} (O={len(mr)-len(myn)}) raw agreement {ag}/{len(myn)}"
        if m == "a" and len(myn) >= 10:
            _, _, ka, cia = kappa([(r['judge'], r['second']) for r in myn], ["Y", "N"])
            line += f" kappa={ka:.3f} approx95CI=({cia[0]:.3f},{cia[1]:.3f})"
        print(line)

    print("\n== disagreements (full list) ==")
    for r in rows:
        if r["second"] == "O" or r["judge"] != r["second"]:
            note = f" note[{r['note']}]" if r["note"] else ""
            print(f"  {r['id']}  judge={r['judge']}(tag {r['tag']}) "
                  f"second={r['second']}{note}")

    print("\n== K5 workbench metadata ==")
    T = second.get("timing", {})
    Rl = second["rulings"]
    ts = sorted((v["t"], k) for k, v in Rl.items())
    gaps = [(ts[i][0] - ts[i-1][0]) / 1000 for i in range(1, len(ts))]
    gaps = [g for g in gaps if g < 600]
    flips = sum(len(v.get("flips", [])) for v in T.values())
    total = (ts[-1][0] - ts[0][0]) / 1000 if len(ts) > 1 else 0
    print(f"median {statistics.median(gaps):.0f}s/case, "
          f"max gap<10min {max(gaps):.0f}s, total span {total/60:.0f}min, "
          f"answer flips: {flips}, notes written: "
          f"{sum(1 for v in Rl.values() if v.get('note'))}")

    print("\nK4 pre-stated comparisons: terra-judge .72, GLM-judge .70 raw; "
          "hierarchy predicts (a) most agreed, (c) most contested.")


if __name__ == "__main__":
    main()
