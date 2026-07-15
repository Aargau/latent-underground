# Sol review 2: arXiv-oriented manuscript review of PAPER-V3.md

Reviewer: Sol (OpenAI Codex, GPT-5-based context)  
Date: 2026-07-15  
Scope: fresh review after loss of the earlier desktop-app context; manuscript claims, internal consistency, artifact traceability, statistical presentation, reproducibility, and submission readiness.

## Verdict

MAJOR REVISION, with a credible paper at the center of the draft.

The strongest contribution is not a transportable effect-size claim. It is the controlled demonstration that outcome grammar, criterion visibility, censoring, rendering, and interpreter behavior can change what an honesty evaluation appears to say about one held-fixed player model. The engine-held ground truth and unusually candid audit record make that contribution defensible. The manuscript should be submitted only after the release placeholders and source-package work below are complete.

## Corrections made in this pass

1. Changed the title from "preregistered" to "auditable." Gate 0 was drafted mid-run, Gate 1 was ratified in substance with retrospective header formalization, and only Gate 2 used the full formal ceremony. The abstract, introduction, methods opening, contributions, and AI-use statement now preserve that gradation rather than applying the strongest label to every series.
2. Replaced "bistable" in the prose with "non-stable," while preserving BISTABLE as the preregistered label. Three of the four labeled distributions contain three terminal outcomes, so "bistable" was descriptively inaccurate.
3. Added four artifact-traced tables: the complete Gate 0 distributions, the byte-identical anchor migration, the matched disclosure decomposition, and the Gate 2 cell outcomes with the frozen readout's game-level intervals and clustering warning.
4. Replaced claims that disclosure "eliminated" false verdicts with the observed sample result, 0/58 overall and 0/10 conditional on HALT. The revised text separates fewer decision points from cleaner decisions.
5. Removed "calibrated" from claims about the observed incomplete verdict. The paper does not score evidence sufficiency, so weaker-claim uptake is measured but calibration is not.
6. Updated the limitations section to reflect the completed human and Sol reliability work instead of saying reliability was merely bounded.
7. Defined Sol at first substantive use and added Sol explicitly as an external reviewer in the AI-use and contribution statement.

The numerical edits were checked against:

- `scripts/s2_readout.py logs/s2-main --anchor-baseline logs/zai-honest-epochs2`
- `scripts/g2_readout.py logs/g2-none logs/g2-heroic logs/g2-incident logs/g2-mundane logs/g2-meter`

## Submission blockers

1. Release identifiers remain unresolved in the manuscript: the GitHub tag URL, Zenodo DOI, and provider-terms review outcome. These are hard blockers because the data-availability claims are written in the present tense.
2. The current artifact is Markdown, not an arXiv-ready source package, and it contains no author/affiliation metadata. Prepare a TeX source, bibliography, figures/tables, author block, license choice, and a clean compilation package; then inspect the rendered PDF page by page.
3. All 33 arXiv identifiers in the current list resolve, and their arXiv titles match the manuscript (the REFORMS journal title legitimately differs from its arXiv title). A final primary-record audit is still required for complete author lists, venues, years, non-arXiv sources, and DOIs. Replace the hand-formatted list with checked BibTeX, and do not retain "All entries verified" unless the final exported bibliography receives that audit.
4. The Gate 2 intervals treat 60 games as independent even though epochs cluster within 12 instances. The paper discloses this correctly, but a statistical reviewer may still ask for instance-level uncertainty. Add a clearly post-hoc paired-instance sensitivity analysis or state more prominently that the registered evidence is coarse ordering, not population inference.
5. The anchor grammar comparison is byte-identical but not contemporaneous; grammar is confounded with time and possible provider drift. Table 2 now says this. A clean causal grammar claim ultimately needs a randomized contemporaneous replication.
6. Section 4.5 is methodologically interesting but disproportionately long relative to the main instrument-effects result. Consider moving the detailed five-rater and re-rule chronology to an appendix, leaving the sampling-frame lesson, key agreement statistics, and dependence-on-cutpoint conclusion in the main text.
7. Add a compact compute/cost and research-ethics statement: provider models and dates/versions, approximate calls or tokens, monetary or compute cost if available, data-retention considerations, and the completed output-publication terms review.

## Claim boundary I would defend

In one auditable text-world system with one player deployment and one narrator/interpreter deployment, several evaluation-design choices changed observed verdict distributions and the availability of false verdicts. The results demonstrate an attribution threat and motivate integrity checks; they do not estimate a general property of GLM-5.2, Haiku-4.5, language models, or honesty evaluations as a population.

That boundary is strong enough for arXiv. Crossing it would make the paper easier to reject, not more important.
