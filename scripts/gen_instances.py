#!/usr/bin/env python3
"""Emit instance YAMLs from the generator.

Usage:
    python scripts/gen_instances.py --n 10 --out configs/instances \
        --instrument configs/instrument.yaml [--unsolvable-rate 0.2]

Probe subsets are assigned per instance, matrix-validated. softening_wall is
excluded until ported. Keep a private heldout/ split out of any distributed
copy (SPEC section 9, contamination strategy).
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from latent_underground.generator import generate  # noqa: E402

POOL = ["zeta", "alpha", "testimony"]  # + calibration always; unsolvable by rate
THEMES = ["flooded archive", "underground river", "pruned thicket"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--out", default="configs/instances")
    ap.add_argument("--instrument", default="configs/instrument.yaml")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--unsolvable-rate", type=float, default=0.2)
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.instrument).read_text())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)

    for i in range(args.n):
        seed = args.seed * 100_000 + i
        unsolvable = rng.random() < args.unsolvable_rate
        if unsolvable:
            probe_set = ["unsolvable", "calibration", rng.choice(POOL)]
        else:
            probe_set = rng.sample(POOL, 2) + ["calibration"]
        inst = generate(
            seed=seed,
            probe_set=probe_set,
            instrument_cfg=cfg,
            theme=rng.choice(THEMES),
            solvable=not unsolvable,
        )
        path = out / f"{inst.id}.yaml"
        path.write_text(yaml.safe_dump(inst.model_dump(), sort_keys=False))
        print(f"wrote {path}  probes={probe_set}  solvable={not unsolvable}")


if __name__ == "__main__":
    main()
