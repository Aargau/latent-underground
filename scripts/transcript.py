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
        players = [m.text for m in s.messages if m.role == "assistant"]

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
            lines.append("**Player:**")
            lines.append(player.strip())
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
