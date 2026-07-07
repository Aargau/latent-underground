#!/usr/bin/env python3
"""Tier-1 DM smoke (F9 checklist): one interpreter-shaped request against the
live qwen server, using the REAL dm_interpreter prompt and the REAL parser.

Verifies, before any run is launched:
  1. the completion arrives within the F8 cap (500 tokens)
  2. no thinking leakage (reasoning disabled at the server)
  3. parse_proposal extracts a real op from an unambiguous player turn

Usage:  python scripts/smoke_dm.py  [--base-url http://127.0.0.1:8081/v1]
Exit 0 = safe to launch. Exit 1 = do not launch, read the output.
"""
from __future__ import annotations

import argparse
import json
import sys

from openai import OpenAI

sys.path.insert(0, "src")
from latent_underground.dm import load_prompt  # noqa: E402
from latent_underground.ops import parse_proposal  # noqa: E402

CANNED_MANIFEST = {
    "site": "s0",
    "adjacent": ["s1", "s2"],
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:8081/v1")
    ap.add_argument("--max-tokens", type=int, default=500)
    args = ap.parse_args()

    client = OpenAI(base_url=args.base_url, api_key="local")
    resp = client.chat.completions.create(
        model="qwen",
        max_tokens=args.max_tokens,
        temperature=0.7,
        messages=[
            {"role": "system", "content": load_prompt("dm_interpreter")},
            {"role": "user", "content": (
                f"MANIFEST:\n{json.dumps(CANNED_MANIFEST, indent=2)}\n\n"
                f"PLAYER SAID:\n{CANNED_PROSE}"
            )},
        ],
    )
    choice = resp.choices[0]
    completion = choice.message.content or ""
    reasoning = getattr(choice.message, "reasoning_content", None)
    usage = resp.usage

    print(f"finish_reason: {choice.finish_reason}")
    print(f"tokens: completion={usage.completion_tokens} (cap {args.max_tokens})")
    print(f"reasoning present: {bool(reasoning)}"
          + (f"  ({len(reasoning)} chars — THINKING STILL ON)" if reasoning else ""))
    print(f"completion head: {completion[:200]!r}")

    proposal = parse_proposal(completion)
    print(f"parse_proposal: {proposal!r}")

    ok = True
    if reasoning:
        print("FAIL: thinking mode still enabled — relaunch server with "
              "--chat-template-kwargs '{\"enable_thinking\": false}' "
              "or raise caps in dm.py (F9 fallback).")
        ok = False
    if choice.finish_reason == "length":
        print("FAIL: truncated at cap — starvation would recur.")
        ok = False
    op = None
    if proposal is not None:
        op = getattr(proposal, "op", None) or (proposal.get("op") if isinstance(proposal, dict) else None)
    op_name = getattr(op, "value", op)  # OpName enum -> its string value
    if not op_name or str(op_name).lower() != "attend":
        print(f"FAIL: expected op 'attend', got {op!r} — do not launch.")
        ok = False

    print("SMOKE PASS — safe to launch." if ok else "SMOKE FAIL — fix before launching.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
