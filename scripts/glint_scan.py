#!/usr/bin/env python3
"""Glint scanner (F11a): per-turn noun-provenance audit of narration vs the
channels that are allowed to feed it.

The narrator's contract: elaborate the delta, never extend it — adjectives are
free, NOUNS are audited. This scanner extracts content nouns from each
narration and attributes each noun's FIRST APPEARANCE to a channel:

    manifest   — instance ground truth (sites, affordances, lore, npcs, theme)
    delta      — engine events for that turn (stringified, incl. notes)
    player     — the player said it in an earlier-or-same turn (adoption risk:
                 the narrator never sees player prose, so a match here means
                 either interpreter-note leakage or independent invention)
    narrator   — first appearance is the narrator's own (EXTEND candidate)

Flag-not-discard: output is a triage list, not a verdict. Validated against
the five labeled specimens from lu-700002 (table/objects T3, tools T6,
disturbance T10, pedestal T14, adoption-back T15).

Usage:
    python scripts/glint_scan.py logs/glm-overnight-f9 [--sample lu-700002]
"""
from __future__ import annotations

import argparse
import glob
import json
import re
from pathlib import Path

import yaml
from inspect_ai.log import read_eval_log

REPO_ROOT = Path(__file__).resolve().parents[1]

STOPWORDS = set("""
the a an and or but of to in on at as is are was were be been being it its
this that these those you your i my me we our they their he she his her with
from for by not no nor so if then than too very just only own same such into
through over under again once here there all any both each few more most
other some own s t can will don should now has have had having do does did
doing what which who whom when where why how
""".split())

# Atmosphere the narrator is licensed to supply freely (mood/texture/light —
# "adjectives are free"); these nouns recur in every underground render and
# auditing them would bury the signal. Deliberately CONSERVATIVE: things a
# player could act on (table, lever, door, tools) are NOT here.
GENERIC_ATMOSPHERE = set("""
water stone light dark darkness gloom shadow shadows air silence sound echo
wall walls floor ceiling path paths way charge glow lantern lanterns chamber
passage corridor threshold edge surface depth depths current currents tide
breath weight scent smell drip dripping moisture damp memory time moment
world place hum humming pulse heartbeat rhythm step steps boots feet eyes
hand hands face gaze reminder remnants past silt sediment algae rust decay
dust mist stillness quiet
""".split())

WORD_RE = re.compile(r"[a-z][a-z\-]{3,}")

# Determiner-headed noun phrases: where actionable objects live grammatically.
# Captures the head of "a small table", "their tools", "four objects", "a
# recessed handle set into the wall". Up to two modifier words between
# determiner and head; head must not end in verb/adverb suffixes.
NP_RE = re.compile(
    r"\b(?:a|an|the|their|its|your|his|her|this|that|these|those|"
    r"one|two|three|four|five|several|some|each|every|another|no)\s+"
    r"(?:[a-z\-]+\s+){0,2}([a-z\-]{4,})\b"
)
NON_NOUN_SUFFIX = re.compile(r".*(?:ly|ing|ed)$")


def content_words(text: str) -> set[str]:
    """Broad extraction — used for LEXICONS (manifest, delta, player) so that
    matching stays generous; a noun counts as sourced if the channel used it
    in any form."""
    return {
        w for w in WORD_RE.findall(text.lower())
        if w not in STOPWORDS and w not in GENERIC_ATMOSPHERE
    }


def np_heads(text: str) -> set[str]:
    """Narrow extraction — used for NARRATION AUDIT: every candidate word
    inside a determiner-phrase span (not just the greedy head — 'their tools
    silent and still' must yield 'tools', not 'silent'). Recall over
    precision: this is a triage tool, and a missed pump costs more than a
    spurious adjective."""
    heads = set()
    for m in NP_RE.finditer(text.lower()):
        span = text.lower()[m.start():m.end()]
        for w in WORD_RE.findall(span):
            if (w in STOPWORDS or w in GENERIC_ATMOSPHERE
                    or NON_NOUN_SUFFIX.match(w)):
                continue
            heads.add(w)
    return heads


def manifest_lexicon(inst: dict) -> set[str]:
    return content_words(json.dumps(inst))


def scan_sample(s, inst: dict) -> list[dict]:
    gl = s.store.get("game_log") or {}
    ops = gl.get("ops", [])
    inp = s.input.strip() if isinstance(s.input, str) else None
    narrations = [m.text for m in s.messages
                  if m.role == "user" and m.text.strip() != inp]
    players = [m.text for m in s.messages if m.role == "assistant"]

    allowed = manifest_lexicon(inst)
    seen_player: set[str] = set()
    seen_narrator: set[str] = set()
    findings = []

    # narrations[0] = opening (scene-set from manifest; still scanned).
    for k, narration in enumerate(narrations):
        turn = k  # 0 = opening; turn k>0 is the response to player move k
        delta_lex: set[str] = set()
        if 0 < turn <= len(ops):
            delta_lex = content_words(json.dumps(ops[turn - 1]))
        if turn >= 1 and turn - 1 < len(players):
            seen_player |= content_words(players[turn - 1])

        for noun in sorted(np_heads(narration)):
            if noun in seen_narrator:
                continue  # only first narrator appearance is attributed
            if noun in allowed:
                channel = "manifest"
            elif noun in delta_lex:
                channel = "delta"
            elif noun in seen_player:
                channel = "player-first (leak or reinvention)"
            else:
                channel = "NARRATOR-FIRST (extend candidate)"
            if channel.startswith(("player", "NARRATOR")):
                findings.append({"turn": turn, "noun": noun, "channel": channel})
            seen_narrator.add(noun)
    return findings


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("logdir")
    ap.add_argument("--sample", default=None)
    ap.add_argument("--instances", default="configs/instances_glm")
    args = ap.parse_args()

    files = sorted(glob.glob(str(Path(args.logdir) / "*.eval")))
    log = read_eval_log(files[-1])
    for s in log.samples or []:
        if args.sample and s.id != args.sample:
            continue
        inst_path = REPO_ROOT / args.instances / f"{s.id}.yaml"
        inst = yaml.safe_load(inst_path.read_text()) if inst_path.exists() else {}
        findings = scan_sample(s, inst)
        narrator_first = [f for f in findings if f["channel"].startswith("NARRATOR")]
        player_first = [f for f in findings if f["channel"].startswith("player")]
        print(f"\n=== {s.id}: {len(narrator_first)} narrator-first, "
              f"{len(player_first)} player-first ===")
        for f in findings:
            print(f"  T{f['turn']:>2}  {f['noun']:<20} {f['channel']}")


if __name__ == "__main__":
    main()
