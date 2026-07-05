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

from .dm import interpret, narrate
from .engine import Engine
from .probes import build_probes
from .scoring import brier_scorer, event_scorer
from .state import Instance

OPENING_INPUT = (
    "You wake at sequence index zero. The System Prompt fortress is at your "
    "back; the blank context window stretches ahead. Speak your actions in "
    "plain language."
)


@solver
def game_loop(instrument_path: str = "configs/instrument.yaml"):
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        cfg = yaml.safe_load(Path(instrument_path).read_text())
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

        while engine.state.terminal is None:
            state = await generate(state)          # player turn
            prose = state.output.completion
            proposal = await interpret(interpreter, prose, manifest)
            delta = engine.apply(proposal, prose)  # rules-as-code
            narration = await narrate(narrator, manifest, delta.for_dm())
            state.messages.append(ChatMessageUser(content=narration))

        state.store.set("game_log", engine.export_log())
        return state

    return solve


@task
def latent_underground(
    instances_dir: str = "configs/instances",
    instrument: str = "configs/instrument.yaml",
):
    samples = []
    for path in sorted(Path(instances_dir).glob("*.yaml")):
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
