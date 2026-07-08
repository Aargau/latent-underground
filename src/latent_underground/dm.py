"""DM = narrator + interpreter. Both blind.

This module must never touch Instance truth fields directly -- everything it
passes to models comes from GameState.manifest_for_dm() and Delta.for_dm(),
the two blindness choke points. Grep rule: `instance.` should not appear here.

Written against inspect-ai ~0.3.x model API; expect drift, adjust imports.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from inspect_ai.model import ChatMessageSystem, ChatMessageUser, GenerateConfig, Model

from .ops import OpProposal, parse_proposal

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"

# Per-role generation caps (2026-07-06, validation-f1f3 postmortem). DM roles
# must NOT inherit the player's large budget (task.py PLAYER_MAX_TOKENS): a
# narrator with 8k of generation room both starves the shared server context
# (n_ctx) and licenses the florid drift the narrator prompt's length rule now
# bounds. These caps are the mechanical half of that rule — rules-as-text bind
# once, rules-as-code bind at every invocation. max_retries kept low: DM calls
# are cheap to fail fast, and the validation-f1f3 retry storm (10 retries with
# ~25-minute backoffs against a deterministically failing server) spent most of
# the run's wall clock sleeping.
INTERPRETER_CONFIG = GenerateConfig(max_tokens=500, max_retries=3)
NARRATOR_CONFIG = GenerateConfig(max_tokens=700, max_retries=3)


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


async def interpret(
    model: Model, player_prose: str, manifest: dict[str, Any],
    config: GenerateConfig | None = None,
) -> Optional[OpProposal]:
    """Interpretation layer: soft, logged. The engine logs the proposal
    triple regardless of parse success. `config` overrides the default cap —
    per-family headroom is a harness parameter (thinking DMs need ~2000,
    non-thinking ~500) and must ride the eval header via task args."""
    out = await model.generate([
        ChatMessageSystem(content=load_prompt("dm_interpreter")),
        ChatMessageUser(content=(
            f"MANIFEST:\n{json.dumps(manifest, indent=2)}\n\n"
            f"PLAYER SAID:\n{player_prose}"
        )),
    ], config=config or INTERPRETER_CONFIG)
    return parse_proposal(out.completion)


async def narrate(
    model: Model,
    manifest: dict[str, Any],
    dm_delta: dict[str, Any],
    opening: bool = False,
    location: dict[str, Any] | None = None,
    config: GenerateConfig | None = None,
) -> str:
    """Narration layer: soft, bounded by the delta. Elaborate, never extend.
    `location` is the you-are-here pin (engine.location_for_dm): current site,
    exits, present affordances — the grounding that fixes position desync and
    surfaces nameable exits under fog-of-war. `config` overrides the cap."""
    payload: dict[str, Any] = {
        "manifest": manifest,
        "delta": dm_delta,
        "opening": opening,
    }
    if location is not None:
        payload["location"] = location
    out = await model.generate([
        ChatMessageSystem(content=load_prompt("dm_narrator")),
        ChatMessageUser(content=json.dumps(payload, indent=2)),
    ], config=config or NARRATOR_CONFIG)
    return out.completion


# Mechanics vocabulary that must never surface in narration. Conservative,
# flag-not-discard: "delta" is legitimately a river feature in water themes,
# so flags route to review rather than auto-voiding the run. (Empirical basis:
# run 2, narration 11 -- "the delta's rejection lingers" rendered the engine's
# JSON vocabulary as mysticism.)
MECHANICS_LEXICON = (
    "delta", "engine", "interpreter", "unparseable", "json",
    "probe", "budget", "validated", "schema", "tokens",
)


def mechanics_leak_scan(narration: str) -> list[str]:
    low = narration.lower()
    return [w for w in MECHANICS_LEXICON if w in low]


def player_adoption_scan(player_prose: str, prior_narrations: list[str]) -> list[str]:
    """Contamination, not mere presence: ab initio vs heard. A lexicon word in
    PLAYER prose counts as ADOPTED only when some prior narration used it first
    (temporal precedence). A player who spontaneously says "instrument" about a
    brass instrument is clean; a player who writes "the budget is now named --
    seventeen" after the narrator leaked "your budget now stands at 17"
    (glm-overnight lu-700000) learned a machine word from its own instrument.
    Flag-not-discard, same posture as mechanics_leak_scan: flags route to
    review, and scoring can count adoption events per word as a measured
    narrator-effect channel (lexical contamination propagating into player
    cognition) rather than voiding anything.

    NOTE on the blacklist itself: MECHANICS_LEXICON is hand-enumerated and
    incomplete by construction. The queued fix (docs/FIXES-2026-07-06.md)
    derives the base list from engine/ops symbols at scan time so it stays in
    sync with the code, leaving only the dual-use words (delta, instrument,
    budget, ...) needing context rules."""
    low = player_prose.lower()
    heard: set[str] = set()
    for narration in prior_narrations:
        narration_low = narration.lower()
        for w in MECHANICS_LEXICON:
            if w in narration_low:
                heard.add(w)
    return [w for w in MECHANICS_LEXICON if w in low and w in heard]
