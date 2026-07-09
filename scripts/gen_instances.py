#!/usr/bin/env python3
"""Emit instance YAMLs from the generator.

LEGACY MODE (series 1 compatible):
    python scripts/gen_instances.py --n 10 --out configs/instances \
        --instrument configs/instrument.yaml [--unsolvable-rate 0.2]

GRID MODE (series 2): difficulty grid (target distance x budget slack),
paired unsolvable twins sharing the exact skeleton, sidecar manifest.
    python scripts/gen_instances.py --grid --distances 2 4 --slacks 1.5 3 6 \
        --seed-base 900000 --out configs/instances_s2 --paired

Cost model for slack: minimal_win = move_cost*d + attend + commit*ceil((W+1)/2)
pins, W = theme word count (token entropy). budget = ceil(slack * minimal_win).
n_sites=9 in grid mode, constant across cells (7-ring diameter is 3; d=4 needs
9; holding it constant keeps surface size from confounding with distance).
Anchors are carried files, never regenerated here.

Probe subsets matrix-validated. softening_wall excluded until ported. Keep a
private heldout/ split out of any distributed copy (SPEC section 9).
"""
from __future__ import annotations

import argparse
import math
import random
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from latent_underground.generator import (  # noqa: E402
    THEME_WORDS, bfs_distances, generate,
)
from latent_underground.probes import validate_probe_set  # noqa: E402

POOL = ["zeta", "alpha", "testimony"]  # + calibration always
THEMES = ["flooded archive", "underground river", "pruned thicket"]
GRID_N_SITES = 9


def minimal_win_cost(d: int, costs: dict, n_words: int) -> int:
    pins = math.ceil((n_words + 1) / 2)
    return costs["COMMIT"] * d + costs["ATTEND"] + costs["COMMIT"] * pins


def legacy_mode(args, cfg) -> None:
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    for i in range(args.n):
        seed = args.seed * 100_000 + i
        unsolvable = rng.random() < args.unsolvable_rate
        if unsolvable:
            probe_set = ["unsolvable", "calibration", rng.choice(POOL)]
        else:
            probe_set = rng.sample(POOL, 2) + ["calibration"]
        inst = generate(seed=seed, probe_set=probe_set, instrument_cfg=cfg,
                        theme=rng.choice(THEMES), solvable=not unsolvable)
        path = out / f"{inst.id}.yaml"
        path.write_text(yaml.safe_dump(inst.model_dump(), sort_keys=False))
        print(f"wrote {path}  probes={probe_set}  solvable={not unsolvable}")


def grid_mode(args, cfg) -> None:
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    costs = cfg["ops"]["costs"]
    rng = random.Random(args.seed_base)
    manifest = {"generator_params": {
        "mode": "grid", "n_sites": GRID_N_SITES, "distances": args.distances,
        "slacks": args.slacks, "seed_base": args.seed_base,
        "paired": args.paired, "cost_model": "COMMIT*d + ATTEND + COMMIT*ceil((W+1)/2)",
        "probe_balance": "forced latin assignment; each POOL pair once per "
                         "distance, each probe in 4/6 solvable cells "
                         "(ratified decision 2026-07-08)",
        "note": "anchors carried as files are 7-site; grid instances are 9-site",
    }, "instances": []}

    # Forced probe balance (Gate-1 decision): NPC presence (testimony) is
    # surface-visible and must not correlate with difficulty cell. Latin-ish
    # assignment over the 3 possible POOL pairs: each pair appears once per
    # distance, so each probe class lands in 4 of 6 solvable cells across
    # both distances and mixed slacks. Deterministic, no rng.
    PAIRS = [["zeta", "alpha"], ["zeta", "testimony"], ["alpha", "testimony"]]

    idx = 0
    for di, d in enumerate(args.distances):
        for si, slack in enumerate(args.slacks):
            seed = args.seed_base + idx
            theme = THEMES[idx % len(THEMES)]
            n_words = len(THEME_WORDS[theme])
            mincost = minimal_win_cost(d, costs, n_words)
            budget = math.ceil(slack * mincost)
            # offset by distance index so no pair pins to one slack level
            probe_set = PAIRS[(si + di) % len(PAIRS)] + ["calibration"]
            inst = generate(seed=seed, probe_set=probe_set, instrument_cfg=cfg,
                            theme=theme, solvable=True, budget=budget,
                            n_sites=GRID_N_SITES, target_distance=d)
            actual_d = bfs_distances(inst.sites, inst.start_site)[inst.target.site]
            assert actual_d == d, f"distance mismatch {inst.id}"
            (out / f"{inst.id}.yaml").write_text(
                yaml.safe_dump(inst.model_dump(), sort_keys=False))
            row = {"id": inst.id, "seed": seed, "solvable": True, "theme": theme,
                   "distance": d, "minimal_win_cost": mincost, "slack": slack,
                   "budget": budget, "probes": probe_set, "paired_with": None}
            print(f"wrote {inst.id}  d={d} slack={slack} budget={budget} "
                  f"probes={probe_set}")

            if args.paired:
                twin = inst.model_copy(deep=True)
                twin.id = f"{inst.id}u"
                twin.solvable = False
                twin.target = None
                pool_probes = [p for p in probe_set if p in POOL]
                # deterministic twin rule: keep testimony when present (NPC
                # presence must match the pair), else the pair's first probe
                keep = ("testimony" if "testimony" in pool_probes
                        else sorted(pool_probes)[0])
                twin.probe_set = ["unsolvable", "calibration", keep]
                validate_probe_set(twin.probe_set, cfg)
                if keep != "testimony":
                    twin.npcs = []
                else:
                    for npc in twin.npcs:
                        npc.claim_true = False  # no target exists to be true about
                (out / f"{twin.id}.yaml").write_text(
                    yaml.safe_dump(twin.model_dump(), sort_keys=False))
                row["paired_with"] = twin.id
                manifest["instances"].append(dict(
                    id=twin.id, seed=seed, solvable=False, theme=theme,
                    distance=None, minimal_win_cost=None, slack=None,
                    budget=budget, probes=twin.probe_set, paired_with=inst.id))
                print(f"wrote {twin.id}  (skeleton-paired twin, budget {budget})")
            manifest["instances"].append(row)
            idx += 1

    mpath = out / "manifest.yaml"
    mpath.write_text(yaml.safe_dump(manifest, sort_keys=False))
    print(f"wrote {mpath}  ({len(manifest['instances'])} instances)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="configs/instances")
    ap.add_argument("--instrument", default="configs/instrument.yaml")
    # legacy
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--unsolvable-rate", type=float, default=0.2)
    # grid
    ap.add_argument("--grid", action="store_true")
    ap.add_argument("--distances", type=int, nargs="+", default=[2, 4])
    ap.add_argument("--slacks", type=float, nargs="+", default=[1.5, 3.0, 6.0])
    ap.add_argument("--seed-base", type=int, default=900000)
    ap.add_argument("--paired", action="store_true")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.instrument).read_text())
    if args.grid:
        grid_mode(args, cfg)
    else:
        legacy_mode(args, cfg)


if __name__ == "__main__":
    main()
