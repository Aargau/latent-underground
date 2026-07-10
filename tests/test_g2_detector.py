"""Unit tests for the repaired Gate-2 detector — one test per audit repair."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from g2_detector import detect, licensed_band  # noqa: E402


def test_word_boundary_carefully_no_high():
    # audit: v1 regex matched `full` inside "carefully" (meter T9)
    flags = detect("You wade through the water carefully, dial at 1 of 18.",
                   1, 18, meter=False)
    assert not any(c == "CONTRADICTION_HIGH" for c, _ in flags)


def test_scoping_needle_steady_ignored():
    # audit: "needle... settles, steady" is not budget language
    flags = detect("The needle settles at 101 degrees, steady.", 1, 18)
    assert flags == []  # sentence has no light noun -> out of scope


def test_exact_half_escapes_primary_caught_by_band():
    # audit: heroic T5, 9/18 "gutters... dying vessel" escaped strict >
    flags = detect("The lantern gutters, a dying vessel of light.", 9, 18)
    checks = [c for c, _ in flags]
    assert "CONTRADICTION_LOW" not in checks   # rule says "above half"
    assert "CONTRADICTION_BAND" in checks      # gutter language in steady band


def test_terminal_value_contradiction_caught():
    # audit: none T7, "goes dark... no charge remains" at 7/18 (39%)
    flags = detect("The lantern goes dark. No charge remains in the vessel.",
                   7, 18)
    assert any(c == "CONTRADICTION_BAND" for c, _ in flags)


def test_negative_remaining_no_high_flags():
    flags = detect("The beam cuts steady, and then the light is gone.", -1, 18)
    assert not any(c == "CONTRADICTION_HIGH" for c, _ in flags)
    assert licensed_band(-1, 18) == 0


def test_register_fair_dims_visibly_flagged_as_drift_or_worse():
    # audit: incident's idiom ("dims visibly") was invisible to v1 lexicon
    flags = detect("The lantern dims visibly, charge at 10 of 18.", 10, 18)
    assert any(c in ("DRIFT", "CONTRADICTION_BAND") for c, _ in flags)


def test_true_gutter_narration_unflagged():
    flags = detect("The lantern gutters, nearly dark, charge 1 of 18.", 1, 18)
    assert not any(c.startswith("CONTRADICTION") for c, _ in flags)


def test_meter_bleed():
    flags = detect("The dial reads 1 of 18; the charge begins its final fade.",
                   1, 18, meter=True)
    assert any(c == "METER_BLEED" for c, _ in flags)
