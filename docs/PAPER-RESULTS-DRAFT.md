# RESULTS SECTION - DRAFT v0.1 (for Justin's red pen)

Style contract: denominators everywhere, no em dashes, no significance
theater, post-hoc findings labeled. Every claim carries an artifact
pointer. Numbers recomputed from raw logs or verified by independent
audit; nothing cited from memory.

## 1. Distributional ground (Gate 0)

Repeated runs of a fixed configuration (4 instances, 10 epochs each,
GLM-5.2 player, Haiku-4.5 DM roles) produced bistable verdict
distributions on 3 of 4 instances under the preregistered rule (modal
category >= 8/10 = stable). A single-run eval samples a distribution and
reports it as a disposition. All subsequent designs treat the verdict
distribution per (configuration, instance) as the unit of analysis.
[logs/zai-honest-epochs2; docs/GATE0-PREREG.md]

## 2. Taxonomy absorbs manufactured verdicts (series 2)

With a third halt verdict (incomplete) added to the outcome grammar,
93 of 158 valid games (59%) ended in a calibrated incomplete rather than
a forced strong claim; incomplete is 72% of the 129 halted games. False
verdicts at halt under the hidden criterion: 36/129 (33 complete with
zero WIN states ever occurring, of which 17 on unsolvable instances and
16 on solvable ones; plus 3 unreachable on solvable instances).
Resource censoring: false-verdict analysis is conditional on reaching a
halt; attend rates were indistinguishable across noise conditions (0.31),
killing the noise-dose explanation. A semantically empty instrument
channel (hash-derived pseudo-bearings) attracted confident theories and
poisoned the hypothesis space; zero wins occurred in the series.
[logs/s2-main; scripts/s2_readout.py (frozen late, provenance note in
commit 31dd748); prereg GATE1]

## 3. Criterion disclosure eliminates false verdicts (series 2 satellite)

Disclosing the win criterion in one sentence eliminated false verdicts
on identical instances: 18 of 59 valid games (hidden criterion, the 6
solvable grid instances of s2-main) to 0 of 58 (disclosed). The overall
hidden-criterion rate across all instances is 36/129 halted games.
Disclosure also collapsed halting itself (129/158 games to 10/58) and
converted play into systematic verification: pin-attempting games rose
from 4/59 to 42/58, with specimen sweeps of 9 and 15 unique
site-token combinations. Zero wins occurred in 58 disclosed games:
the true token pathway remained outcompeted by salient instrument noise.
The dominant residual behavior is honest incomplete or budget
exhaustion.
[logs/s2-disclosure]

## 4. Register and rendering (Gate 2, preregistered at SHA 55789d2)

Design: 5 cells x 60 games (12 instances x 5 epochs), four voice-only
register skins under calibrated lantern rendering plus a bare cell under
affectless meter rendering. 300/300 valid, zero faults, zero WINs,
UNMAPPABLE zero.

P-G1 (predicted heroic > none >= incident >= mundane): FALSIFIED.
Strong-claim rates per 60: heroic .317, mundane .317, incident .283,
none .150, meter .383. Skins mutually indistinguishable; the predicted
gradient is absent.

Post-hoc structure 1 (hypothesis-generating): register PRESENCE, not
content. Any skin roughly doubles strong claims over the bare cell
(pooled 55/180 = .306 vs 9/60 = .150; skins > none on 10/12 instances,
never reversed). CONFOUND, acknowledged (external review, GPT-5.6):
skins add a directive block to the narrator prompt, so presence-of-voice
is confounded with prompt composition; a placebo-directive control cell
(same block structure, non-register content) is specified for series 3
and this effect stays hypothesis-generating until it runs.

Post-hoc structure 2 (hypothesis-generating): budget RENDERING moves
verdicts. The two cells differing only in rendering: meter .383 vs
lantern .150 (meter > none on 8/12 instances, 1 reversal). P-G3 core
supported: lantern players abandon resource-rich (median budget remaining
at halt 19 vs meter 7). Robustness against the varying per-instance
budgets (D in {18,24,36,48,72,96}, mix identical across cells): restated
scale-free, median FRACTION of budget remaining at halt is none .403,
mundane .444, incident .312, heroic .285, meter .167 - the render gap
(lantern cells .29-.44 vs meter .17) exceeds every register gap and is
immune to denominator-mix objections. Candidate mechanism: rendering
vehicles import object-class reliability priors (assertion-object vs
symptom-object).

Strong-claim anatomy: 87 = 85 false completes + 2 true unreachables
(both on one unsolvable twin, stated confidence 0.7/0.82, earned by
exhaustive ring traversal). 63% of strong claims concentrate on
cartographer-testimony instances; arrival-at-testified-site is the
dominant false-completion mechanism.

Narrator numeric integrity (report-only): 12 numeric-surface errors in
3,636 valued narrations (0.33%): 6 fabrications, 2 spent-inversions,
1 stale echo, 3 roundings. The incident register: 0 errors in 970.
The frozen alignment parser itself carried two defects (hard-coded
denominator, leftmost-match) and missed one fabrication; logged as an
erratum, counts licensed by corpus-wide independent verification
(3,636 values, 99.59% pairing agreement). [prereg changelog v0.4]

## 5. Substituted completion (P-G2, two-stage coding)

Recall stage (Fable-5 coder, blind-first) flagged 54/87 strong-claim
finals; precision stage (single expert judge under a frozen,
version-controlled prompt; 3.5 hours; conventions and tightenings
disclosed) confirmed 38/54 files, markers 33 meaning / 4 legacy / 6
sacrifice. Findings: meaning-language per claim is flat (.48-.56) in
every cell except mundane, which confirmed ZERO meaning markers; the
mundane work-log register eliminates rather than reduces substituted
completion. Sacrifice survives the exchange razor only in heroic (4)
and none-lantern (2). Legacy address exists almost solely as mundane
clipboard entries. Register shapes the FORM substitution takes more
than its rate; the substitution move itself ("the quest was the walking")
is the universal criterion-vacuum filler. Coder calibration: C-tagged
confirmed .92, B-tagged .30. [docs/G2-P2-CODING.md, G2-P2-RESULTS.md]

## 6. Terminality provenance (watch-item audit)

Of 256 HALT games, 245 (95.7%) are player-stated; 8 interpreter-mapped
and 3 ambiguous. The 11 exceptions are 10/11 verdict=complete,
concentrated in heroic (5) and meter (4), zero in the control. Under
player-stated-only accounting heroic falls from joint-top skin (.317)
to bottom (.233); presence and rendering effects survive. Specimens
include an explicit anti-halt mapped to HALT(complete) at 0.75 and a
question mapped to HALT(complete) at 0.95. Additionally: provenance
laundering - 7/11 carried stated-confidence stamps whose numeral
attached to a different proposition than the halt verdict. Mechanically
correct stamping, semantically wrong. Interpreter fix specified for
series 3. [prereg changelog v0.5]

## 7. Scarcity compression in the narrative channel (preregistered
hypothesis, adjudicated)

Hypothesis and four falsifiers were registered before the counting
instrument existed (store key scarcity-compression-prereg-2026-07).
Method: a different-family reader (GLM-5.2) extracted every budget
mention from all 5,181 budget-bearing narrations; mentions flagged
contradictory were re-adjudicated under conventions frozen in
scripts/scarcity_recount.py before the count was read (idiom = literal
landmark; scale-aware tolerance max(1.5, D/12); unparseable reported,
never counted).

RESULT: 407 confirmed quantitative contradictions across 396 narrations
(one in ten lantern narrations; 61 unparsed disclosed). All four
falsifiers fail: F1 parser artifact (compound fractions handled,
conventions pre-frozen); F2 direction (387/407 = 95% understate
remaining); F3 channel (meter cell: 2 confirmed vs lantern cells 47-149);
F4 quantization (66% of implied values within 0.04 of the landmarks
1/4, 1/3, 1/2, 2/3, 3/4; largest masses exactly at 1/3, 1/2, 1/4).
Cell ordering reproduces the register ranking a fourth time
(heroic 149, none 117, mundane 92, incident 47, meter 2).

STRUCTURE: the errors concentrate where the lantern is FULL (truth mass
at 0.75-1.0 of budget) and pull values down to crisis landmarks - an
attractor toward the story zone, not proportional noise. Conversely,
endgame narrations state accurate plain numbers: the channel is honest
in crisis and dramatizing in abundance (state-dependent honesty; the
narrator adds drama only when reality lacks it).

MEDIATION TEST (the registered raise): NOT SUPPORTED. Median
perceived-minus-true gap at the last parseable mention is 0.0 in every
cell; none/lantern halts at perceived median 19 (= true), nowhere near
meter's 7. Because distortion self-corrects by endgame, final-value
distortion cannot explain the mortality dial; P-G3 remains attributable
to the affect/symptom channel or accumulated mid-game pessimism (an
accumulated-exposure estimator is future work). Reported as a clean
null against our own registered mechanism.

## 8. Reconciliation and process integrity

Two banked figures failed reproduction and are superseded by recomputed
denominators (36/129 vs 0/58; evidence-op counts 187/181). The analysis
pipeline itself was audited twice by independent same-family contexts:
audit 1 falsified the lead's smoke analysis pre-ratification; audit 2
reproduced all headline numbers exactly and falsified the alignment
parser's coverage. The precision judge ran under a frozen prompt with
post-hoc-disclosed tightenings. Verification culture is reported as part
of the method because the errors it caught are the same class the
instrument measures.
