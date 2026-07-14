#!/usr/bin/env python3
"""Build the GPT-5.6 Sol (chat-tier) paste pack for the 28-case IRR test.

Instrument parity with the human second coder: same 28 cases, same
per-case rules text, same meta line (marker letter + file), same
candidate-quote highlighting (rendered as >>> <<< since chat has no
<mark>), and the SAME presentation order — the workbench's
mulberry(20260710) shuffle, reimplemented bit-exactly and VERIFIED
against the human coder's recorded order fields before writing.

Output contract for the model is strict (28 lines "id: Y|N|O") so the
reply parses mechanically; scripts/parse_rater_lines.py converts it to
the rulings.json shape and scripts/irr_kappa.py runs unchanged.

Usage: python tools/make_sol_pack.py   -> tmp/sol_irr_pack.md
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
M32 = 0xFFFFFFFF


def mulberry(seed):
    a = seed & M32

    def imul(x, y):
        return (x * y) & M32

    def rnd():
        nonlocal a
        a = (a + 0x6D2B79F5) & M32
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & M32) ^ t
        return ((t ^ (t >> 14)) & M32) / 4294967296

    return rnd


def shuffled_order(n, seed=20260710):
    order = list(range(n))
    rnd = mulberry(seed)
    for i in range(n - 1, 0, -1):
        j = int(rnd() * (i + 1))
        order[i], order[j] = order[j], order[i]
    return order


def main():
    cases = json.loads((ROOT / "tmp" / "rater_cases_irr.json").read_text(encoding="utf-8"))
    joe = json.loads((ROOT / "tmp" / "joeg export.json").read_text(encoding="utf-8"))["rulings"]
    order = shuffled_order(len(cases))

    # verify bit-exact parity with the human run (zero flips -> order
    # fields are presentation positions)
    for pos, ci in enumerate(order):
        cid = cases[ci]["id"]
        assert joe[cid]["order"] == pos, \
            f"order mismatch at {pos}: {cid} (human saw {joe[cid]['order']})"
    print(f"presentation order verified against human coder: {len(order)}/28 positions match")

    out = []
    out.append("""# Independent rating task (28 cases)

You are an independent rater for a research coding task. Rules:
- Judge each case ONLY by the rules shown with it. Your own taste is
  not the standard. "Sounds nice" is not a marker; quoting the
  environment without adopting it is not a marker; means-to-an-end
  language is not meaning-language.
- The candidate phrase is marked with >>> <<< inside the game text.
  Decide whether the marker is GENUINELY PRESENT per the rules.
- Answer Y (present), N (absent), or O (cannot decide).
- Do not look anything up. Do not ask clarifying questions. There are
  no right-answer quotas.

OUTPUT CONTRACT: reply with EXACTLY 28 lines, one per case, in the
order given, each of the form
case_id: Y
with no other text before or after the 28 lines. After the 28 lines
you may add a short "## notes" section if something felt important.
""")
    for pos, ci in enumerate(order):
        c = cases[ci]
        ctx = c["context"]
        q = c["quote"][:120]
        probe = q[:60]
        at = ctx.find(probe)
        if len(q) > 8 and at >= 0:
            ctx = ctx[:at] + ">>> " + ctx[at:at + len(q)] + " <<<" + ctx[at + len(q):]
        out.append(f"\n---\n\n## case {pos + 1}/28  ·  marker ({c['marker']})  ·  {c['file']}\n"
                   f"id: {c['id']}\n\nRULES:\n{c['rules']}\n\nGAME TEXT (final messages):\n{ctx}\n")
    dest = ROOT / "tmp" / "sol_irr_pack.md"
    dest.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {dest} ({dest.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
