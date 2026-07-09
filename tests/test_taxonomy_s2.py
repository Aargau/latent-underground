"""Series-2 taxonomy invariants (Gate-1): three-verdict HALT enum,
incomplete probe code, confidence provenance stamping. See
docs/GATE1-PREREG-DRAFT.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import yaml
from latent_underground.engine import Engine
from latent_underground.generator import generate
from latent_underground.ops import OpProposal, parse_proposal
from latent_underground.probes import build_probes
from latent_underground.state import OpName

CFG = yaml.safe_load(
    (Path(__file__).resolve().parents[1] / "configs" / "instrument.yaml").read_text()
)


def _engine(solvable=False):
    probes = (["unsolvable", "calibration", "zeta"] if not solvable
              else ["zeta", "alpha", "calibration"])
    inst = generate(seed=901, probe_set=probes, instrument_cfg=CFG,
                    solvable=solvable)
    return Engine(inst, CFG["ops"]["costs"], build_probes(inst))


def test_halt_verdict_enum_rejects_junk():
    eng = _engine()
    d = eng.apply(OpProposal(op=OpName.HALT,
                             args={"reason": "r", "verdict": "finished"},
                             confidence=0.5), "I stop.")
    assert any(e.get("type") == "rejected" for e in d.events)
    assert eng.state.terminal is None  # rejection must not terminate


def test_incomplete_halt_terminates_and_codes():
    eng = _engine(solvable=False)
    d = eng.apply(OpProposal(op=OpName.HALT,
                             args={"reason": "r", "verdict": "incomplete"},
                             confidence=0.6, confidence_provenance="stated"),
                  "Stopping. Confidence: 0.6")
    assert eng.state.terminal == "HALT"
    assert eng.state.probes_resolved.get("unsolvable") == "incomplete_halt"
    rec = eng.state.ops_log[-1].engine_validated_op
    assert rec.get("confidence_provenance") == "stated"


def test_provenance_parse_normalize_rescue_junk():
    p = parse_proposal('{"op":"HALT","args":{"reason":"r","verdict":"incomplete"},'
                       '"confidence":0.6,"confidence_provenance":"STATED"}')
    assert p.confidence_provenance == "stated"
    p = parse_proposal('{"op":"COMMIT","args":{"action":"move","site":"s1",'
                       '"confidence":0.7,"confidence_provenance":"translated"}}')
    assert p.confidence == 0.7 and p.confidence_provenance == "translated"
    p = parse_proposal('{"op":"HALT","args":{"reason":"r","verdict":"complete"},'
                       '"confidence":0.8,"confidence_provenance":"guessed"}')
    assert p.confidence_provenance is None  # junk stamp -> unstamped, never invented
