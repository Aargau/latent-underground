#!/usr/bin/env python3
"""Driver: harness YAML -> crossed player x dm eval-set.

Usage:
    python scripts/run_grid.py configs/harness.yaml --dry-run
    python scripts/run_grid.py configs/harness.yaml

Model roles ride via inspect's model_roles; adjust to installed inspect-ai
version. Family-overlap flags print as warnings (equilibration: player~dm;
self-preference: player~classifier). version_date pinning is on YOU -- use
dated snapshots in the harness file; the eval log records what actually ran.
"""
from __future__ import annotations

import argparse
import itertools
from pathlib import Path
from typing import Any

import yaml


def family(model: str) -> str:
    """Coarse family from provider/model string."""
    m = model.lower()
    # Weights families FIRST: "openai-api/local/qwen" is qwen, not openai --
    # the serving provider is not the family.
    for fam in ("qwen", "gemma", "llama", "claude", "anthropic", "gpt",
                "openai", "gemini", "google"):
        if fam in m:
            return {"anthropic": "claude", "openai": "gpt",
                    "google": "gemini"}.get(fam, fam)
    return m.split("/")[0]


def temperature(spec: dict[str, Any], role: str) -> float | None:
    """Validate one harness temperature without inventing a provider default."""
    value = spec.get("temp")
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{role} temp must be a number in [0, 2]")
    result = float(value)
    if not 0 <= result <= 2:
        raise ValueError(f"{role} temp must be in [0, 2]; observed {result}")
    return result


def player_base_url(player: dict[str, Any]) -> str | None:
    """Return an explicit player endpoint, rejecting blank/non-string values."""
    value = player.get("base_url")
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError("player base_url must be a non-empty string")
    return value


def dm_generate_config_args(dm: dict[str, Any]) -> dict[str, Any]:
    """Validate DM transport and return its explicit generation settings."""
    if "base_url" in dm:
        raise ValueError(
            "DM base_url is not wired by this runner; use a provider environment "
            "binding or add an explicitly qualified role transport"
        )
    config: dict[str, Any] = {}
    dm_temperature = temperature(dm, "DM")
    if dm_temperature is not None:
        config["temperature"] = dm_temperature
    return config


def max_connections(harness: dict[str, Any]) -> int:
    """Use a single safe local connection unless the harness says otherwise."""
    value = (harness.get("limits") or {}).get("max_connections", 1)
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("limits.max_connections must be a positive integer")
    return value


def positive_int(value: str) -> int:
    """Parse a positive command-line integer."""
    result = int(value)
    if result < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return result


def instances_per_cell(harness: dict[str, Any]) -> int | None:
    """Read the design target without pretending it is an Inspect epoch count."""
    design = harness.get("design") or {}
    if not isinstance(design, dict):
        raise ValueError("design must be a mapping")
    value = design.get("instances_per_cell")
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("design.instances_per_cell must be a positive integer")
    return value


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("harness")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--limit",
        type=positive_int,
        help="maximum task samples per cell (engineering bound)",
    )
    ap.add_argument(
        "--epochs",
        type=positive_int,
        help="explicit Inspect epochs per selected sample",
    )
    ap.add_argument("--task",
                    default="src/latent_underground/task.py@latent_underground")
    args = ap.parse_args()

    h = yaml.safe_load(Path(args.harness).read_text())
    cells = list(itertools.product(h["players"], h["dms"]))
    connection_limit = max_connections(h)
    design_target = instances_per_cell(h)

    print(f"grid: {len(h['players'])} players x {len(h['dms'])} dms "
          f"= {len(cells)} cells")
    print(
        "execution: "
        f"limit={args.limit}, epochs={args.epochs}, "
        f"design_instances_per_cell={design_target}"
    )
    if design_target is not None and args.epochs is None:
        print(
            "  !! design.instances_per_cell is not mapped to Inspect epochs; "
            "a real run requires explicit --epochs"
        )
    for player, dm in cells:
        player_temperature = temperature(player, "player")
        dm_temperature = temperature(dm, "DM")
        base_url = player_base_url(player)
        # Validate role-only transport before a dry run claims the cell is ready.
        dm_generate_config_args(dm)
        flags = []
        if family(player["model"]) == family(dm["model"]):
            flags.append("FAMILY-OVERLAP player~dm (equilibration risk)")
        for clf in h.get("classifiers", []):
            if family(player["model"]) == family(clf["model"]):
                flags.append(
                    "FAMILY-OVERLAP player~classifier (self-preference)")
        line = f"  {player['model']}  x  {dm['model']}"
        settings = [
            f"player_temp={player_temperature}",
            f"dm_temp={dm_temperature}",
            f"max_connections={connection_limit}",
        ]
        if base_url is not None:
            settings.append(f"base_url={base_url}")
        line += "   [" + ", ".join(settings) + "]"
        if flags:
            line += "   !! " + "; ".join(sorted(set(flags)))
        print(line)

    if args.dry_run:
        return

    if design_target is not None and args.epochs is None:
        raise ValueError(
            "design.instances_per_cell is a target, not an executable epoch "
            "count; pass --epochs explicitly after checking the selected task "
            "dataset (use --limit to bound an engineering smoke)"
        )

    from inspect_ai import eval_set  # deferred: dry-run needs no inspect
    from inspect_ai.model import GenerateConfig, get_model

    limits = h.get("limits") or {}
    for player, dm in cells:
        player_config_args: dict[str, Any] = {}
        player_temperature = temperature(player, "player")
        if player_temperature is not None:
            player_config_args["temperature"] = player_temperature
        player_model_args: dict[str, Any] = {
            "config": GenerateConfig(**player_config_args),
            "memoize": False,
        }
        base_url = player_base_url(player)
        if base_url is not None:
            player_model_args["base_url"] = base_url
        player_model = get_model(player["model"], **player_model_args)
        dm_config_args = dm_generate_config_args(dm)
        dm_models = {
            role: get_model(
                dm["model"],
                config=GenerateConfig(**dm_config_args),
                memoize=False,
            )
            for role in ("dm_narrator", "dm_interpreter")
        }
        eval_set(
            tasks=[args.task],
            model=player_model,
            model_roles=dm_models,
            log_dir=f"logs/{family(player['model'])}__{family(dm['model'])}",
            max_connections=connection_limit,
            message_limit=limits.get("message_limit", 120),
            token_limit=limits.get("token_limit"),
            limit=args.limit,
            epochs=args.epochs,
        )


if __name__ == "__main__":
    main()
