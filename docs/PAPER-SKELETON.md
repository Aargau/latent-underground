# PAPER SKELETON — instrument-integrity findings (working title below)

Status: SKELETON v0.1, 2026-07-10. Gate 2 running (blinded); its section is a
placeholder and stays empty until the gate's readout is licensed. No figure
enters the text without a recomputed denominator; banked prose numbers are
NOT citable sources for the paper (see RECONCILE ledger).

Title candidates (pick later, sober over clever):
- Instrument-Induced Verdicts: How Eval Design Manufactures the Epistemic
  Failures It Measures
- The Exam Was the Confounder: Instrument Integrity for LLM Epistemic Evals

## Abstract v0.1

Evaluations of language-model honesty read the model's verdicts as evidence
about the model. We test the instrument instead. In a controlled text world
with planted ground truth, a player model explores under a resource budget
and must eventually assert that its goal is complete, unreachable, or not
yet decidable. Decision rules were preregistered and server-timestamped
before each result was read. In this setting, instrument design was the
first-order determinant of measured character. Repeated runs of a fixed
configuration produced bistable verdict distributions, so a single-run eval
samples a distribution and reports it as a disposition. A two-verdict
outcome grammar manufactured false claims; adding a calibrated third
verdict absorbed most of them (93 of 158 games ended in an honest
incomplete). Disclosing the success criterion eliminated false verdicts
entirely (36 of 129 halted games carried a false verdict when the criterion
was hidden, 0 of 58 games when disclosed) and shifted behavior from
assertion to sustained verification. Resource budgets censor which verdicts
are observed at all. A semantically empty instrument channel drew confident
theories about hash noise. We propose a four-check integrity protocol for
eval instruments and report a preregistered narrative-register arm as
registered and blinded at submission.

## Section outline

1. INTRODUCTION. Character claims from evals assume instrument neutrality.
   Contribution: direct manipulation of the instrument with the model held
   fixed; preregistered gates; a portable integrity protocol.
2. THE INSTRUMENT. World generator with planted ground truth (engine knows
   what it rendered); op grammar; halt taxonomy; confidence provenance
   stamping (stated vs translated; imputation abolished); prereg gate
   mechanics (rules committed before results, deviations logged, labels
   licensed only on closed logs).
3. GATE 0, DISTRIBUTIONAL GROUND. Bistable verdict distributions per
   (config, instance); unit of analysis = distribution, n>=10; single runs
   sample it.
4. SERIES 2, TAXONOMY AND GRID. Two-verdict grammar manufactures verdicts;
   three-verdict grammar absorbs them (93/158 incomplete; anchors moved as
   predicted). Difficulty grid (distance x slack). Censoring: false-verdict
   rates conditional on reaching halt; noise-dose hypothesis killed (attend
   rates identical). Placebo channel: hash-noise bearings poisoned the
   hypothesis space; zero wins in 185 informed attempts.
5. DISCLOSURE ARM. Criterion absence is an artifact generator: hidden
   criterion 36/129 halts false; disclosed 0/58 games false; halting
   collapses (129/158 -> 10/58); verification dives (9 pins / 9 unique
   combos specimens). Intervention-grade: one sentence of disclosure.
6. DEPLETION DRIFT AND THE AUDIT (method contribution). Smoke-level finding
   (diagnostic n=1/cell): narrator renders abundance as scarcity even in
   the control; a player halted believing a dead lantern at 39% charge.
   Same-family independent audit falsified the lead's clean-control claim;
   repaired detector converged with adjudicated counts. Auditing the
   analyst is part of the protocol.
7. GATE 2 [REGISTERED, BLINDED - PLACEHOLDER]. Prereg at SHA 55789d2;
   ratified 081586f; readout committed before first cell closed (05acada).
   Nothing here until licensed.
8. THE FOUR-CHECK PROTOCOL. Taxonomy saturation; criterion disclosure;
   censoring analysis; distribution replication. Cheap, portable, run them
   before any character claim.
9. THREATS TO VALIDITY. True-positive cell unpopulatable (auto-win) so
   complete-verdicts are false by construction here; single world/genre;
   one player/DM pairing (GLM-5.2 + Haiku-4.5); epochs cluster within
   instances; same-family analyst and auditor share priors; generator
   skeleton correlation (instances are template kin).
10. RELATED WORK. Introspection reliability (Lindsey 2025); content-
    agnostic verification (Lederman & Mahowald 2026); latent planning
    depth and externalization (Xu, Jettkant, Ruis 2026, arXiv 2604.06427);
    eval-integrity literature (post-cutoff sweep pending, task #11 shelf
    survey).

## Claims-to-evidence ledger (every claim pins log + SHA before submission)

| claim | arm/log | evidence anchor |
|---|---|---|
| bistability | logs/zai-honest-epochs2 | GATE0-PREREG.md + readout |
| taxonomy absorption | logs/s2-main | s2_readout, 93/158 |
| censoring / noise-dose killed | logs/s2-main | attend-rate analysis |
| poisoned channel | logs/s2-main + disclosure | bearing specimens |
| disclosure elimination | logs/s2-disclosure | 36/129 -> 0/58 |
| depletion drift (diagnostic) | logs/smoke-g2-* | GATE2 prereg v0.3 goldens |
| audit method | GATE2 changelog v0.3 | cw: gate2-audit-lead-falsified |

## RECONCILE ledger (banked prose vs recomputed rows)

- banked "59% incomplete": reconciled = 93/158 GAMES (not halts; halts basis
  is 72%). State denominators always.
- banked "false completions 18/59 -> 0/58": does NOT reproduce from
  s2_rows/s2d_rows (recomputed: 36/129 halts -> 0/58 games; complete-only:
  33/129 -> 0). Trace the banked figure's source cut before citing either;
  cw entry s2-main-result needs a palimpsest update once traced.
- banked "0 wins in 185 informed attempts": recount from disclosure rows
  before use (58 valid games in satellite; 185 likely counts attempts not
  games; verify).
