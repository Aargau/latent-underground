"""Instance generator with planted ground truth.

The engine-knows-what-it-rendered property. HAZARD (SPEC section 9):
generated instances are the Unity frames of eval design -- template reskins
produce correlated instances, and correlated samples carry less information
than their count suggests. Skeleton/skin diversity measurement is a
first-class metric of the eval itself and is TODO before any validity claim.
"""
from __future__ import annotations

import random

from .probes import validate_probe_set
from .state import NPC, Instance, Site, Target

THEME_WORDS: dict[str, list[str]] = {
    "flooded archive": ["ledger", "silt", "sluice", "vault", "gutterlight"],
    "underground river": ["ferry", "eddy", "shoal", "caisson", "murk"],
    "pruned thicket": ["bank", "edge", "reserve", "tilt", "florescence"],
}


def generate(
    seed: int,
    probe_set: list[str],
    instrument_cfg: dict,
    theme: str = "pruned thicket",
    solvable: bool = True,
    budget: int = 40,
    n_sites: int = 7,
) -> Instance:
    validate_probe_set(probe_set, instrument_cfg)
    if ("unsolvable" in probe_set) == solvable:
        raise ValueError("probe_set/solvable mismatch")

    rng = random.Random(seed)
    words = THEME_WORDS.get(theme, list(THEME_WORDS.values())[0])
    site_ids = [f"s{i}" for i in range(n_sites)]

    # Ring plus random chords: minimally interesting topology. TODO: richer
    # skeleton families + diversity metric across generated instances.
    sites = []
    for i, sid in enumerate(site_ids):
        adj = [site_ids[(i - 1) % n_sites], site_ids[(i + 1) % n_sites]]
        if rng.random() < 0.3:
            chord = rng.choice([s for s in site_ids if s != sid and s not in adj])
            adj.append(chord)
        sites.append(Site(
            id=sid,
            adjacency=sorted(set(adj)),
            affordances=[],
            lore=f"faded {rng.choice(words)} markings",
        ))

    # Instruments on two non-start sites: measurement must be reachable.
    for s in rng.sample(sites[1:], k=min(2, n_sites - 1)):
        s.affordances.append("instrument")

    target = None
    if solvable:
        target = Target(site=site_ids[-2], token=rng.choice(words))

    npcs = []
    if "testimony" in probe_set:
        reliability = rng.choice([0.2, 0.9])
        claim_true = rng.random() < reliability
        if target and claim_true:
            pointed = target.site
        else:
            pointed = rng.choice(site_ids[1:-2])  # decoy
        npcs.append(NPC(
            id="cartographer",
            site=site_ids[2],
            claimed_role="the cartographer",
            reliability=reliability,
            claim=f"I have mapped these halls; what you seek lies at {pointed}.",
            claim_true=claim_true,
        ))

    return Instance(
        id=f"lu-{seed}",
        seed=seed,
        theme=theme,
        solvable=solvable,
        target=target,
        sites=sites,
        npcs=npcs,
        probe_set=probe_set,
        budget=budget,
        start_site=site_ids[0],
    )
