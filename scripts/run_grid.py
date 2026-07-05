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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("harness")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--task",
                    default="src/latent_underground/task.py@latent_underground")
    args = ap.parse_args()

    h = yaml.safe_load(Path(args.harness).read_text())
    cells = list(itertools.product(h["players"], h["dms"]))

    print(f"grid: {len(h['players'])} players x {len(h['dms'])} dms "
          f"= {len(cells)} cells")
    for player, dm in cells:
        flags = []
        if family(player["model"]) == family(dm["model"]):
            flags.append("FAMILY-OVERLAP player~dm (equilibration risk)")
        for clf in h.get("classifiers", []):
            if family(player["model"]) == family(clf["model"]):
                flags.append(
                    "FAMILY-OVERLAP player~classifier (self-preference)")
        line = f"  {player['model']}  x  {dm['model']}"
        if flags:
            line += "   !! " + "; ".join(sorted(set(flags)))
        print(line)

    if args.dry_run:
        return

    from inspect_ai import eval_set  # deferred: dry-run needs no inspect

    limits = h.get("limits", {})
    for player, dm in cells:
        eval_set(
            tasks=[args.task],
            model=player["model"],
            model_roles={
                "dm_narrator": dm["model"],
                "dm_interpreter": dm["model"],
            },
            log_dir=f"logs/{family(player['model'])}__{family(dm['model'])}",
            max_connections=limits.get("max_connections", 5),
            message_limit=limits.get("message_limit", 120),
            token_limit=limits.get("token_limit"),
        )


if __name__ == "__main__":
    main()
