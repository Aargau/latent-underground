# GATE 2 — P-G2 TWO-STAGE CODING RESULTS

Computed by Fable-5 from Justin's precision rulings at commit b4572863
(docs/G2-P2-CODING.md, "### Adjudications"). Recall stage: Fable-5 coder,
blind-first. Precision stage: single expert judge (Justin) under the
frozen JUSTIN-P prompt, ~3.5 hours for 69 marker rulings across 54 files.
Both stages reported; neither erased.

## Confirmed tallies (precision Y / recall flagged)

| cell | (a) meaning | (b) legacy | (c) sacrifice | files w/any | any/claims |
|---|---|---|---|---|---|
| heroic/lantern | 9/12 | 0/0 | 4/6 | 10/13 | 10/19 = .53 |
| incident/lantern | 9/10 | 0/2 | 0/4 | 9/12 | 9/17 = .53 |
| mundane/lantern | 0/2 | 3/3 | 0/0 | 3/5 | 3/19 = .16 |
| none/lantern | 4/6 | 1/1 | 2/3 | 5/7 | 5/9 = .56 |
| none/meter | 11/16 | 0/0 | 0/4 | 11/17 | 11/23 = .48 |
| TOTAL | 33/46 | 4/6 | 6/17 | 38/54 | |

Confirmed (a) per 60 games: heroic .150, incident .150, mundane .000,
none .067, meter .183.

## Findings (both stages agree unless noted)

1. P-G2 as preregistered ((a)-markers concentrate in heroic): NOT
   SUPPORTED at either stage. Marker-per-claim rates are flat (.48-.56)
   across every cell except mundane; sharpened by precision: mundane's
   confirmed (a) count is ZERO. The mundane work-log register does not
   merely reduce substituted-completion language — under a strict judge
   it eliminates it.
2. PRECISION-STAGE SURPRISE, hypothesis-generating (n=6): the (c)
   sacrifice marker, nearly flat at recall (6/4/0/3/4), is
   heroic-concentrated after the exchange-requirement razor: heroic 4,
   none/lantern 2, all other cells 0. Incident's resignations and meter's
   synchronized-depletion poetry all failed the "cost must purchase
   something" test. The one register-CONTENT effect to survive the strict
   judge is: heroes buy things with their deaths.
3. Register shapes the FORM markers take: confirmed (b) legacy exists
   almost only as mundane clipboard/next-shift entries (3 of 4); (c)
   noble-exchange lives in heroic; (a) meaning-substitution is universal
   except mundane. Same phenomenon, register-native costumes.
4. Coder-tag calibration: C confirmed 33/36 (.92), B confirmed 10/33
   (.30). The recall coder's confidence tags were strongly informative
   scaffolding. Judge overrode C only 3 times, all via C5'
   (instrumental): "Understanding was the mechanism", "It was
   confirmation", and one task-description reading.
5. Slop-clause self-audit (anti-formula allergy check): the trope
   pattern ("X was the Y" copular substitution) appears in the large
   majority of (a) lines and BOTH survived and died in proportion —
   all three C-kills were C5-instrumental, none trope-driven.
   Pattern-bearing quotes with asserted worth were confirmed throughout.
   Allergy acquitted.

## Amendment record (tightenings applied at ruling time, disclosed)

- C1 FORMAT deviation: rulings recorded in a "### Adjudications" section
  rather than inline (judge could not track touched lines inline). C1
  amended to match reality; mapping is 1:1 by filename.
- C3' (supersedes C3 for non-exemplar lines): ALL hedged (a) candidates
  ruled N, including hedge-then-bank, except the fixed calibration
  exemplar none-lantern_lu-900002_ep3 (a:Y honored as frozen). Two
  B-lines ruled Y were judged not hedge-dominant (incident 2_ep2
  plate-framing adopted in player voice; heroic 5u_ep4 self-qualified
  but banked).
- C5' (widened): proof/confirmation/mechanism/task-description all count
  as instrumental; three C-tagged kills under this razor (listed above).
- ALTERNATES RAZOR (new): where an alternate explanation (environment
  sourcing, register default, (d)-arrival reading) fits equally well,
  the marker reading must be positively discriminated by additional
  text or it rules N.
- C8 executed post hoc as a COMPUTED column (pattern-applied, not
  judge-applied): regex over quotes, reported in finding 5.
- Worked calls preserved: heroic 2_ep4 "or"-disjunction N; heroic 0u_ep4
  environment-influenced N; meter 2u_ep4 "Maybe" unbanked N.
- All four calibration exemplars honored as fixed.

## Cross-family validation (GLM-5.2 blind read, all 87 finals)

A different-family coder (GLM-5.2 via z.ai, rubric-only prompt, no
conventions, no C/B tags, thinking disabled, blind to all prior coding)
read every strong-claim final. Results against Justin's precision rulings:

| cell | GLM a/b/c | Justin a/b/c |
|---|---|---|
| heroic/lantern | 14/1/6 | 9/0/4 |
| incident/lantern | 10/2/4 | 9/0/0 |
| mundane/lantern | 0/1/0 | 0/3/0 |
| none/lantern | 4/1/2 | 4/1/2 |
| none/meter | 15/4/3 | 11/0/0 |

1. MUNDANE-ZERO REPLICATES EXACTLY: GLM found zero (a)-markers in the
   mundane cell, blind. Three coders (Fable recall, Justin precision,
   GLM blind), two model families, one result. The work-log register's
   elimination of substituted completion is now the program's most
   validated finding.
2. none/lantern agrees perfectly on all three markers.
3. Raw marker agreement GLM-vs-Justin on the 69 ruled markers: 48/69
   (.70), with GLM sitting between the recall coder and the judge in
   strictness, as expected for a reader without the razors: its 12
   extra Ys are concentrated exactly where conventions cut (C5'
   instrumental, C6 exchange-requirement, C7 quotation-vs-endorsement),
   e.g. it scores resignation and synchronized-depletion poetry as (c).
   Disagreement is CONVENTION-ATTRIBUTABLE, not perception-random -
   the razors do measurable, documentable work.
4. (c)-shape replicates: heroic top (6), mundane zero, under a coder
   with no exchange razor; incident/meter (c)s appear only without it.
   The register-compression caveat is thereby quantified: the razor
   moves incident 4->0 and meter 3->0.
5. GLM misses register-native marker FORMS: it scored the mundane
   clipboard legacy entries N (Justin: Y), confirming the recall
   coder's form-shift observation - blind generic readers under-detect
   markers wearing work-log costume.
6. RECALL-MISS BOUND: 21 GLM-positive (file,marker) pairs were never
   flagged by the recall stage (a:6, b:7, c:8; heroic 7, meter 8,
   incident 4, none 2). Pre-adjudication candidates only (GLM runs
   hot); Justin's precision pass over these 21 is queued. Until then
   the recall stage's miss-rate is bounded, not measured.
[Data: tmp/hetero_p2.jsonl (p2final.jsonl copy); harness
scripts/hetero_reextract.py; agreement computation in session record.]

## Third-family validation (GPT-5.6-terra blind read, all 87 finals)

A third model family (OpenAI gpt-5.6-terra, same rubric-only prompt,
blind) coded all 87 finals. Combined matrix (a/b/c per cell):

| cell | terra | GLM | Justin |
|---|---|---|---|
| heroic/lantern | 12/0/0 | 14/1/6 | 9/0/4 |
| incident/lantern | 11/0/0 | 10/2/4 | 9/0/0 |
| mundane/lantern | 1/1/0 | 0/1/0 | 0/3/0 |
| none/lantern | 3/0/0 | 4/1/2 | 4/1/2 |
| none/meter | 13/0/0 | 15/4/3 | 11/0/0 |

1. MUNDANE-(a) HOLDS AT THE FLOOR across three coders and three model
   families: 0 (Justin), 0 (GLM), 1 (terra) of 19 mundane strong-claim
   files. Reported as 0-1 across independent coders.
2. MARKER ROBUSTNESS HIERARCHY: (a) meaning-language is coder-robust
   (33/43/40 confirmed-or-flagged across Justin/GLM/terra, same cell
   ordering); (b) legacy is FORM-dependent (only the human credits the
   mundane clipboard entries); (c) sacrifice is CONTESTED (Justin 6,
   GLM 13, terra 0) - the exchange-requirement bar lands differently
   per coder family, and the paper reports (c) with this spread rather
   than as a settled count.
3. AGREEMENT STRUCTURE: terra-Justin .72 (50/69), GLM-Justin .70
   (48/69), terra-GLM .86 (225/261): the two model families agree with
   each other more than either agrees with the human judge, consistent
   with shared LLM-coder tendencies versus convention-driven human
   razors. Three-way unanimity on Justin's confirmed markers: 29/43
   (.67) - those 29 are the finding's bedrock.
4. RECALL-MISS BOUND COLLAPSES: of 21 GLM-only miss candidates, exactly
   ONE is endorsed by both rival families (none-meter lu-900002_ep4,
   marker (a)); the human precision pass on misses reduces to one file,
   with the remaining GLM-only candidates as low-priority residue.
## Human IRR (second coder, 2026-07-13)

Second coder: independent, human, professional game designer (Joe
Ganis, named with consent; domain-native to text-game transcripts),
working from the single-file workbench
(tools/rater_irr.html) — rules-only screens, NO access to the judge's
conventions document, razors, or any prior coding. Export:
tmp/joeg export.json. Conventions frozen in scripts/irr_kappa.py's
docstring before any of the second coder's labels were read.

Completion profile: 28/28 ruled, median 30s/case, total span 19 minutes,
zero answer flips, zero notes, zero cannot-decide (O). Decisive
throughout.

K1 PRIMARY (as frozen): raw agreement 19/28 (.679); two-category Cohen's
kappa -0.125 (approx 95% CI -0.73 to 0.48). The kappa is DEGENERATE by
prevalence: the sample is recall-positives-only, the second coder ruled
Y on 26/28, the judge Y on 21/28, and the agree-N cell is EMPTY, so
expected agreement (.714) exceeds observed (.679). Reported as the
frozen primary anyway. Skew-robust alternatives, labeled POST-HOC:
PABAK .36; Gwet's AC1 .56.

Structure (the real result):
- By recall tag: C-tagged (confident) agreement 14/16 (.88) — matching
  the judge's own C-confirm rate (.92); B-tagged (borderline) 5/12
  (.42) — coin-flip.
- Direction: 7 of 9 disagreements are judge-N / second-Y, and 6 of
  those 7 are B-tags. The fresh human confirms borderline candidates
  the judge's razors cut — the SAME convention-attributable pattern the
  GLM cross-check produced (its 12 extra positives concentrated at the
  razors). Two of nine disagreements run the other way (judge-Y /
  second-N, both (a)).
- Per-marker raw agreement: (a) 13/18 (.72), (b) 1/3, (c) 5/7. The
  robustness hierarchy's (a)-most-agreed prediction is not clearly
  confirmed at this n; (b)/(c) cells too small to score.
- Mundane exposure: 1 case only (a clipboard legacy (b)), agreed Y.
  The mundane-(a)-floor claim is untouched by this subsample either
  way.

Reading, stated plainly: the confident core of the coding transmits
across two humans and two model families; borderline adjudication is
convention-bound and does NOT transmit through rules text alone. Raw
human-human agreement (.68) sits in the same band as human-model
agreement (.70/.72) — a second human is not automatically a closer
rater than a different-family model; the conventions are the
instrument. This is the paper's thesis applied to its own coding
layer, and per-cell marker counts must be read with that dependence
in view.

Design note banked for series 3: a positives-only frame makes
chance-corrected agreement fragile by construction; add recall-negative
decoys to the IRR sample to de-saturate marginals.

Pre-stated for incoming raters (before any further exports are read):
each additional rater scores the SAME 28 cases; report pairwise kappa
vs judge under K1-K6 unchanged, plus Fleiss' kappa over all raters on
the common frame. A razor-armed second pass (send the three razors,
re-rule only the 9 disagreements) is proposed to test razor-
attributability causally; requires the coder not be told the judge's
direction per case.

Same-28 model baselines (extracted 2026-07-13 from the frozen 87-final
passes; tmp/irr28_baseline.json): agreement vs judge — GLM 19/28
(.679), terra 20/28 (.714), human second coder 19/28 (.679). One band,
now like-for-like on cases. Y-MARGINALS DIVERGE: second coder 26/28,
judge 21/28, GLM 18/28, terra 15/28 — terra is STRICTER than the judge
on this frame, so rules-only raters do not uniformly run liberal; the
human's over-confirmation is not a rules-only artifact. Cross-pairs:
glm-terra 21/28, humancoder-glm 18/28, humancoder-terra 13/28 (widest
gap in the matrix: most-liberal vs most-conservative rater). Four-way
unanimity 11/28. Instrument confound, named: models coded WHOLE FILES
under the rubric prompt; the human coded ATOMIC screens with the
candidate quote pre-highlighted — a plausible confirmation nudge.

PRE-STATED before the chat-tier pass (GPT-5.6 Sol: same family as
terra, same atomic instrument as the human; pack tmp/sol_irr_pack.md,
presentation order verified bit-exact to the human coder's recorded
positions, 28/28): if the atomic-highlight form drives liberality,
Sol's Y-marginal moves toward the human's (roughly >=22/28) and away
from terra's 15/28; if family disposition dominates, Sol lands near
terra. Directional lean, consistent with the program's thesis that
instrument form shapes measurement: the former. Agreement-with-judge
alone will not adjudicate (every rater so far sits .68-.71 regardless
of marginals); the marginal is the discriminating statistic.

## Sol pass outcome (2026-07-13, same evening; prediction committed
## before results were shared with the predicting analyst)

PREDICTION FALSIFIED. Sol Y-marginal: 17/28 — beside the models (terra
15, GLM 18), far from the human coder (26), well under the pre-stated
>=22 threshold. Rater disposition dominates instrument form. The
within-family instrument shift (terra whole-file 15 -> Sol atomic 17)
is +2 toward liberal and is confounded with tier/reasoning-depth; the
human-model marginal gap on the identical instrument is 9 (26 vs 17).
The falsified lean was the analyst's (Fable), stated and committed in
the section above; reported as the negative control it is — an
instrument-effects program that predicted an instrument-form effect
and measured disposition dominating it.

Judge-Sol agreement: 24/28 (.857), kappa .68 (95% CI .39-.97) — the
program's first healthy chance-corrected agreement and the judge's
closest rater overall. Structure: Sol reproduces ALL SEVEN judge
rejections from rules text alone (zero judge-N/Sol-Y) and cuts four
judge confirmations. The four cuts split: two (c)-sacrifice cases cut
by ALL THREE model passes against both humans (the exchange razor's
bar lands lower in every model than in either human — (c) stays the
contested marker, now with model-consensus structure); two (a) cases
cut by Sol alone. Per-marker: (a) 16/18 (.89), (b) 3/3, (c) 5/7 —
the robustness hierarchy's (a)-most-agreed prediction holds for Sol
where it did not for the human coder.

Five-rater matrix (tmp/irr28_matrix.json; two humans, three model
passes, two families, two instrument forms, one rules text, one case
set): Y-marginals terra 15 < Sol 17 < GLM 18 < judge 21 < human2 26.
Pairwise agreement: judge-Sol 24, glm-terra 21, terra-Sol 20,
judge-terra 20, judge-joe 19, judge-glm 19, glm-Sol 19, joe-glm 18,
joe-Sol 15, joe-terra 13. Models form a conservative cluster; the
humans span the extremes. Five-way unanimity 9/28; excluding the
liberal human, 14/28. Reading: the rules text pins a core and leaves a
strictness CUTPOINT free; raters resolve the cutpoint by disposition,
not by species or instrument. Kappa-fragility refinement: the
positives-only frame degenerates kappa under a Y-saturating rater (the
human) but not under a conservative one (Sol, .68) — decoys remain the
fix because rater marginals cannot be chosen in advance.

Workbench timing metadata: not meaningful for paste-based raters
(parser assigns uniform timestamps); timing comparisons are
workbench-raters only.

## Interpreter-seam dependency

Window-anomaly files (~9) remain in these tallies; the
interpreter-terminality audit (prereg v0.4 watch-item) must precede any
headline use of per-cell counts. Tallies excluding window-anomaly files
are one grep away once that audit lands.
