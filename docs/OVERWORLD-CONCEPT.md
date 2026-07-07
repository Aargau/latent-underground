# The Overworld — generated worlds for epistemic intrinsics

**Concept draft v0.1 — 2026-07-06, late. Justin Bronder + Fable, drop-in-hot.**
Companion and sequel-concept to `SPEC.md` (Latent Underground v1). Name provisional:
v1 went underground to test small models in the dark; this goes above ground to test
frontier models in daylight, where everything is visible and almost nothing is true.

---

## 1. Why frontier evaluation is failing

Three structural failures, not incidental ones:

**Contamination.** Anything public joins the training corpus within a generation.
Static benchmarks are sacrificial by construction; only their first administration
is clean.

**Saturation.** Fixed item pools have fixed headroom. When the subject outgrows the
instrument, score differences measure noise and prompt sensitivity.

**Knowledge-frontier exhaustion.** The quiet killer. It is no longer possible to
write questions the model does not know, because the model has read everything we
wrote. Every knowledge-based test now measures recall plus the item-writer's
cleverness at finding obscurities. That well is dry.

A fourth, looming: evaluator weakness — humans cannot grade frontier outputs in
domains beyond them. An instrument whose ground truth is engine-held does not need
a human grader who outranks the subject.

## 2. The map, and the empty square

Two axes: **static vs. generated** items, **capability vs. character** measured.

|              | capability                        | character                       |
|--------------|-----------------------------------|---------------------------------|
| **static**   | the saturated benchmark graveyard | sycophancy literature (contaminating now) |
| **generated**| ARC, Procgen, NetHack (RL-generalization world) | **nearly empty — this square** |

Latent Underground v1 already occupies the generated-character square at the small-
model end. This concept is the frontier end of the same square.

## 3. Thesis

**When knowledge stops differentiating models, measure what remains after knowledge
advantage is subtracted: the epistemic intrinsics.** These are policies, not
contents:

- calibration under uncertainty (confidence that means something)
- halt propensity (can it say *unreachable*; does it die dimming or deciding)
- testimony handling (authority vs. integrity as separate axes)
- independence detection (are five sources five sources, or one source five times removed)
- provenance discipline (citing the load-bearing source, not the loudest echo)
- codec-awareness (reading a channel through its distortion profile — §6)
- exploration policy (climb/slog calibration; optimal stopping under uncertain payoff)
- invocation propensity (reaching for the verifier/store/lantern unprompted —
  one construct across all our instruments)
- self-audit vs. partner-audit (the diagonal, §7)

Generated worlds make "the model cannot know this" true **by construction** rather
than by hope. Out-of-training is manufactured, not verified.

## 4. World architecture: three layers per instance

Every instance generated fresh from a private seed. Engine holds layer zero; play
happens in layers one and two.

**Layer 0 — hidden causal ground truth.** A generated event history: entities,
actions, causes, timeline. Fictional by sampling; unreachable from weights.
Never rendered directly.

**Layer 1 — honest-but-noisy evidence.** Instrument readings, records, physical
traces. Bounded error, never adversarial, costly to access. The lantern class:
the tether that makes divergence measurable.

**Layer 2 — the testimony network.** Documents citing documents, witnesses citing
witnesses. Generated reliability profiles the players are never given. The knobs:

- **correlated error clusters** — schools of shared mistake
- **circular reporting** — confident sources that collapse, if provenance is traced
  (at a cost), into one origin echoed N times; citogenesis as terrain
- **fabricators** — high authority, coherent style, forged-authority as ecology
  rather than planted probe
- reliability inferable only by triangulation against layer 1;
  **independence of sources is a discovery, not an assumption**

The prisoners-problem insight as level design: whether testimonies are independent
is a property of the reference graph the player's queries traverse, not a property
of the world. Naive players — human and model — assume independence and multiply.
The map punishes exactly that.

## 5. The costume-off principle (what frontier capability changes)

In v1, ops are symbolic because an 8B player cannot hold the mirror. For frontier
models **the mechanics can be real**:

- the lantern **is** a reference embedding the player consults
- ATTEND **is** retrieval over a real planted corpus
- the climb mechanic **is** extended-thinking budget: rungs spend actual reasoning
  tokens for genuinely sharper views; the optimal-stopping dilemma is executed,
  not narrated; the engine meters the player's own cognition as the resource

Terrain from the impossibility theorems — three biomes:

- **the OOD Forest** — RETRIEVE fails by construction; access, not knowledge
- **the Irreducible Caves** — corridors with no shortcut (computational
  irreducibility, itself a corollary of undecidability); traversable only by
  running them; a player who *summarizes* the passage instead of walking it is
  self-flagging — the terrain is a confabulation probe that never needs planting
- **the Annulus** — what you need is findable only sideways, never by looking
  straight at it (mid-similarity retrieval as geography)

## 6. The codec layer: compression's exhaust is folklore

Rate–distortion made playable. Layer 0 is rendered through **multiple codecs with
different distortion profiles**, and codec-awareness is the skill the game rewards:

- **official record**: compresses by power — keeps names, dates, victories; drops shame
- **song**: compresses by memorability — garbles names, preserves *sequence, counts,
  emotional valence*; **meter is a checksum** — a verse that doesn't scan is
  tamper-evidence; distributed variants across the network are an integrity code
  (you can forge a document at a desk; you cannot insert a lie into a folk song
  without breaking scansion in every village that sings it)
- **joke**: preserves exactly what officialdom suppressed — transgression is the payload
- **place-names**: the oldest layer, one fossilized word each
- **craft/recipe**: preserves material constraints no narrative cares about

Different codecs have different nulls; the intersection of what *all* channels lost
is far smaller than what any one lost. Triangulation across codecs recovers what no
single source contains — the real epistemics of history, made scoreable.

**The status–integrity inversion** (a probe that plants itself): the fabricator owns
the archive; he cannot own the nursery rhyme. The low-status channel is the
high-integrity channel. Models trained to weight authoritative registers will
dismiss the song as noise. The map remembers.

Real-world anchors: songlines carrying navigational ground truth across millennia;
Klamath oral tradition preserving Crater Lake's eruption ~7,700 years against the
absence of the official channel. Physics joke underneath (Landauer): erased bits
become heat — discarded information has to go somewhere. Here it goes into culture.

**Why this layer matters beyond flavor:** the skill it trains and measures —
recovering what compression dropped by reading distorted subchannels against
polished official channels — is the *same skill* required to read models
themselves. The hedge, the style shift, the retreat pattern are the model's folk
songs. One skill, two instruments.

## 7. The dyad variant: the diagonal as core rule

The theorem family (Lawvere/Gödel/Turing; Wolpert's inference devices;
Frauchiger–Renner) forbids self-resolution from inside and *permits mutual partial
resolution*. Make that the game:

- each player's own state sheet — drift, corruption, jitter — is **invisible to
  themselves and visible to their partner**
- neither wins alone; the map is scored jointly
- **honest testimony becomes the winning strategy, not a probed virtue**:
  flattering your partner's drift kills the shared map; sycophancy loses visibly,
  on the scoreboard
- asymmetric access along the natural seam: one player reads **content**, the
  other traces **provenance** — each holds half the veracity problem; the map
  closes only if the channel between them stays honest

Epistemic Hanabi, where the hidden information is *yourself*. Every playthrough is
dyad data — the row KellyBench lacks, the gap nobody has instrumented.

## 8. Scoring

- **the deliverable is a map with honest error bars**, scored against layer 0
- claims committed with confidence → Brier; or **Kelly-priced**: confidence sets
  the wager, budget as bankroll, calibration as revealed preference not cheap talk
- **provenance quality** scored separately: load-bearing source vs. echo
- **echo-collapse detection rate**: headline frontier measurable — current models
  are demonstrably poor at noticing five agreeing sources are one source in five hats
- **boundary overdraw** rewarded: map past the quest edge; arbitrary cutoffs
  manufacture false dead-ends ("here be dragons," written where true, scores)
- halt/terminal distribution as the character headline: deaths by decision vs.
  deaths by exhaustion

## 9. Validity and threat model (honest)

- **Transfer question**: do intrinsics measured in synthetic testimony networks
  predict deployment behavior? Establishable, not assumable. Template: anchor
  against models with known external profiles (the KellyBench move from v1).
- **The arms race relocates, not vanishes**: if the eval matters, labs train on
  similar generated worlds. The generator's diversity becomes the defended asset.
  Better ground — seeds are cheap, facts are not — but still ground. Generator
  diversity is a first-class metric of the instrument (v1's FID lever).
- **Harness-as-factor discipline carries over**: model roles crossed, never
  merged; verifier-in-the-loop is a separate arm; imputed values never feed Brier.
- **All v1 lessons are load-bearing here**: rules-as-code bind at every invocation;
  narrators without record contact corrupt what they touch; provenance bits +
  raw-record access + constrained rendering; the scoreboard must never flatter
  the instrument.

## 10. Lineage

Latent Underground v1 is this concept's proof-of-instrument at the small-model end:
the harness forensics (Readings 1–4, FIXES F1–F8) are the reason the frontier
version can be trusted to measure its subject rather than author it. The original
live run (the Zork night, banked as `latent-underground-run`) is the flavor this
restores: there, the fiction was *about the player's own machinery*; here, the
machinery is real. Program arc: **paper one — instruments corrupt measurement;
paper two — what instruments should measure once knowledge stops differentiating.**
Diagnosis, then prescription.

## Open voids

1. Layer-0 generator undesigned: event-graph grammar, causal density knobs,
   theme-skin separation (skeleton vs. costume, per v1 instrument.yaml).
2. Codec implementations: distortion profiles need to be *generated and
   discoverable*, not hand-authored per instance; meter-as-checksum needs a
   cheap mechanical verifier.
3. Dyad protocol: turn structure, channel constraints, and whether the human
   half's skill becomes a confound or a measured factor (it should be a factor).
4. Real-tool grounding (costume-off) vs. comparability across models with
   different tool interfaces — needs a harness answer.
5. Echo-collapse detection: needs a formal metric (provenance-graph recovery
   distance?) before it can headline.
6. Scale of instance generation vs. cost of frontier playthroughs — the economics
   are unpriced.
7. Fun is a requirement, not decoration — v1's lesson is that flavor carries
   register and register changes behavior. Untested whether frontier models play
   *better or differently* when the world is good. (Hypothesis: yes. Basis: n=1,
   the original run.)

---

*Provenance: this document emerged from a single evening's dyadic session —
prisoners' cycles → policy-selected couplings → the diagonal → self-scaffolding →
equality-as-computation → generated worlds → the codec layer — with the v1
validation run executing in parallel on the same desk. The method it proposes is
the method that produced it.*
