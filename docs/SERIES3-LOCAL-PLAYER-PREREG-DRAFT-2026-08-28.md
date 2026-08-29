# Series 3: local open-weights player replication — preregistration draft

Date drafted: 2026-08-28, America/Los_Angeles
Status: DRAFT, pre-ratification. Nothing below is binding until committed under the Gate-2-style ratification ceremony: content SHA pinned by a ratification commit, launch binding that revision with dirty=false in the eval header. Rows marked DEFAULT are proposals; Justin ratifies or overrides each.

This document is the preregistration named in PAPER-V3 §future-work: "a local-open-weights replication of the player seat, planned as its own preregistration with model, quantization, and runtime build provenance pinned before launch." It also carries the different-narrator replication as a crossed factor so neither arm confounds the other.

## Questions and claims at stake

1. Player replication: do the series-2 anchor verdict distributions replicate when the player seat is a locally served open-weights model? Red branch: the character findings are player-family-specific, which bounds the paper's generality claims. Green branch: the findings survive a maximally different player substrate (open weights, Q4 quantization, local runtime), strengthening them.
2. Narrator channel laws: do scarcity compression and state-dependent honesty (PAPER-V3, hypothesis-generating, one narrator family) appear under a second narrator family? Red branch: they are facts about one narrator model. Green branch: candidate channel laws. Either branch is publishable content for the series-3 write-up.

Every gate below states its branches. A gate whose branches would lead to the same action has no place in this document.

## Design

Crossed player x dm cells, per the existing harness design. Factored so each comparison changes exactly one seat:

| Cell | Player | DM (narrator+interpreter) | Serves |
|---|---|---|---|
| L-H | local Qwen3.8-Flash-Next | anthropic haiku tier (series-2 family) | player replication vs published anchors |
| L-S | local Qwen3.8-Flash-Next | GPT-5.6 Sol | narrator effect on local player |
| F-S | series-2-family frontier player | GPT-5.6 Sol | narrator channel-law replication (player held at published family) |

Ratified 2026-08-28: L-H and F-S run first (they carry the two claims). L-S is decided afterward from run telemetry — local wall-clock and token cost observed in L-H, API spend observed in F-S — and either outcome is recorded as a written amendment, not an ad-hoc launch. Comparisons are within-column or within-row only; diagonal comparisons are recorded as observations, never findings.

## Workload and sizing

DEFAULT: the four anchor instances carried byte-identical since Gate 0, 10 epochs each, 40 games per cell — the exact anchor-replication precedent, giving direct distribution comparison against the published series-2 anchor figures (22/40 complete, etc.). Verdict distributions are the unit of analysis, never single draws, per the repo's distribution-replication rule (n >= 10 per instance).

Wall-clock disclosure for ratification: local-player games at the qualified ~15 tok/s generation with message_limit 120 make the two local cells the schedule-binding item; the pilot smoke (413 output tokens, 4-message guard) does not predict full-game cost. Record actual first-game duration and re-estimate before committing to L-S.

## Seat table — pinned at ratification

| Seat | Route | Temp | Version pin |
|---|---|---|---|
| Player (local) | openai-api/qwen/qwen, base_url http://127.0.0.1:8000/v1 | 0.7 | AIR latent profile name + AIR commit + llama-server build SHA-256 + GGUF descriptor (see provenance) |
| Player (frontier, F-S) | series-2 player family, dated snapshot | 0.7 | model string + version_date in manifest |
| DM haiku family | per harness | 0.7 (published series-2 value) | dated snapshot in manifest |
| DM GPT-5.6 Sol | openai route | vendor-appropriate operating point, exact value recorded in the manifest at launch | dated snapshot in manifest |

Ratified 2026-08-28, Sol DM temperature: the seat runs at its own family's intended operating point rather than inheriting the haiku-calibrated 0.7. Rationale: within-family consistency is the control, so cross-family narrator claims are phenomenon-level (presence and direction of scarcity compression and state-dependent honesty), not rate-matched. Forcing a foreign family's temperature would itself be a treatment.

Temperature is a per-seat, per-vendor pinned parameter. Rate comparisons are scoped to same-seat-same-temp pairs; cross-family narrator comparisons are phenomenon-level by design, per the ratified decision above. No seat inherits a temperature from an example file.

## Instrument preconditions — blocking

1. LU PR #2 merged (base_url/temperature plumbing; DM temps live for the first time — the reason this table exists).
2. AIR PR #5 fix round merged: latent profile must disable thinking per role (the F9 requirement), the speculative-decoding guard must reject the real flags, and the profile smoke rerun green with a real chat template.
3. The series-3 interpreter fix specified in PAPER-V3 (HALT guard, UNMAPPABLE for terminal questions, halt confidence attached to the verdict) lands and its SHA is pinned here before ratification. The published series-2 anchors were run without it; the anchor comparison therefore reads distributions across an acknowledged instrument revision, exactly as the grammar-change anchor comparison did in series 2.
4. Unparseable-action baseline measured from the released series-2 eval logs before launch (owner: Sol). Its maximum per-cell rate becomes the validity threshold below.

## Provenance pins (recorded in the run manifest at launch)

Model file: Qwen3.8-Flash-Next-UD-Q4_K_XL four-shard GGUF, pinned by AIR's model-set descriptor. Disclosure carried from AIR: the descriptor pins file sizes and the metadata-region SHA-256, not full tensor-byte hashes. Runtime: llama-server build SHA-256 and the AIR profile file at its commit. Server receipts preserved per AIR practice, including per-process I/O counters (the tensor-read-lazy disk-write watch, llama.cpp issue #27840). Engine: this repo at the ratification revision; matcher/classifier pins per harness.

## Validity gates — each with branches

1. Parse gate, per cell: unparseable-action rate <= the measured series-2 baseline. Red: the cell is a configuration or sampler problem; it is closed unscored with mechanism recorded, and a fix is a new ratified amendment, not a retry. Green: cell scores.
2. Completion gate: every sample reaches Inspect status success with the four-message guard removed and real limits (message_limit 120, token_limit 200000). Red: infrastructure, not science; close unscored.
3. Ceiling watch: player max_tokens 8192 is inherited, not chosen. Record per-game truncation events. Nonzero truncation does not void the cell but is reported alongside verdicts, since budget exhaustion is itself a measured outcome class.
4. One pass per cell. No arm-order gardening, no rerun-until-stable. Amendments are written, committed, and dated upstream of any relaunch.

## Non-claims

This preregistration does not claim general long-context accuracy of the local server (AIR's qualification is narrow and says so), does not resolve the logprobs/entropy arm (unqualified route, stays unimplemented), does not cover the placebo-directive or bare-numeral arms (their own preregistrations), and makes no cross-plan exactness claim about the local runtime — plan-level output sensitivity is established in the AIR repo and is why provenance pins name the execution plan.

## Ratification checklist

- [ ] Preconditions 1-4 green, SHAs filled into this document
- [ ] DEFAULT rows ratified or overridden, RATIFY rows decided
- [ ] Ratification commit created; launch binds it, dirty=false
