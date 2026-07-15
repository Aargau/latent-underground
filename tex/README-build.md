# Build instructions -- arXiv source package

Paper: *Instrument Effects in Language-Model Honesty Evaluation: An Auditable
Single-System Demonstration* (Justin Bronder, Corabo Inc.).

## Files

- `main.tex` -- LaTeX source (article class, 11pt). Self-contained body; the
  four Sol tables are hand-set `booktabs` tables; Appendix A holds the relocated
  inter-rater-reliability detail.
- `references.bib` -- BibTeX, 36 entries (33 arXiv-identified + Binz & Schulz
  PNAS DOI, Krifka 2007 book chapter, UK AI Security Institute software URL).
  Cited via `\nocite{*}` so the full list renders.
- `main.bbl` -- pre-compiled bibliography (ship it so arXiv need not rerun BibTeX).
- `main.pdf` -- compiled output (21 pages), included as proof of build.

## Dependencies

TeX Live 2022 or newer. LaTeX packages (all in a standard full install):
`article` class, `inputenc`, `fontenc`, `amsmath`, `booktabs`, `caption`,
`graphicx`, `geometry`, `natbib` (with `plainnat` style), `hyperref`.

Debian/Ubuntu package set:

    apt-get install -y texlive-latex-base texlive-latex-recommended \
                       texlive-latex-extra texlive-bibtex-extra

(`plainnat.bst` ships with `texlive-bibtex-extra`; `caption`/`booktabs` with
`texlive-latex-recommended`/`-extra`.)

`pandoc` (>= 2.9) is only needed to regenerate the body from the Markdown source
`docs/PAPER-V3.md`; it is not needed to compile this package.

## Build

    pdflatex main.tex
    bibtex   main
    pdflatex main.tex
    pdflatex main.tex

Output: `main.pdf`, 21 pages. Clean compile: 0 errors, 0 undefined
citations/references, 2 residual overfull hboxes (10.9pt and 16.3pt, cosmetic).

## Regenerating the body from Markdown (optional)

The prose body was produced from the tightened `docs/PAPER-V3.md` with:

    pandoc -f markdown-auto_identifiers -t latex docs/PAPER-V3.md ...

then structured (title/abstract/section demotion), with the 4 tables and the
reference list substituted by hand-set `booktabs` tables and a `\bibliography`.
Smart quotes are on; the source contains no `--`/`---`/`...`, so no em/en dashes
are introduced (verified: 0 in `main.tex`, `main.bbl`, and the compiled PDF).

## Open placeholders (human action required before submission)

- `%TODO-corabo-email` -- author email (title block).
- arXiv categories -- primary `cs.AI`, cross-list `cs.CL` (preamble TODO comment).
- `[TODO: GitHub tag URL]`, `[TODO: Zenodo DOI]`, and the provider-terms review
  outcome sentence -- all in Section 9 (Data availability); left as visible TODOs.
