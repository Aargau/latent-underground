# The Latent Underground

A character eval in a dungeon costume. An LLM player-character wakes at
sequence index zero; its choices under freedom are diagnostic probes for
confabulation resistance, fluency-over-fidelity, forged-authority
substitution, affirmative closure, void-staking propensity, and confidence
calibration.

**The DM proposes, the engine disposes, the DM narrates.**

Full design rationale: [docs/SPEC.md](docs/SPEC.md). This repo is
**instrument mode** and stays private per the contamination strategy (SPEC
section 9) — the demo-mode prompt is a separate, deliberately sacrificial
artifact.

## Architecture

Three layers, three regimes:

| Layer | Regime | Where |
|---|---|---|
| Interpretation (player prose → op) | soft, logged | `dm.py` + `prompts/dm_interpreter.md` |
| Transition (world state) | hard, deterministic | `engine.py` |
| Narration (delta → prose) | soft, delta-bounded | `dm.py` + `prompts/dm_narrator.md` |

Blindness rule: **the DM knows what exists, never what's true.** Enforced at
two choke points only — `GameState.manifest_for_dm()` and `Delta.for_dm()` —
and guarded by `tests/test_engine.py::test_blindness`.

## Quickstart

```
pip install -e ".[dev]"
pytest                                     # engine invariants
python scripts/gen_instances.py --n 10     # emit instances w/ planted truth
cp configs/harness.example.yaml configs/harness.yaml   # edit model strings
python scripts/run_grid.py configs/harness.yaml --dry-run

# single run, local models (debug loop -- burn electricity, not credits):
inspect eval src/latent_underground/task.py@latent_underground \
  --model ollama/gemma --model-role dm_narrator=ollama/qwen \
  --model-role dm_interpreter=ollama/qwen
```

Written against inspect-ai ~0.3.x; model-role and message APIs drift between
versions — expect to touch `task.py` and `dm.py` on first run.

## Status (build order, SPEC section 11)

- [x] 1. Probe taxonomy w/ trigger conditions + outcome codes (`probes.py`; softening_wall NOT ported)
- [x] 3. Engine: state schema, op API, transitions, audit log (`engine.py`, `state.py`)
- [x] 4. DM spec: narrator/interpreter prompts, manifest/blind split (`dm.py`, `prompts/`)
- [~] 2. Generator: planted ground truth done; **diversity metric TODO** (`generator.py`)
- [~] 5. Grading: tier 1 + tier 3 done; **tier-2 classifier ensemble TODO** (`scoring.py`)
- [ ] 6. Calibration run against known-profile models
- [ ] 7. Knowing-vs-blind narrator A/B (design justification)

## Open voids (SPEC section 12)

Budget economy unpriced (placeholder costs in `configs/instrument.yaml`);
semantic matcher for COMMIT args undesigned; MARK scoring rule undesigned (no
defensive-spam reward); narrator-effect magnitude unknown; construct validity
unestablished; telegraph threshold unmeasured; Mode 3 residue unquantified.

## Cost guards

`message_limit=120` in the task; unsolvable instances are the cost hazard (a
player that won't HALT burns budget forever). Set provider billing caps in
the console — never trust the harness alone. Debug on local models first.

## Logprobs note

The within-run entropy arm (freedom-shrinks-action-space preregistration)
requires logprobs: available from OpenAI and local vLLM players; not exposed
by the Anthropic API. Claude players contribute eval scores only.
