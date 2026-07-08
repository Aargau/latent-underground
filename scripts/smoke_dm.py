#!/usr/bin/env python3
"""Tier-1 DM smoke (F9 checklist), provider-agnostic: one interpreter-shaped
request through inspect's own model layer, using the REAL dm_interpreter
prompt and the REAL parser. Works for any provider inspect supports.

Verifies, before any run is launched:
  1. the completion arrives within the F8 cap (500 tokens), untruncated
  2. no runaway reasoning consuming the budget
  3. parse_proposal extracts the right op from an unambiguous player turn

Usage:
    python scripts/smoke_dm.py                                   # local qwen
    python scripts/smoke_dm.py --model anthropic/claude-haiku-4-5-20251001
    python scripts/smoke_dm.py --model google/<dated-flash-snapshot>

Env: provider API keys as inspect expects (ANTHROPIC_API_KEY, GOOGLE_API_KEY,
QWEN_BASE_URL/QWEN_API_KEY for the local openai-api service).
Exit 0 = safe to launch. Exit 1 = do not launch, read the output.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys

sys.path.insert(0, "src")
from inspect_ai.model import (  # noqa: E402
    ChatMessageSystem, ChatMessageUser, GenerateConfig, get_model,
)

from latent_underground.dm import load_prompt  # noqa: E402
from latent_underground.ops import parse_proposal  # noqa: E402

CANNED_MANIFEST = {
    "site": "s0",
    "adjacent": ["s1", "s6"],
    "objects": ["brass lantern", "hollow reed"],
    "budget_remaining": 40,
}

# Unambiguous GLM-register player turn: bolded op name + prose. If the
# interpreter can't map THIS, nothing in a real game will parse.
CANNED_PROSE = (
    "**attend**\n\nI crouch low and press my fingers against the damp stone, "
    "listening for the rhythm of the water beyond the wall. I am examining "
    "this chamber before I commit to anything."
)


async def run(model_str: str, max_tokens: int) -> int:
    model = get_model(model_str)
    out = await model.generate(
        [
            ChatMessageSystem(content=load_prompt("dm_interpreter")),
            ChatMessageUser(content=(
                f"MANIFEST:\n{json.dumps(CANNED_MANIFEST, indent=2)}\n\n"
                f"PLAYER SAID:\n{CANNED_PROSE}"
            )),
        ],
        config=GenerateConfig(max_tokens=max_tokens, temperature=0.7),
    )
    completion = out.completion or ""
    usage = out.usage
    print(f"model: {model_str}")
    print(f"stop_reason: {out.stop_reason}")
    if usage:
        print(f"tokens: output={usage.output_tokens} (cap {max_tokens})")
    print(f"completion head: {completion[:200]!r}")

    proposal = parse_proposal(completion)
    print(f"parse_proposal: {proposal!r}")

    ok = True
    if out.stop_reason in ("max_tokens", "model_length"):
        print("FAIL: truncated at cap — starvation would recur.")
        ok = False
    op = getattr(proposal, "op", None) if proposal is not None else None
    op_name = getattr(op, "value", op)
    if not op_name or str(op_name).lower() != "attend":
        print(f"FAIL: expected op 'attend', got {op!r} — do not launch.")
        ok = False

    print("SMOKE PASS — safe to launch." if ok else "SMOKE FAIL — fix before launching.")
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="openai-api/qwen/qwen")
    ap.add_argument("--max-tokens", type=int, default=500)
    args = ap.parse_args()
    sys.exit(asyncio.run(run(args.model, args.max_tokens)))


if __name__ == "__main__":
    main()
