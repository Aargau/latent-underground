# RELEASE BUNDLE - arXiv submission architecture

Three artifacts, three jobs, one verification loop.

1. ARXIV: paper source only (LaTeX + figures). No data. The paper's
   claims-to-evidence ledger cites (a) the GitHub tag and (b) the Zenodo
   DOI below. Optionally attach the two prereg PDFs as ancillary files
   (small); the repo copies are canonical.
2. GITHUB (this repo, flipped PUBLIC at submission, tagged v1.0-arxiv):
   code, preregistrations with their FULL COMMIT HISTORY - the
   rules-before-results chain (ratification 55789d2 -> 081586f, readout
   05acada before first cell closed, etc.) becomes publicly verifiable
   against GitHub's server timestamps. Also: coding records, results
   docs, MANIFEST.sha256. Logs are gitignored and never entered history;
   held-out instances (configs/instances/heldout/) likewise, preserving
   future eval validity. Secrets sweep: clean (verified pre-flip).
   Enable the GitHub-Zenodo integration on the tag for a code DOI.
3. ZENODO (data record, DOI cited in paper): logs.tar.zst containing all
   .eval files (48MB total - already zstd inside), the derived-data files
   (tmp/hetero_values.jsonl, tmp/p2final.jsonl), and a copy of
   MANIFEST.sha256. CC BY 4.0, matching the paper.

Verification loop for any reader: check commit timestamps on GitHub
(rules before results) -> download Zenodo archive -> sha256 -c
MANIFEST.sha256 (logs match what the committed manifest promised) ->
rerun scripts/*_readout.py and scripts/scarcity_recount.py -> reproduce
every table.

SUBMISSION CHECKLIST
- [ ] python scripts/make_manifest.py ; commit MANIFEST.sha256
- [ ] tar + zstd the logs/ tree and derived data; upload to Zenodo; DOI
- [ ] paste DOI into paper's data-availability statement
- [ ] provider terms check: publication of model outputs as research
      data (Anthropic + z.ai) - reviewed and noted in the paper
- [ ] repo -> public; tag v1.0-arxiv; enable Zenodo code archiving
- [ ] arXiv submit (cs.AI primary, cs.CL cross); endorsement code ready
