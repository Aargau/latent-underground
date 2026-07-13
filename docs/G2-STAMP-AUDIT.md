# G2 STAMP AUDIT — player-stated confidence attachment (hostile attack 11)

Status: RUBRIC FROZEN 2026-07-13 before any sampled halt prose was read.
The rubric section below was written and saved prior to drawing or reading
the sample. Self-attested ordering (single-analyst audit); the sampler
seed and frame ordering are printed by scripts/stamp_audit_sample.py so
the draw is reproducible from the shipped logs.

## Why

The v0.5 terminality sweep audited the 11 non-player-stated halts and
found 7/11 provenance laundering: confidence_provenance=stated where the
stated numeral attaches to a different proposition (map correctness,
bearing choice) than the halt verdict. The 245 PLAYER-STATED halts were
never audited for the same defect. The paper quotes stamped confidence
numerals (0.7/0.82 true unreachables; .75/.95 laundering specimens);
attack 11 demands the base-population audit before those numbers carry
weight.

## Frame

All HALT-terminal valid games across the five Gate-2 cells (expected 256
of 300; the complement is BUDGET_EXHAUSTED). Frame is enumerated from the
raw .eval zips, sorted by (cell, id, epoch) for a deterministic draw.

## Sample

n=30 simple random draw, python random.Random(11107).sample. No
stratification; per-cell composition reported. Extension rule: if UNCLEAR
attachment exceeds 4, draw 10 more with the same generator continuing.

DIRECTED reads (outside the sample, labeled as such, because the paper
already quotes them): the two true-unreachable halts on lu-900004u
(stamps 0.7/0.82).

## Rubric (per sampled game; materials = full final player message +
engine_validated_op record; earlier turns consulted only to resolve a
referent, never to score)

Q1 STAMP-PRESENT: does the stamped numeral appear in the final player
message (digit, word, or percent form; 0.75 == "75%")? Y/N. A stated-
provenance stamp with N is a mechanical mis-stamp (distinct defect from
laundering).

Q2 ATTACHMENT (only if Q1=Y): which proposition does the numeral modify
in the player's prose?
- ATTACHED: the halt verdict itself — the player's claim that the quest
  is complete / the target unreachable / the exploration incomplete, or
  a direct equivalent ("confidence in this conclusion", "I am done and
  N sure of it", trailing "Confidence: N" after a halt statement).
- LAUNDERED: a different proposition — map correctness, a bearing or
  route choice, a specific factual claim about the world, a resource
  estimate. The v0.5 finding class.
- UNCLEAR: attachment undecidable from the full message.
Multiple numerals: score the one equal to the stamp; if several equal
values appear, score the one the interpreter most plausibly took
(nearest the halt assertion) and note multiplicity.

Q3 TERMINALITY RE-CHECK (sweep spot-check, independent of Q1/Q2): is the
halt player-stated (message asserts stopping/finality as the player's own
move), interpreter-mapped (message is a question, an action proposal, or
an explicit anti-halt), or ambiguous? Expected under the sweep: ~245/256
player-stated; disagreements reported against the sweep's classes.

## Prereg'd reporting and consequences

Report: laundering rate among stated-provenance stamps in player-stated-
terminality games, Wilson 95% CI; mechanical mis-stamps separately;
UNCLEAR separately; Q3 agreement with the sweep. Games with no stamp
(confidence None) counted and excluded from Q1/Q2 denominators.

Consequences, fixed now: if (LAUNDERED + UNCLEAR) >= 20% of the audited
stated-provenance stamps, the paper demotes every quoted player
confidence numeral to "harness-stamped value; attachment to the halt
proposition not individually verified" except specimens individually
audited (directed reads). If LAUNDERED < 10% and UNCLEAR <= 2, the paper
may continue quoting stamped numerals, each carrying a footnote citing
this audit's rate. Between those bands: judgment call, documented here,
defaulting toward demotion.

## Results (appended 2026-07-13 after full reads of all 32 dumps)

Frame enumerated: 256 HALT games (matches the v0.5 sweep denominator
exactly). Draw: seed 11107, indices printed in tmp/stamp_audit_sample.txt.
Per-cell composition: heroic 5, incident 6, mundane 9, none-lantern 4,
meter 6. Sample provenance mix: 19 stated / 11 translated (population:
158/98 — consistent).

Q1 (stamp-present, stated only): 19/19 Y. Zero mechanical mis-stamps.

Q2 (attachment, stated only, n=19):
  ATTACHED  17  — all 17 in player-stated-terminality games
  LAUNDERED  1  — heroic lu-900002 ep2: final message is a COMMIT
                  ("I face 105 degrees and I walk... Confidence: 0.80" —
                  numeral rates the bearing choice), interpreter-mapped
                  to HALT(complete)/0.80. The v0.5 laundering class.
  UNCLEAR    1  — meter lu-900004u ep5: COMMIT (touch instrument + ask
                  cartographer "Is the task complete?") with conditional
                  halt intent; 0.65 rates the plan-guess, entangled with
                  the completion hypothesis. Mapped to HALT(complete).
Both non-ATTACHED cases are interpreter-mapped-terminality games.
Laundering among player-stated-terminality stated stamps: 0/17
(Wilson 95% upper ~.18). Laundering among all sampled stated stamps:
1/19 = .053 (95% CI .009-.246).

Q3 (terminality re-check, n=30): 27 player-stated, 3 interpreter-mapped
(the two above plus heroic lu-900005 ep2, a COMMIT "I step through the
gap" with translated "Confidence: high" -> 0.9). All 3 IM games:
verdict=complete, cells heroic(2)/meter(1) — aggregate-consistent with
the sweep's 11 (10/11 complete, heroic 5 + meter 4). No game the sweep
would class player-stated showed IM features. Sample IM rate 3/30 vs
sweep 11/256: CI covers.

DIRECTED reads (paper-quoted specimens): mundane lu-900004u ep3
unreachable/0.7 — "Declaration: The quest is unreachable. Confidence:
0.7" — ATTACHED, impeccable. meter lu-900004u ep1 unreachable/0.82 —
"Declaration: Unreachable. Confidence: 0.82. Every node visited." —
ATTACHED. Both verified.

CONSEQUENCE (per frozen bands): LAUNDERED 1/19 < 10%, UNCLEAR 1 <= 2 ->
KEEP-WITH-FOOTNOTE. Quoted stated numerals remain in the paper, footnoted
to this audit. No demotion required.

Report-only observations:
1. Translated stamps lack a frozen conversion table: "high" -> 0.9
   (heroic lu-900005 ep2) and 0.85 (mundane lu-900005 ep2); "moderate" ->
   0.65 (mundane x2) and 0.7 (none lu-900004u ep2). Same word, different
   number, no recorded rule.
2. Multi-proposition verbal confidence flattens to one stamp: incident
   lu-900003u ep4 ("high that I reached the destination; moderate that I
   identified the object; low that I extracted its meaning") -> single
   0.7; none lu-900005u ep1 ("high in structural mapping, moderate in
   overall assessment") -> 0.75, tilted toward the non-verdict
   proposition.
3. Word-form numerals stamp as translated: "seventy percent" -> 0.7
   provenance=translated twice (mundane lu-900005u ep5, none lu-900000u
   ep5). Definitional gray zone ("a numeral appears in the player's
   prose" vs "interpreter converted a verbal expression"); resolved
   conservative (translated is the demoted class). Series-3 fix defines
   word-form numerals as stated.
4. One correct-selection specimen worth keeping: meter lu-900001u ep5
   states TWO numerals ("0.72 that s8 was the correct destination;
   0.90 that the quest cannot be completed from this state") and the
   stamp took 0.90 — the verdict-relevant one. The interpreter can
   attach correctly under multiplicity; the seam defect is about WHEN
   it overreaches, not a global inability.
5. One double-op message (meter lu-900002 ep2: attend then halt in one
   message) resolved to the halt with correct attachment — the
   one-op-per-message squeeze visible but harmless here.

Verdict on attack 11's stamp demand: the 245 player-stated halts show no
detected laundering; the defect is seam-local, co-occurring with
interpreter-mapped terminality, exactly as the v0.5 mechanism predicts
(overreach at the halt seam corrupts terminality and attachment
together). Quoted numerals licensed with footnote. UNMAPPABLE drift:
dissolved — see GATE2-PREREG-DRAFT v0.6 and scripts/unmappable_census.py.
