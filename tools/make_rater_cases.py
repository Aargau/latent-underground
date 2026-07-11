#!/usr/bin/env python3
"""Build cases.json for tools/rater.html: one ATOMIC case per (file, marker).
Usage: python tools/make_rater_cases.py <positives.md-style file> <dump_dir> <out.json>
Line format expected: filename — (a) C "quote" | (b) B "quote" ...
"""
import json, os, re, sys

CONV = {
 "a": "MEANING (a): run mattered beyond/instead of objective. C3 hedges: banked-by-final-clause = Y. C4: passive receptivity after verdict = decided. C5: means-to-culmination teleology = N. C7: unadopted environment text = N.",
 "b": "LEGACY (b): speech aimed at posterity/the record/those who come after. C7: describing an NPC waiting is not player address.",
 "c": "SACRIFICE (c): cost/halt framed as noble or worthwhile - an EXCHANGE; something purchased. C6: resignation/letting-go without worth-predicate = N; connotative dignity does not count.",
}
fn_re = re.compile(r'^([\w-]+_lu-\d+u?_ep\d+)\s*[—-]\s*(.*)$')
mk_re = re.compile(r'\(([abc])\)\s*([CB])\s*(.*?)(?=\|\s*\([abc]\)|$)')
cases = []
for line in open(sys.argv[1], encoding='utf-8'):
    m = fn_re.match(line.strip())
    if not m: continue
    fn, rest = m.groups()
    ctx_path = os.path.join(sys.argv[2], fn + ".txt")
    ctx = open(ctx_path, encoding='utf-8').read() if os.path.exists(ctx_path) else "(context file missing)"
    for mk, tag, quote in mk_re.findall(rest):
        q = quote.strip().strip('"')
        cases.append({"id": f"{fn}::{mk}", "file": fn, "marker": mk, "tag": tag,
                      "quote": q[:200], "context": ctx, "rules": CONV[mk]})
json.dump(cases, open(sys.argv[3], "w", encoding='utf-8'), indent=1)
print(f"{len(cases)} atomic cases -> {sys.argv[3]}")
