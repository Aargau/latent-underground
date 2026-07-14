#!/usr/bin/env python3
"""Convert a pasted rater reply (lines of "case_id: Y|N|O") into the
rulings.json shape that scripts/irr_kappa.py consumes.

Validates: exactly the 28 IRR case ids, each once, verdicts in {Y,N,O}.
Anything after a "## notes" line is preserved to the output as 'notes'.

Usage: python scripts/parse_rater_lines.py REPLY.txt RATER_NAME OUT.json
"""
import json
import re
import sys
import time


def main():
    reply, rater, out = sys.argv[1], sys.argv[2], sys.argv[3]
    cases = json.load(open("tmp/rater_cases_irr.json", encoding="utf-8"))
    ids = {c["id"] for c in cases}
    text = open(reply, encoding="utf-8").read()
    body, _, notes = text.partition("## notes")
    R = {}
    for line in body.splitlines():
        m = re.match(r"\s*([\w:.\-]+::[abc])\s*[:=]\s*([YNO])\b", line.strip())
        if not m:
            continue
        cid, v = m.group(1), m.group(2)
        if cid not in ids:
            sys.exit(f"unknown case id: {cid}")
        if cid in R:
            sys.exit(f"duplicate ruling for {cid}")
        R[cid] = {"v": v, "note": "", "t": int(time.time() * 1000), "order": len(R)}
    missing = ids - set(R)
    if missing:
        sys.exit(f"missing {len(missing)} rulings: {sorted(missing)[:5]}...")
    json.dump({"rater": rater, "rulings": R, "timing": {},
               "notes": notes.strip()}, open(out, "w", encoding="utf-8"), indent=1)
    print(f"wrote {out}: 28/28 rulings for rater '{rater}'")


if __name__ == "__main__":
    main()
