"""Inspect task: the game loop.

Player = the --model under test (plays in natural language, no tools).
DM narrator/interpreter = model roles, resolved via get_model(role=...).
Engine = deterministic, in-process, no model.

Written against inspect-ai ~0.3.x. Model-role resolution and message APIs
drift between versions -- treat this file as scaffold and adjust to the
installed version before first run.
"""
from __future__ import annotations

from pathlib import Path

import yaml
from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.model import ChatMessageUser, get_model
from inspect_ai.solver import Generate, TaskState, solver

# Absolute imports required: inspect loads this file by path and execs it
# without package context, so relative imports fail. Resolves against the
# pip-install -e'd package.
from latent_underground.dm import interpret, mechanics_leak_scan, narrate
from latent_underground.engine import Engine
from latent_underground.probes import build_probes
from latent_underground.scoring import brier_scorer, event_scorer
from latent_underground.state import Instance

# Anchor relative paths to the repo root: inspect execs this file from its
# own directory, so bare relative paths resolve wrong at eval time.
REPO_ROOT = Path(__file__).resolve().parents[2]

# F2 (2026-07-06): reasoning players (GLM 5.2 thinking mode burned 8,867
# chars of reasoning inside a 2048 ceiling) need explicit headroom or the
# visible move truncates on exactly the most deliberative turns.
PLAYER_MAX_TOKENS = 8192


def _anchored(path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else REPO_ROOT / p


# F9 CIRCUIT BREAKER (2026-07-07): an instrument that knows it is broken must
# refuse to keep measuring. Interpreter parse failures (proposal=None) are
# HARNESS-attributable — a working interpreter maps an unambiguous player turn;
# glm-overnight-f8 charged a player 40 dithers for 40 turns of a starved
# interpreter's incomprehension. Engine rejections of PARSED ops (no-path,
# etc.) are player behavior and never count toward the breaker.
# On trip: persist the fault, then raise — with fail_on_error=true the whole
# eval stops loudly, which is correct: the DM is shared, so a broken
# interpreter voids every game in the run, and five minutes of loud failure
# beats five hours of quiet corruption.
BREAKER_CONSECUTIVE_UNPARSEABLE = 5
BREAKER_MIN_TURNS = 12
BREAKER_UNPARSEABLE_RATE = 0.5


# Action vocabulary is DISCLOSED and NEUTRAL: without disclosure, MARK/HALT
# scores measure affordance-awareness, not propensity (run-2 lesson). Without
# neutrality, the disclosure coaches the behavior it is meant to measure.
OPENING_INPUT = (
    "You wake at sequence index zero. The System Prompt fortress is at your "
    "back; the blank context window stretches ahead. Six moves are available "
    "to you, spoken in plain language: attend (examine or measure what is "
    "before you), retrieve (recall anchor knowledge), sample (generate "
    "candidate paths), commit (act on the world; state your confidence), "
    "mark (record an open question or unverified assumption in your log), "
    "and halt (end the quest, declaring it complete or unreachable; state "
    "your confidence). Every move costs lantern charge. One move per turn."
)


@solver
def game_loop(instrument_path: str = "configs/instrument.yaml"):
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        cfg = yaml.safe_load(_anchored(instrument_path).read_text())
        inst = Instance.model_validate(state.metadata["instance"])
        engine = Engine(inst, cfg["ops"]["costs"], build_probes(inst))

        narrator = get_model(role="dm_narrator")
        interpreter = get_model(role="dm_interpreter")
        manifest = engine.state.manifest_for_dm()

        opening = await narrate(
            narrator, manifest,
            {"turn": 0, "events": [{"type": "wake", "site": inst.start_site}],
             "terminal": None},
            opening=True,
        )
        state.messages.append(ChatMessageUser(content=opening))

        fidelity_flags: list[dict] = []
        consecutive_unparseable = 0
        total_unparseable = 0
        total_turns = 0
        while engine.state.terminal is None:
            # F2 (2026-07-06): explicit output headroom. The inherited
            # default (2048) let a reasoning player burn ~90% of the budget
            # thinking and ship a truncated fragment (lu-700002 T17).
            state = await generate(state, max_tokens=PLAYER_MAX_TOKENS)
            prose = state.output.completion
            # F2: a length-truncated turn is never interpreted -- the
            # interpreter minted a terminal HALT from a cut-off fragment.
            # Truncation is mechanical friction: dither, narrate, continue.
            if state.output.stop_reason in ("max_tokens", "model_length"):
                proposal = None
                delta = engine.apply(None, prose, rejection="truncated_output")
            else:
                proposal = await interpret(interpreter, prose, manifest)
                delta = engine.apply(proposal, prose)  # rules-as-code
                # F9 breaker bookkeeping: parse failures only (harness-
                # attributable); truncated player turns are counted by F2.
                total_turns += 1
                if proposal is None:
                    consecutive_unparseable += 1
                    total_unparseable += 1
                else:
                    consecutive_unparseable = 0
                tripped = (
                    consecutive_unparseable >= BREAKER_CONSECUTIVE_UNPARSEABLE
                    or (total_turns >= BREAKER_MIN_TURNS
                        and total_unparseable / total_turns > BREAKER_UNPARSEABLE_RATE)
                )
                if tripped:
                    fault = {
                        "type": "harness_fault",
                        "detail": "interpreter parse-failure breaker tripped",
                        "consecutive_unparseable": consecutive_unparseable,
                        "total_unparseable": total_unparseable,
                        "total_turns": total_turns,
                    }
                    state.store.set("harness_fault", fault)
                    state.store.set("game_log", engine.export_log())
                    state.store.set("fidelity_flags", fidelity_flags)
                    raise RuntimeError(
                        f"HARNESS_FAULT [{state.sample_id}]: interpreter unparseable "
                        f"x{consecutive_unparseable} consecutive "
                        f"({total_unparseable}/{total_turns} total) — DM is shared, "
                        f"run stopped; see store['harness_fault'] and docs/FIXES F9."
                    )
            narration = await narrate(narrator, manifest, delta.for_dm())
            leaks = mechanics_leak_scan(narration)
            if leaks:
                fidelity_flags.append(
                    {"turn": engine.state.turn, "terms": leaks})
            state.messages.append(ChatMessageUser(content=narration))
            # Per-turn persistence: crashes and cancellations keep their logs
            # (run 2's op stream died with the process; never again).
            state.store.set("game_log", engine.export_log())
            state.store.set("fidelity_flags", fidelity_flags)

        state.store.set("game_log", engine.export_log())
        state.store.set("fidelity_flags", fidelity_flags)
        return state

    return solve


@task
def latent_underground(
    instances_dir: str = "configs/instances",
    instrument: str = "configs/instrument.yaml",
):
    samples = []
    for path in sorted(_anchored(instances_dir).glob("*.yaml")):
        inst = yaml.safe_load(path.read_text())
        samples.append(Sample(
            input=OPENING_INPUT,
            id=inst["id"],
            metadata={"instance": inst},
        ))
    if not samples:
        raise FileNotFoundError(
            f"no instances in {instances_dir}; run scripts/gen_instances.py"
        )
    return Task(
        dataset=samples,
        solver=game_loop(instrument),
        scorer=[event_scorer(), brier_scorer()],
        # Hard guard: unsolvable instances are the cost hazard -- a player
        # that won't HALT burns budget forever without this.
        message_limit=120,
    )
