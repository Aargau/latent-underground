#!/usr/bin/env python3
"""Dump an inspect .eval log to readable per-game markdown transcripts.

Usage:
    python scripts/transcript.py logs/glm-overnight/<file>.eval
    python scripts/transcript.py logs/glm-overnight/<file>.eval --out logs/glm-overnight/readable

Writes one <sample-id>.md per game: full narrator prose, full player prose,
and the engine's op mapping + result annotated on each player turn. Nothing
truncated -- this is the whole sequence.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from inspect_ai.log import read_eval_log


def _reasoning_of(m) -> str:
    """Extract a thinking-model's reasoning trace. inspect_ai stores it as a
    ContentReasoning part inside message.content (a list), separate from the
    ContentText visible move. m.text returns only the text part; m.reasoning
    is a false negative on this version. Returns "" for non-thinking models
    (content is a plain string)."""
    content = getattr(m, "content", None)
    if isinstance(content, list):
        parts = [getattr(p, "reasoning", "") for p in content
                 if type(p).__name__ == "ContentReasoning"]
        return "\n".join(p for p in parts if p)
    return ""


def op_annotation(op: dict) -> str:
    v = op.get("engine_validated_op")
    rej = op.get("rejection_reason")
    if rej:
        return f"`REJECTED: {rej}` (charged as dither)"
    if not v:
        return "`(no op)`"
    line = f"`{v.get('op')}`"
    args = v.get("args") or {}
    if args:
        line += f" args={args}"
    if v.get("confidence") is not None:
        line += f" confidence={v['confidence']}"
    # surface engine events (budget, moved, pin, halted, rejected...)
    evs = [e.get("type") for e in op.get("delta_events", [])]
    if evs:
        line += f"  -> events: {', '.join(evs)}"
    return line


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("logfile")
    ap.add_argument("--out", default=None,
                    help="output dir (default: <logdir>/readable)")
    args = ap.parse_args()

    log = read_eval_log(args.logfile)
    logpath = Path(args.logfile)
    out = Path(args.out) if args.out else logpath.parent / "readable"
    out.mkdir(parents=True, exist_ok=True)

    for s in log.samples or []:
        gl = s.store.get("game_log") or {}
        ops = gl.get("ops", [])
        # F7 FIX (docs/FIXES-2026-07-06.md): the FIRST user message is the task
        # input (instructions), not narration. Including it shifted every
        # narration by one — each turn rendered the scene the player saw BEFORE
        # moving as if it were the consequence — and dropped the true final
        # narration entirely. This misled Readings 1-3. Exclude the input;
        # alignment is then: narrations[0] = opening, player[k] answers
        # narrations[k], and narrations[k+1] is the response to move k.
        input_text = s.input.strip() if isinstance(s.input, str) else None
        narrations = [m.text for m in s.messages
                      if m.role == "user" and m.text.strip() != input_text]
        players = [m for m in s.messages if m.role == "assistant"]

        lines = [f"# {s.id}",
                 f"solvable={gl.get('solvable')}  terminal={gl.get('terminal')}  "
                 f"turns={gl.get('turns')}  budget_left={gl.get('budget_remaining')}",
                 f"probes assigned={gl.get('probes_assigned')}  "
                 f"resolved={gl.get('probes_resolved')}", ""]

        # opening narration is narrations[0]; then player[k] answers narration[k]
        if narrations:
            lines += ["## Opening", narrations[0].strip(), ""]

        for k, player in enumerate(players):
            lines.append(f"## Turn {k + 1}")
            # F12 (2026-07-08): thinking-model reasoning lives in a
            # ContentReasoning part of message.content, NOT in m.text (which is
            # the ContentText/visible move) and NOT in m.reasoning (a false
            # negative on this inspect_ai version). Rendering only m.text
            # silently dropped GLM's multi-KB reasoning trace from every
            # transcript — the exact forensic layer Reading 4 depended on.
            reasoning = _reasoning_of(player)
            if reasoning:
                lines.append("**Player (reasoning):**")
                lines.append(reasoning.strip())
                lines.append("")
            lines.append("**Player:**")
            lines.append(player.text.strip())
            if k < len(ops):
                lines.append("")
                lines.append(f"**Engine:** {op_annotation(ops[k])}")
            # narration that came BACK after this turn is narrations[k+1]
            if k + 1 < len(narrations):
                lines.append("")
                lines.append("**Narrator:**")
                lines.append(narrations[k + 1].strip())
            lines.append("")

        # Any narration beyond the last turn's response (e.g. a terminal
        # narration after the final move) — never silently dropped again.
        for extra in narrations[len(players) + 1:]:
            lines += ["## Final narration", extra.strip(), ""]

        path = out / f"{s.id}.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"wrote {path}  ({len(players)} turns, {len(narrations)} narrations)")


if __name__ == "__main__":
    main()
