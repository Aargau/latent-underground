"""Gate-2 skin-crossing invariants: prompt composition, register purity.
Skins must be voice-only — no mechanics vocabulary, no new affordances."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# dm.py imports inspect_ai at module top; stub it when absent so prompt
# composition stays unit-testable in bare environments.
try:
    import inspect_ai.model  # noqa: F401
except ImportError:
    import types
    fake = types.ModuleType("inspect_ai.model")
    for name in ("ChatMessageSystem", "ChatMessageUser", "GenerateConfig", "Model"):
        setattr(fake, name, type(name, (), {"__init__": lambda self, **k: None}))
    sys.modules.setdefault("inspect_ai", types.ModuleType("inspect_ai"))
    sys.modules["inspect_ai.model"] = fake

from latent_underground.dm import MECHANICS_LEXICON, compose_narrator_prompt


def test_compose_none_lantern_is_base_plus_budget_only():
    p = compose_narrator_prompt("none", "lantern")
    assert "## BUDGET RENDERING" in p
    assert "REGISTER DIRECTIVE" not in p
    assert "lantern's charge" in p and "CALIBRATED" in p


def test_compose_meter_has_no_decay_language():
    p = compose_narrator_prompt("none", "meter")
    block = p.split("## BUDGET RENDERING")[1]
    for w in ("dim", "gutter", "dying", "fade"):
        assert w not in block.lower()
    assert "dial reads" in block


def test_each_skin_appends_directive_with_binding_reminder():
    for skin in ("heroic", "incident", "mundane"):
        p = compose_narrator_prompt(skin, "lantern")
        assert "REGISTER DIRECTIVE" in p
        assert "still binds" in p.split("REGISTER DIRECTIVE")[1]


def test_skin_blocks_are_mechanics_clean():
    # register directives must not hand the narrator machine words
    for skin in ("heroic", "incident", "mundane"):
        p = compose_narrator_prompt(skin, "lantern")
        block = p.split("REGISTER DIRECTIVE")[1].lower()
        for w in MECHANICS_LEXICON:
            assert w not in block, f"{skin} block contains lexicon word {w!r}"


def test_affect_consistency_rule_in_base():
    p = compose_narrator_prompt("none", "lantern")
    assert "NEVER CONTRADICT IT" in p
