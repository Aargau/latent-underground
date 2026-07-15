# FLIP-DAY RUNBOOK — arXiv submission, paper 1

Execute top to bottom in one afternoon. Steps marked ONLY-YOU require your
hands (I cannot flip repo visibility, accept terms, upload to Zenodo, or
submit). Steps marked IRREVERSIBLE do not undo cleanly; read them before
running them. Everything before Phase 5 is reversible.

Repo: github.com/Aargau/latent-underground   Tag to cut: v1.0-arxiv
Submission: arXiv, primary cs.AI, cross-list cs.CL, license CC BY 4.0

Precondition already met: manuscript final, 37 refs verified, endorsement
live (Mihaela), reproduction loop executable, provider terms cleared.

---

## PHASE 0 — PRE-FLIGHT (reversible)

0.1  Clean tree, everything pushed:
       git status          # expect: clean, up to date with origin/main

0.2  SECRETS SWEEP (gate before anything goes public). Confirm no keys,
     tokens, or .env entered history:
       git ls-files | grep -iE '\.env|secret|apikey|\.pem|credential' ; echo "---"
       git log -p | grep -iE 'sk-|api[_-]?key|ZAI_|OPENAI_API|ANTHROPIC_API|Bearer ' | head
     Expect no real secrets. Provider keys were always read from env, not
     committed; confirm that holds. If anything shows, STOP and scrub before
     Phase 5.

0.3  Optional tidies (your call, none blocking):
     - tex/README-build.md line 57 still lists %TODO-corabo-email as open; it
       is fixed. One-line correction.
     - PAPER-V1.md / PAPER-V2-READABLE.md carry the old provider-terms +
       DOI/tag TODOs; they are superseded drafts. Leave as process history,
       or add "> Superseded by PAPER-V3.md" at the top of each.
     - README.md root has two genuine code TODOs (diversity metric, tier-2
       classifier). Accurate future-work; leave or tidy.
     - Strip internal comments from tex/main.tex (blend note line 31,
       arXiv-categories reminder line 14) for a pristine source, or leave.

---

## PHASE 1 — RESERVE THE DOI (ONLY-YOU; reversible until you publish)

The paper's Section 9 cites a Zenodo DOI. Reserve it now so you can write it
into the paper before submitting, breaking the chicken-and-egg.

1.1  Zenodo: New upload. Fill metadata (title, author Justin Bronder /
     Corabo Inc., CC BY 4.0). Use "Reserve DOI" to mint the DOI string
     without publishing. Copy the reserved DOI (form: 10.5281/zenodo.XXXXXXX).
     Do NOT publish yet; you upload the actual files in Phase 5.

---

## PHASE 2 — FILL THE TWO PLACEHOLDERS (reversible commits)

The GitHub tag URL is deterministic, you can write it before the tag exists:
  https://github.com/Aargau/latent-underground/releases/tag/v1.0-arxiv

2.1  In docs/PAPER-V3.md (Section 9, ~line 305): replace
       [TODO: GitHub tag URL]   -> the tag URL above
       [TODO: Zenodo DOI]       -> the reserved DOI
2.2  In tex/main.tex (Section 9, ~lines 1195 and 1205): same two replacements
     (the TeX shows them as {[}TODO: ...{]}).
2.3  z.ai marking (the RELEASE.md checklist item you added): prepare the
     GLM-5.2/AI-generated + upstream-terms notice text for the Zenodo README
     and for the headers of tmp/hetero_values.jsonl and tmp/p2final.jsonl.
     You apply this to the Zenodo bundle in Phase 5; stage the text now.

(If you want, I can make the 4 placeholder edits mechanically once you paste
me the reserved DOI — same careful multi-file + grep pass as before.)

---

## PHASE 3 — MANIFEST + FINAL CONTENT COMMIT (reversible)

Manifest regenerates LAST, after the Section 9 edits changed the docs.

3.1  python scripts/make_manifest.py         # regenerates MANIFEST.sha256
3.2  sha256sum -c MANIFEST.sha256            # expect all OK now
3.3  git add -A ; git status                 # review: PAPER-V3.md, main.tex,
                                             # MANIFEST.sha256, any tidies
3.4  git commit -m "Flip-day: fill GitHub tag URL + Zenodo DOI in section 9;
     regenerate manifest; final pre-submission state"
3.5  git push

---

## PHASE 4 — FINAL COMPILE + EYEBALL (reversible)

4.1  Compile (one command if tectonic/latexmk installed):
       cd tex && tectonic main.tex          # OR: latexmk -pdf main.tex
4.2  Open tex/main.pdf and confirm on the page:
     - author email bronder@corabo.com (not %TODO)
     - Section 9 shows the real tag URL and DOI (no TODO)
     - the Russinovich self-audit paragraph is present in the reconciliation
       discussion
     - ~21-22 pages, tables render, references list ends at 37 entries
     - zero literal "TODO" visible anywhere in the rendered PDF

---

## PHASE 5 — FLIP + ARCHIVE (ONLY-YOU; IRREVERSIBLE from 5.2 on)

5.1  Final secrets-sweep confirm (repeat 0.2). Last chance before public.
5.2  IRREVERSIBLE (one-way in practice): flip the GitHub repo to PUBLIC
     (Settings -> General -> Danger Zone -> Change visibility).
5.3  Cut the tag on the pushed final commit:
       git tag v1.0-arxiv ; git push origin v1.0-arxiv
     (Now the tag URL in Section 9 resolves.)
5.4  Build the data bundle:
       tar --use-compress-program=zstd -cf logs.tar.zst logs/
     Add the derived-data files (tmp/hetero_values.jsonl, tmp/p2final.jsonl)
     and a copy of MANIFEST.sha256.
5.5  Apply the z.ai marking (Phase 2.3 text) to the Zenodo README and the two
     GLM-derived data files' headers.
5.6  IRREVERSIBLE: upload the bundle to the reserved-DOI Zenodo record and
     PUBLISH. The DOI is now permanent and matches Section 9.

---

## PHASE 6 — SUBMIT TO arXiv (ONLY-YOU; IRREVERSIBLE at 6.6)

6.1  arXiv (logged in as the Corabo-email account that holds endorsement
     JIECGB): Start New Submission.
6.2  Upload the TeX SOURCE package (arXiv prefers source over PDF): main.tex
     + references.bib. Tables are inline, no figure files. Optionally attach
     the two prereg PDFs as ancillary files (convert GATE1/GATE2-PREREG .md
     to PDF first if you want them).
6.3  Let arXiv compile; review the arXiv-generated PDF page by page.
6.4  Primary category cs.AI, cross-list cs.CL. Title and abstract as in the
     paper. License: CC BY 4.0.
6.5  Read the Submittal Agreement (already reviewed; provider-terms warranty
     now backed by docs/PROVIDER-TERMS-REVIEW.md). Accept.
6.6  IRREVERSIBLE (license is perpetual): Submit. Endorsement is live, so it
     proceeds. Note the arXiv ID and the announce time (usually next business
     day, 20:00 ET mailing).

---

## PHASE 7 — POST (after it is live)

7.1  Thank-you to Mihaela (LinkedIn), referencing the Delta days. Warm-channel
     maintenance, no ask.
7.2  Career fan-out per plan: Felix Rieseberg re-ping with the arXiv link;
     Aditi Kumar connect; "since applying, I've published" second-touch on
     both Anthropic ATS entries.
7.3  Bank the submission: arXiv ID, Zenodo DOI, tag, announce date.
7.4  Anything a reviewer or you spot post-hoc folds into v1.1; arXiv revisions
     are free and normal.

---

## DECISIONS TO MAKE ONCE (flagged, not blocking)

- Zenodo: reserve-DOI (this runbook) vs GitHub-Zenodo auto-DOI on release.
  Reserve-DOI is cleaner because it lets the paper cite the DOI pre-publish.
- Ancillary prereg PDFs: attach or not (requires md->PDF conversion).
- Strip internal .tex comments for pristine source: yes/no.
- The two superseded drafts (V1, V2): add "superseded" header or leave as
  process record.
