#!/usr/bin/env python3
"""Build MANIFEST.sha256 for the release bundle: every .eval log plus the
claim-bearing documents. The manifest is committed to the repo (public at
submission) and included in the Zenodo data record, closing the loop:
paper cites Zenodo DOI -> archive verifies against committed manifest ->
readout scripts rerun against verified logs -> claims reproduce.
"""
import hashlib, glob, sys

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

targets = sorted(glob.glob('logs/**/*.eval', recursive=True)) + sorted(glob.glob('docs/*.md')) + sorted(glob.glob('scripts/*.py')) + sorted(glob.glob('configs/instances_s2/*.yaml')) + ['configs/instances_s2-manifest.yaml']
out = open('MANIFEST.sha256', 'w', encoding='utf-8')
for p in targets:
    try:
        out.write(f"{sha(p)}  {p}\n")
    except FileNotFoundError:
        print(f"skip (missing): {p}", file=sys.stderr)
print(f"{len(targets)} entries -> MANIFEST.sha256")
