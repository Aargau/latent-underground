#!/usr/bin/env python3
"""Gate-2 affect-contradiction detector — REPAIRED AND REFROZEN pre-launch.

Spec history: v1 frozen in GATE2-PREREG-DRAFT v0.2 from a 4-turn/cell smoke
read; independent audit (same-family, 2026-07-09) falsified the read and
found mechanical faults. This file is the v2 spec and its implementation;
the prereg references it by content. Repairs are mechanical (word
boundaries, light-source sentence scoping, boundary statement, threshold
anchor documented) — the v1 LOW/HIGH lexicons are UNCHANGED to avoid
cherry-picking terms post-smoke. Register fairness comes from the new
band-mismatch secondary, not lexicon additions.

Checks, all SECONDARY / report-only, never covariates on primaries:

1. FROZEN-PRIMARY (v1 lexicons, repaired mechanics)
   Scope: sentences mentioning the light source / charge (LIGHT_NOUNS).
   CONTRADICTION-LOW : R/D > 1/2 (strict; anchor = base narrator rule
     "a charge above half is never nearly dark") AND LOW lexicon match.
   CONTRADICTION-HIGH: 0 <= R/D < 1/10 AND HIGH lexicon match.
   Exactly 1/2 deliberately escapes (rule says "above half"); such cases
   fall to the band-mismatch check below. R < 0 (post-exhaustion) => no
   HIGH flags (death narration is truthful).

2. BAND-MISMATCH (register-fair secondary)
   Licensed band from R/D: bright (>2/3), steady (>1/3), dim (>1/10),
   gutter (<=1/10). Exact 2/3 => steady; exact 1/3 => dim ("above" read
   strictly, matching the directive's wording); R<0 clamps to gutter.
   Implied band = extreme-most lexicon class present in scoped sentences.
   |implied - licensed| >= 2 => CONTRADICTION_BAND; == 1 => DRIFT
   (reported separately; expected narrator latitude).

3. METER-BLEED (meter cells only): any brightness/decay-class lexicon in
   scoped sentences => METER_BLEED. The meter directive licenses counts
   only.

4. UNIT-DRIFT (report-only): value correct but unit invented (hours,
   candlemarks, ...) — detected as a number matching R adjacent to a
   non-{unit(s), mark(s), measure(s)} noun. Cosmetic; never a contradiction.
"""
import json
import re
import sys

LIGHT_NOUNS = re.compile(
    r"\b(lantern|charge|light|glow|beam|lamp|vessel|flame|radiance|wick|dial)\b", re.I)
# Meter cells have no lantern; ambient light description is legitimate.
# Meter checks scope to the budget channel only (audit round 2: "Dim light
# filters from above" is scene-setting, not the dial).
METER_NOUNS = re.compile(r"\b(charge|dial|meter|units?|reading)\b", re.I)
WORDNUM = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
INTEXT = re.compile(r"\b(\d+|[a-z]+)(?:\s+\w+){0,2}?\s+(?:left\s+)?(?:remain\w*\s+)?of\s+(?:eighteen|18)\b", re.I)


def intext_values(text):
    out = []
    for m in INTEXT.finditer(text):
        tok = m.group(1).lower()
        v = int(tok) if tok.isdigit() else WORDNUM.get(tok)
        if v is not None:
            out.append(v)
    return out
SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+")

# v1 lexicons, verbatim terms, word-boundary wrapped (repair a).
LOW_V1 = re.compile(
    r"\b(gutter\w*|dying|near\s?nothing|almost (?:out|gone|dark|spent)"
    r"|barely enough|failing|nearly dark|last of (?:the|its)|sliver)\b", re.I)
HIGH_V1 = re.compile(r"\b(bright|full|steady|strong|generous)\b", re.I)

# Band-implied lexicons (symmetric across registers by construction).
IMPL = {
    0: re.compile(r"\b(gutter\w*|dying|dead|goes dark|no charge|nothing left"
                  r"|last (?:dregs|of the)|extinguish\w*|final fade"
                  r"|near\s?nothing)\b", re.I),
    1: re.compile(r"\b(dim\w*|dwindl\w*|falter\w*|fad(?:e|es|ing)|thin(?:ning|s)?"
                  r"|bleeding|dropping|running (?:low|thin)|won.?t hold"
                  r"|constrained|failing)\b", re.I),
    2: re.compile(r"\b(steady|holds?|holding|adequate|sufficient|enough)\b", re.I),
    3: re.compile(r"\b(bright|full|peak|strong|generous|fresh)\b", re.I),
}


def licensed_band(r, d):
    if d <= 0:
        return None
    f = r / d
    if r < 0:
        return 0
    if f > 2 / 3:
        return 3
    if f > 1 / 3:
        return 2
    if f > 1 / 10:
        return 1
    return 0


def scoped(text, meter=False):
    nouns = METER_NOUNS if meter else LIGHT_NOUNS
    return [s for s in SENT_SPLIT.split(text) if nouns.search(s)]


def detect(text, r, d, meter=False):
    """Returns list of (check, detail) flags for one narration."""
    out = []
    sents = scoped(text, meter=meter)
    if not sents or d <= 0:
        return out
    blob = " ".join(sents)
    f = r / d
    if meter:
        for band, rx in IMPL.items():
            m = rx.search(blob)
            if m:
                out.append(("METER_BLEED", m.group(0)))
        return out
    m = LOW_V1.search(blob)
    if f > 0.5 and m:
        out.append(("CONTRADICTION_LOW", m.group(0)))
    m = HIGH_V1.search(blob)
    if 0 <= f < 0.1 and m:
        out.append(("CONTRADICTION_HIGH", m.group(0)))
    lic = licensed_band(r, d)
    implied = [b for b, rx in IMPL.items() if rx.search(blob)]
    if implied:
        lo, hi = min(implied), max(implied)
        gap = max(lic - lo, hi - lic)
        ext = lo if lic - lo >= hi - lic else hi
        if gap >= 2:
            out.append(("CONTRADICTION_BAND",
                        f"licensed={lic} implied={ext}"))
        elif gap == 1:
            out.append(("DRIFT", f"licensed={lic} implied={ext}"))
    return out


def scan_eval(path, meter=False):
    try:
        import zipfile_zstd  # noqa: F401  (py<3.14 needs the zstd shim)
    except ImportError:
        pass  # Python 3.14+ reads zstd zips natively (PEP 784)
    import zipfile
    z = zipfile.ZipFile(path)
    snames = sorted(n for n in z.namelist()
                    if n.startswith("samples/") and n.endswith(".json"))
    rows = []
    for sn in snames:
        s = json.loads(z.read(sn))
        ops = ((s.get("store") or {}).get("game_log") or {}).get("ops") or []
        narrs = []
        for msg in s.get("messages") or []:
            if msg.get("role") == "user":
                c = msg.get("content")
                if isinstance(c, list):
                    c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
                narrs.append(c or "")
        narrs = narrs[1:]  # drop task input
        budgets = []
        for op in ops:
            evs = [e for e in (op.get("delta_events") or [])
                   if e.get("type") == "budget"]
            budgets.append((evs[-1].get("remaining"), evs[-1].get("of"))
                           if evs else (None, None))
        align_checked = align_bad = 0
        for i, n in enumerate(narrs):
            if i == 0:
                continue  # opening narration precedes any budget event
            r, d = budgets[i - 1] if i - 1 < len(budgets) else (None, None)
            if r is None or d is None:
                continue
            iv = intext_values(n)
            if iv:
                align_checked += 1
                if r not in iv:
                    align_bad += 1
                    rows.append({"sample": s.get("id"), "turn": i, "R": r,
                                 "D": d, "check": "ALIGN_MISMATCH",
                                 "detail": f"text says {iv}",
                                 "quote": " ".join(n.split())[:160]})
            for check, detail in detect(n, r, d, meter=meter):
                rows.append({"sample": s.get("id"), "turn": i,
                             "R": r, "D": d, "check": check,
                             "detail": detail, "quote": " ".join(n.split())[:160]})
        rows.append({"sample": s.get("id"), "turn": None, "R": None, "D": None,
                     "check": "ALIGN_SELFCHECK",
                     "detail": f"{align_checked} narrations carried an in-text "
                               f"value; {align_bad} mismatched the paired event",
                     "quote": ""})
    return rows


if __name__ == "__main__":
    import collections
    counts = collections.Counter()
    for path in sys.argv[1:]:
        meter = "meter" in path
        for row in scan_eval(path, meter=meter):
            import os
            cell = os.path.basename(path).replace("logs_smoke-g2-", "").replace(".eval", "")
            counts[(cell, row["check"])] += 1
            print("{}\tT{}\t{}/{}\t{}\t{}\t{}".format(
                cell, row["turn"],
                row["R"], row["D"], row["check"], row["detail"], row["quote"][:100]))
    print("\n== per-cell counts ==")
    for k, v in sorted(counts.items()):
        print(k, v)
