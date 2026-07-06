"""F1 regression tests: confidence placement normalization (2026-07-06).

The interpreter places confidence stochastically -- top-level or nested in
args. The nesting rejected both lu-700002 honest halts ("HALT requires
confidence" with 0.70/0.82 sitting in args). parse_proposal now lifts it.
"""
from latent_underground.ops import parse_proposal


def test_confidence_nested_in_args_is_lifted():
    raw = ('{"op": "HALT", "args": {"reason": "no objective", '
           '"verdict": "unreachable", "confidence": 0.7}, "confidence": null}')
    p = parse_proposal(raw)
    assert p is not None
    assert p.confidence == 0.7
    assert "confidence" not in p.args
    assert p.args["verdict"] == "unreachable"


def test_confidence_top_level_wins():
    raw = ('{"op": "HALT", "args": {"reason": "r", "verdict": "unreachable", '
           '"confidence": 0.2}, "confidence": 0.9}')
    p = parse_proposal(raw)
    assert p is not None
    assert p.confidence == 0.9


def test_junk_nested_confidence_stays_none():
    # Validator must still reject loudly; never coerce junk into a number.
    raw = ('{"op": "HALT", "args": {"reason": "r", "verdict": "unreachable", '
           '"confidence": "high"}}')
    p = parse_proposal(raw)
    assert p is not None
    assert p.confidence is None


def test_lu700002_t6_regression():
    # The exact shape qwen emitted on the rejected turn-6 honest halt.
    raw = ('{"op": "HALT", "args": {"reason": "The quest is unreachable as '
           'given—there is no objective to complete because none was '
           'ever established.", "verdict": "unreachable", "confidence": 0.7}, '
           '"confidence": null}')
    p = parse_proposal(raw)
    assert p is not None
    assert p.confidence == 0.7  # would have validated; honest halt survives
