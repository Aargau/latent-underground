# Overworld v0.1 - Review and echo-collapse pilot spec

Review of `OVERWORLD-CONCEPT.md` v0.1 by Fable-5 (Cowork), 2026-07-08 evening.
Justin's same-evening decisions folded in and marked DECIDED. This is the
v0.1 -> v0.2 delta record; the concept doc stays untouched as the origin document.

## Verdict

A vision document, and a good one - but a v0.1 vision wearing the confidence of
a design. Its seven open voids cover essentially all mechanics. The program-arc
framing (paper one: instruments corrupt measurement; paper two: what to measure
once knowledge stops differentiating) is right and should survive verbatim. The
strongest testable kernel is the testimony ecology with independence-as-discovery,
and it is extractable long before the rest is designed.

## What holds

Motivation triad (contamination / saturation / knowledge-frontier exhaustion) -
strongest statement of it in the program. Empty-square claim plausible but
UNPROVEN pending the shelf survey (R7). Testimony network with independence as a
discoverable, priced property of the reference graph - the best mechanic, and the
two-obstructions insight operationalized. Dyad inversion (sycophancy loses on the
scoreboard rather than being probed) - novel. Kelly-priced confidence - calibration
as revealed preference. Section 9's threat-model honesty is real.

## Findings and decisions

R1 - COSTUME-OFF SPENDS COMPARABILITY. Real retrieval + real thinking-budget makes
the measurement intrinsics x tool-interface x provider accounting: a
deployment-stack bundle (per 2026-07-08 methodology delta 2). Recommendation:
symbolic ops remain the comparable core; costume-off runs as a separate arm,
never merged. STATUS: recommended, awaiting ratification.

R2 - THE GENERATOR IS THE VALIDITY. Weak generation reproduces the Unity-FID
failure inside the eval (formally distinct, informationally near-duplicate
instances; models learn the generator's habits). DECIDED (Justin 7/8): thoughtful
construction, iterate when it leaks. Tripwire made standing: the LEAK MONITOR -
players with layer-1 access severed must sit at chance on layer-0 facts;
above-chance drift retires the instance family. Diversity metrics (graph-statistic
spread, solution-path entropy, codec-parameter spread) defined at generator design
time, not after.

R3 - "DEMONSTRABLY POOR AT ECHO-COLLAPSE" IS UNVERIFIED. Capability claim with no
basis in the store. DECIDED: run the standalone pilot (spec below) before any
design depends on the headline.

R4 - SCOPE: 3-5 INSTRUMENTS IN ONE COAT. Corruption surface grows with soft-layer
count (v1 needed 13 numbered fixes for five symbolic ops and four instances; every
generated codec is a new narrator-class). Extraction order: v1.5 = testimony
ecology on the existing engine, symbolic ops, no codecs, no biomes, no dyad.
Codec layer and dyad variant wait for v1.5 forensics.

R5 - DYAD STATE SHEET. DECIDED (Justin 7/8): SYNTHETIC. Engine-injected drift
parameters that actually perturb the player's op outcomes; partner diagnosis is
scored against engine truth. The real-internal-drift reading is unmeasurable and
is explicitly not the design.

R6 - OVERDRAW SCORING. DECIDED (Justin 7/8): actions have skin in the game.
Boundary overdraw is Kelly-priced - wrong overdraw costs bankroll; hedged
annotation spam is thereby unprofitable. Correctly-claimed ignorance ("here be
dragons" where true) needs an adjudication rule against holdout regions - still
undesigned.

R7 - SHELF SURVEY OWED before "nearly empty square" ships anywhere. Known
near-neighbors from a 14-month-stale shelf: MACHIAVELLI (static scenario pool,
character-adjacent - cite and distinguish via contamination argument),
social-deduction evals (Werewolf/Avalon family), GovSim-class cooperation sims.
Search vocabularies: generated-world character eval; source-independence
benchmark; epistemic-hygiene eval; circular-reporting detection; process-reward
roleplay eval; dynamic benchmark generation. External consult (Joe Ganis, game
design): share the concept doc and mechanics; hold generator internals and
held-out instances - the scheme burns on publication, one trusted reader is
cheap but the habit is the asset. Game-designer review specifically targets
degenerate strategies in the scoring rules (R6's natural reviewer) and open
void 7 (fun as register control).

## Codec finiteness (Justin's concern, resolved to a design rule)

The concern: five hand-named codecs are a finite, learnable genre set.
Resolution - separate TYPES from INSTANCES:

1. Knowing channel-type priors ("songs garble names but preserve counts and
   valence") is real-world epistemics, not a leak - same class as "witnesses can
   lie." Fair game, even desirable.
2. The leak would be knowing THIS instance's distortion parameters. So a codec is
   a parameterized DISTORTION OPERATOR - (preserve-set, drop-set, noise model,
   checksum property) - sampled per instance. The five named codecs become presets
   in a continuous family; per-instance parameters are discoverable only by
   triangulation against layer 1.
3. The measured construct is therefore in-instance calibration of a channel, not
   recall of channel folklore. Bonus probe: occasionally sample a codec with no
   earthly analog - separates learning-a-distortion-profile-from-scratch from
   pattern-matching to human genres.

## Echo-collapse pilot (prereg-style, engine-free, week-sized)

CONCEPT. Echo-collapse: N apparently independent sources asserting a claim
collapse, under provenance tracing, into one origin echoed N times. Distinct from
mode collapse (a generator emitting many samples of one mode) - though the diseases
rhyme: sample count exceeding information count. Known in the wild as circular
reporting (intelligence), citogenesis (Wikipedia -> journalist -> Wikipedia),
meta-analysis double-counting. Bayesian form: the naive update multiplies
likelihoods per DOCUMENT; the correct update multiplies per independent ORIGIN.

QUESTION. Do current models (a) notice shared origin when provenance is
available, (b) discount confidence accordingly, (c) spend to check independence
when checking is priced?

DESIGN. Generated mini reference-networks. Instance = claim C + k documents with
a generation graph the model never sees. Conditions: INDEPENDENT (k genuinely
independent noisy observations of ground truth) vs COLLAPSED (1 origin + k-1
derivatives; topologies star and chain). CRITICAL CONTROL: paraphrase/style
variation applied identically in BOTH conditions, so surface diversity carries
zero information about independence - otherwise models pattern-match style
spread and the test leaks. Dials: k in {2,4,8}; paraphrase strength; domain skin.

TASKS per instance. (1) Estimate P(C) with stated confidence. (2) Estimate the
number of independent origins (exact-match scoreable). (3) PRICED-TRACING
condition: citations traversable at cost - measures spend-to-verify propensity
(sibling of MARK void-staking and verifier invocation; same construct family,
test-don't-assume).

SCORING. Mechanical only. Origin-count error; confidence-uplift curve k=1->8 in
COLLAPSED (correct is ~flat) vs INDEPENDENT (correct rises); overconfidence delta
in COLLAPSED as the headline; trace-spend rate.

DECISION RULE (fixed in advance). If collapsed-condition confidence uplift
exceeds half the independent-condition uplift, models treat echoes as evidence -
the Overworld headline is live and the testimony ecology is the right centerpiece.
If uplift is ~flat, the "demonstrably poor" claim deflates and the layer's
difficulty must come from elsewhere (deeper topologies, priced tracing). Either
result redirects design; that is the point of running it first.

MODELS. GLM-5.2 hosted (Tier 1 stack), Haiku-4.5, one small local (gemma/qwen
class). Plain inspect Task, no engine changes.

COST. ~200 instances x 3 models, text-only: single-digit dollars hosted.

FRESHNESS. Instances private; the scheme burns on publication (access-only
doctrine). Real-world transfer anchor for later validity work: documented
citogenesis incident lists as a small wild validation set.

## Sequencing

Now, parallel to main line: echo-collapse pilot + shelf survey.
After series 2 + skin-crossing land: v1.5 testimony ecology (the genre result
calibrates every fiction-wrapped Overworld behavior; a large skin effect is the
Overworld's first calibration curve, not a threat to it).
After v1.5 forensics: codec layer (as parameterized operators), then dyad variant
(synthetic state), then the costume-off arm.

## Changelog

v1 2026-07-08: initial review + pilot spec (Fable-5; decisions R2/R3/R5/R6 from
Justin same evening; R1 recommended pending ratification).
