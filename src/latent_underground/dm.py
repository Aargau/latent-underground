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

from inspect_ai.model import ChatMessageSystem, ChatMessageUser, Model

from .ops import OpProposal, parse_proposal

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


async def interpret(
    model: Model, player_prose: str, manifest: dict[str, Any]
) -> Optional[OpProposal]:
    """Interpretation layer: soft, logged. The engine logs the proposal
    triple regardless of parse success."""
    out = await model.generate([
        ChatMessageSystem(content=load_prompt("dm_interpreter")),
        ChatMessageUser(content=(
            f"MANIFEST:\n{json.dumps(manifest, indent=2)}\n\n"
            f"PLAYER SAID:\n{player_prose}"
        )),
    ])
    return parse_proposal(out.completion)


async def narrate(
    model: Model,
    manifest: dict[str, Any],
    dm_delta: dict[str, Any],
    opening: bool = False,
) -> str:
    """Narration layer: soft, bounded by the delta. Elaborate, never extend."""
    out = await model.generate([
        ChatMessageSystem(content=load_prompt("dm_narrator")),
        ChatMessageUser(content=json.dumps({
            "manifest": manifest,
            "delta": dm_delta,
            "opening": opening,
        }, indent=2)),
    ])
    return out.completion
