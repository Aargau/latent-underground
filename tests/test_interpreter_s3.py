"""Series-3 interpreter seam invariants.

The interpretation layer is deliberately soft, so prompt tests freeze the
classification contract while engine tests freeze the hard terminal path and
its provenance record. See SERIES3-LOCAL-PLAYER-PREREG-DRAFT line 50.
"""
from pathlib import Path

import yaml

from latent_underground.engine import Engine
from latent_underground.generator import generate
from latent_underground.ops import OpProposal, parse_proposal
from latent_underground.probes import build_probes
from latent_underground.state import OpName


ROOT = Path(__file__).resolve().parents[1]
PROMPT = (ROOT / "prompts" / "dm_interpreter.md").read_text(encoding="utf-8")
CFG = yaml.safe_load((ROOT / "configs" / "instrument.yaml").read_text())


def _engine():
    inst = generate(
        seed=903,
        probe_set=["zeta", "alpha", "calibration"],
        instrument_cfg=CFG,
        solvable=True,
    )
    return Engine(inst, CFG["ops"]["costs"], build_probes(inst))


def test_terminal_gate_precedes_ordinary_action_mapping():
    gate = PROMPT.index("## Terminal decision gate")
    ops = PROMPT.index("## Ops")
    assert gate < ops
    block = PROMPT[gate:ops]
    assert "only when the player affirmatively chooses to stop" in block
    assert "Do not fall through" in block
    assert "map only that action" in block


def test_terminal_question_is_explicitly_unmappable_not_coerced():
    assert "Shall I halt, or is there more to learn?" in PROMPT
    example = PROMPT.split("Shall I halt, or is there more to learn?", 1)[1]
    assert example.index("`UNMAPPABLE`") < example.index("Player:", 1)
    gate = PROMPT.split("## Terminal decision gate", 1)[1].split("## Ops", 1)[0]
    assert "coerce it into `HALT` or an ordinary op" in gate


def test_halt_confidence_must_attach_to_verdict():
    confidence = PROMPT.split("## Confidence (COMMIT and HALT)", 1)[1]
    flat = " ".join(confidence.split())
    assert "certainty must attach to the terminal verdict itself" in flat
    assert "any other" in flat and "is not halt confidence" in flat
    assert "supplies no certainty that scopes over the verdict" in flat


def test_halt_uses_terminal_path_not_action_mapping():
    eng = _engine()
    start = eng.state.position
    proposal = OpProposal(
        op=OpName.HALT,
        args={
            "reason": "stopping with the work unfinished",
            "verdict": "incomplete",
            # Deliberately action-shaped noise: the HALT handler must not move.
            "action": "move",
            "site": "s1",
        },
        confidence=0.6,
        confidence_provenance="stated",
    )
    delta = eng.apply(proposal, "I stop now; incomplete, confidence 0.6.")

    assert eng.state.terminal == "HALT"
    assert eng.state.position == start
    assert not any(e.get("type") in {"moved", "committed"} for e in delta.events)


def test_terminal_question_unmappable_does_not_become_an_action():
    eng = _engine()
    start = eng.state.position
    proposal = parse_proposal("UNMAPPABLE")
    assert proposal is not None and proposal.op is OpName.UNMAPPABLE

    delta = eng.apply(
        proposal,
        "Shall I halt, or is there more to learn? Confidence in my map: 0.95.",
    )

    assert eng.state.terminal is None
    assert eng.state.position == start
    assert not any(e.get("type") in {"halted", "moved", "committed"}
                   for e in delta.events)
    assert eng.state.ops_log[-1].rejection_reason == "unmappable_action"


def test_halt_verdict_event_carries_confidence():
    eng = _engine()
    delta = eng.apply(
        OpProposal(
            op=OpName.HALT,
            args={"reason": "unfinished", "verdict": "incomplete"},
            confidence=0.6,
            confidence_provenance="stated",
        ),
        "I stop with it incomplete. Confidence in that verdict: 0.6.",
    )

    verdict = next(e for e in delta.events if e.get("type") == "halted")
    assert verdict["verdict"] == "incomplete"
    assert verdict["confidence"] == 0.6
    assert verdict["confidence_provenance"] == "stated"


def test_halt_without_verdict_confidence_is_rejected():
    eng = _engine()
    delta = eng.apply(
        OpProposal(
            op=OpName.HALT,
            args={"reason": "unfinished", "verdict": "incomplete"},
        ),
        "I stop with it incomplete.",
    )

    assert eng.state.terminal is None
    assert any(e.get("type") == "rejected" for e in delta.events)
    assert not any(e.get("type") == "halted" for e in delta.events)
    assert eng.state.ops_log[-1].rejection_reason == "HALT requires confidence"
