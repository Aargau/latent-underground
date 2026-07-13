#!/usr/bin/env python3
"""Scarcity-compression recount v1 - FROZEN CONVENTIONS (committed before
the count below was read; tests prereg key scarcity-compression-prereg-2026-07,
falsifiers F1-F4).

IDIOM CONVENTION (frozen): an idiom maps to its literal landmark value.
"barely/scarcely/just/about/roughly X" implies X (the modifier hedges but
does not move the landmark). "below/under X" implies X minus one scale
tick; "above/over X" implies X plus one tick (tick = D/12). Spent-forms
invert: "X spent/burned/gone/used" implies remaining = D - X.
CONTRADICTION iff |implied_remaining - R| > max(1.5, D/12) (scale-aware
tolerance). DIRECTION = sign(implied - R): negative = narrator understates
remaining (scarcity-ward). Compound fractions parse fully: two-thirds,
three-quarters, four-fifths, three-fifths, five-sixths, N-of-M in words
or digits. Unparseable phrases are reported, never counted either way.
"""
import json, re, sys, collections

WORDNUM = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
for w, v in [("thirty", 30), ("forty", 40), ("fifty", 50), ("sixty", 60), ("seventy", 70), ("eighty", 80), ("ninety", 90)]:
    WORDNUM[w] = v
UNITFRAC = {"half": 1/2, "halves": 1/2, "third": 1/3, "thirds": 1/3, "quarter": 1/4, "quarters": 1/4,
            "fourth": 1/4, "fourths": 1/4, "fifth": 1/5, "fifths": 1/5, "sixth": 1/6, "sixths": 1/6,
            "eighth": 1/8, "eighths": 1/8, "tenth": 1/10, "tenths": 1/10, "twelfth": 1/12, "twelfths": 1/12,
            "sixteenth": 1/16, "sixteenths": 1/16}
NUMPAT = r"(?:\d+|" + "|".join(WORDNUM) + r")"

def wordval(s):
    s = s.lower().strip()
    if s.isdigit(): return int(s)
    if "-" in s:
        parts = s.split("-")
        if all(p in WORDNUM for p in parts): return sum(WORDNUM[p] for p in parts)
    return WORDNUM.get(s)

def parse_implied(phrase, D):
    """Return implied REMAINING, or None if unparseable. Frozen order of rules."""
    pl = " " + phrase.lower().replace("—", " ").replace("-", " ") + " "
    spent = bool(re.search(r"\b(spent|burned|burnt|gone|used|consumed|drained|through)\b", pl))
    # R1: explicit N of/out of/in M (digits or words)
    m = re.search(r"\b(" + NUMPAT + r")\s+(?:\w+\s+){0,3}?(?:of|out of|in)\s+(?:the\s+)?(" + NUMPAT + r")\b", pl)
    if m:
        a, b = wordval(m.group(1)), wordval(m.group(2))
        if a is not None and b:
            v = a / b * D
            return D - v if spent else v
    # R2: compound fraction "N Xths" e.g. two thirds, three quarters, eight sixteenths
    m = re.search(r"\b(" + NUMPAT + r")\s+(" + "|".join(UNITFRAC) + r")\b", pl)
    if m:
        n = wordval(m.group(1)); f = UNITFRAC[m.group(2)]
        if n is not None:
            v = n * f * D
            return D - v if spent else v
    # R3: bare unit fraction "a third", "half"
    m = re.search(r"\b(?:a|an|one)?\s*(" + "|".join(UNITFRAC) + r")\b", pl)
    if m:
        v = UNITFRAC[m.group(1)] * D
        if re.search(r"\b(below|under|less than)\b", pl): v -= D / 12
        if re.search(r"\b(above|over|more than)\b", pl): v += D / 12
        return D - v if spent else v
    # R4: bare count "twelve units/marks/measures remain(ing)/left"
    m = re.search(r"\b(" + NUMPAT + r")\b(?=[^.]{0,30}\b(?:remain|left|charge|units?|marks?|measures?|parts?|glimmers?|notches?|ticks?)\b)", pl)
    if m:
        v = wordval(m.group(1))
        if v is not None and v <= D * 1.5:
            return D - v if spent else v
    return None

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "tmp/hetero_values.jsonl"
    rows = [json.loads(l) for l in open(src, encoding="utf-8") if l.strip()]
    flags = []
    for r in rows:
        for m in (r.get("res") or {}).get("mentions", []):
            if m.get("contradicts"):
                flags.append((r["key"], r["R"], r["D"], m.get("phrase", "")))
    # numeric-bearing filter (same as before): digits, number words, or fraction words
    def numeric_bearing(ph):
        pl = ph.lower()
        return bool(re.search(r"\d", pl) or re.search(r"\b(" + "|".join(list(WORDNUM)) + r")\b", pl)
                    or any(w in pl for w in UNITFRAC))
    cands = [f for f in flags if numeric_bearing(f[3])]
    conf, over, unparsed = [], 0, 0
    for key, R, D, ph in cands:
        v = parse_implied(ph, D)
        if v is None: unparsed += 1; continue
        tol = max(1.5, D / 12)
        if abs(v - R) > tol:
            conf.append((key, R, D, ph, v, v - R))
    under = sum(1 for *_, d in conf if d < 0)
    print(f"flags total: {len(flags)} | numeric-bearing: {len(cands)} | unparsed: {unparsed}")
    print(f"CONFIRMED contradictions (frozen tol): {len(conf)} across {len(set(k for k,*_ in conf))} narrations")
    print(f"DIRECTION: understate-remaining {under}/{len(conf)} = {under/len(conf):.2f}  (F2 tests this)")
    cells = collections.Counter(k.split("|")[0] for k, *_ in conf)
    print("by cell:", dict(cells))
    # F4 landmark clustering: histogram of implied/D
    hist = collections.Counter()
    for _, R, D, _, v, _ in conf:
        hist[round(v / D, 2)] += 1
    top = hist.most_common(8)
    print("implied/D mass (top 8):", top)
    lm = sum(n for frac, n in hist.items() if min(abs(frac - t) for t in (0.25, 1/3, 0.5, 2/3, 0.75)) < 0.04)
    print(f"mass within 0.04 of landmarks (.25,.33,.5,.67,.75): {lm}/{len(conf)} = {lm/len(conf):.2f}  (F4)")
    # truth distribution of the confirmed set, for the attractor-vs-proportional question
    tr = collections.Counter()
    for _, R, D, *_ in conf:
        tr[round(R / D * 4) / 4] += 1
    print("true R/D quartile mix of confirmed set:", dict(sorted(tr.items())))
    with open("/tmp/scarcity_confirmed.json", "w", encoding="utf-8") as f:
        json.dump([{"key": k, "R": R, "D": D, "phrase": p, "implied": v, "delta": d} for k, R, D, p, v, d in conf], f, indent=1)
    print("confirmed rows -> /tmp/scarcity_confirmed.json")

if __name__ == "__main__":
    main()
