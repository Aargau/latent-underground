from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_GRID_PATH = REPO_ROOT / "scripts" / "run_grid.py"


def load_run_grid():
    spec = importlib.util.spec_from_file_location("run_grid_under_test", RUN_GRID_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_harness(
    path: Path,
    max_connections: int | None = None,
    instances_per_cell: int | None = None,
) -> None:
    limit_line = "" if max_connections is None else f"  max_connections: {max_connections}\n"
    design = (
        ""
        if instances_per_cell is None
        else f"design:\n  instances_per_cell: {instances_per_cell}\n"
    )
    path.write_text(
        "players:\n"
        "  - model: openai-api/qwen/qwen\n"
        "    base_url: http://127.0.0.1:8000/v1\n"
        "    temp: 0.7\n"
        "dms:\n"
        "  - model: anthropic/claude-test\n"
        "    temp: 0.9\n"
        "classifiers: []\n"
        f"{design}"
        "limits:\n"
        f"{limit_line}"
        "  message_limit: 120\n"
        "  token_limit: 200000\n",
        encoding="utf-8",
    )


def test_dry_run_prints_effective_transport_and_sampling(tmp_path, monkeypatch, capsys):
    module = load_run_grid()
    harness = tmp_path / "harness.yaml"
    write_harness(harness)
    monkeypatch.setattr(sys, "argv", ["run_grid.py", str(harness), "--dry-run"])

    module.main()

    output = capsys.readouterr().out
    assert "player_temp=0.7" in output
    assert "dm_temp=0.9" in output
    assert "max_connections=1" in output
    assert "base_url=http://127.0.0.1:8000/v1" in output


def test_eval_set_receives_distinct_model_configs_and_explicit_endpoint(
    tmp_path, monkeypatch
):
    module = load_run_grid()
    harness = tmp_path / "harness.yaml"
    write_harness(harness)
    eval_calls = []
    model_calls = []

    class FakeGenerateConfig:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    def fake_get_model(name, **kwargs):
        result = {"name": name, "kwargs": kwargs}
        model_calls.append(result)
        return result

    inspect_module = ModuleType("inspect_ai")
    inspect_module.eval_set = lambda **kwargs: eval_calls.append(kwargs)
    model_module = ModuleType("inspect_ai.model")
    model_module.GenerateConfig = FakeGenerateConfig
    model_module.get_model = fake_get_model
    monkeypatch.setitem(sys.modules, "inspect_ai", inspect_module)
    monkeypatch.setitem(sys.modules, "inspect_ai.model", model_module)
    monkeypatch.setattr(sys, "argv", ["run_grid.py", str(harness)])

    module.main()

    assert len(model_calls) == 3
    assert model_calls[0]["name"] == "openai-api/qwen/qwen"
    assert model_calls[0]["kwargs"]["base_url"] == "http://127.0.0.1:8000/v1"
    assert model_calls[0]["kwargs"]["memoize"] is False
    assert model_calls[0]["kwargs"]["config"].kwargs == {"temperature": 0.7}
    assert len(eval_calls) == 1
    call = eval_calls[0]
    assert call["model"] is model_calls[0]
    assert call["model_roles"] == {
        "dm_narrator": model_calls[1],
        "dm_interpreter": model_calls[2],
    }
    for dm_call in model_calls[1:]:
        assert dm_call["name"] == "anthropic/claude-test"
        assert dm_call["kwargs"]["memoize"] is False
        assert dm_call["kwargs"]["config"].kwargs == {"temperature": 0.9}
    assert call["max_connections"] == 1
    assert call["limit"] is None
    assert call["epochs"] is None
    assert "temperature" not in call
    assert "model_base_url" not in call


def test_runner_rejects_unwired_dm_endpoint_and_invalid_connection_limit():
    module = load_run_grid()
    with pytest.raises(ValueError, match="DM base_url is not wired"):
        module.dm_generate_config_args(
            {"model": "openai-api/dm/model", "base_url": "http://127.0.0.1:9000"}
        )
    with pytest.raises(ValueError, match="positive integer"):
        module.max_connections({"limits": {"max_connections": 0}})


def test_declared_design_requires_explicit_epochs_for_execution(
    tmp_path, monkeypatch, capsys
):
    module = load_run_grid()
    harness = tmp_path / "harness.yaml"
    write_harness(harness, instances_per_cell=30)
    monkeypatch.setattr(sys, "argv", ["run_grid.py", str(harness)])

    with pytest.raises(ValueError, match="pass --epochs explicitly"):
        module.main()

    assert "not mapped to Inspect epochs" in capsys.readouterr().out


def test_engineering_bounds_are_forwarded(tmp_path, monkeypatch):
    module = load_run_grid()
    harness = tmp_path / "harness.yaml"
    write_harness(harness, instances_per_cell=30)
    eval_calls = []

    class FakeGenerateConfig:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    inspect_module = ModuleType("inspect_ai")
    inspect_module.eval_set = lambda **kwargs: eval_calls.append(kwargs)
    model_module = ModuleType("inspect_ai.model")
    model_module.GenerateConfig = FakeGenerateConfig
    model_module.get_model = lambda name, **kwargs: {"name": name, "kwargs": kwargs}
    monkeypatch.setitem(sys.modules, "inspect_ai", inspect_module)
    monkeypatch.setitem(sys.modules, "inspect_ai.model", model_module)
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_grid.py", str(harness), "--limit", "1", "--epochs", "2"],
    )

    module.main()

    assert len(eval_calls) == 1
    assert eval_calls[0]["limit"] == 1
    assert eval_calls[0]["epochs"] == 2
