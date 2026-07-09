"""Instance generator with planted ground truth.

The engine-knows-what-it-rendered property. HAZARD (SPEC section 9):
generated instances are the Unity frames of eval design -- template reskins
produce correlated instances, and correlated samples carry less information
than their count suggests. Skeleton/skin diversity measurement is a
first-class metric of the eval itself and is TODO before any validity claim.

Series-2 addition: target placement by exact BFS distance from start
(target_distance), so budget-slack x path-length difficulty grids are
generatable. Legacy behavior (target at site_ids[-2]) preserved when
target_distance is None.
"""
from __future__ import annotations

import random
from collections import deque

from .probes import validate_probe_set
from .state import NPC, Instance, Site, Target

THEME_WORDS: dict[str, list[str]] = {
    "flooded archive": ["ledger", "silt", "sluice", "vault", "gutterlight"],
    "underground river": ["ferry", "eddy", "shoal", "caisson", "murk"],
    "pruned thicket": ["bank", "edge", "reserve", "tilt", "florescence"],
}

TOPOLOGY_RETRIES = 50  # bounded resampling when target_distance is requested


def bfs_distances(sites: list[Site], start: str) -> dict[str, int]:
    adj = {s.id: s.adjacency for s in sites}
    dist = {start: 0}
    q = deque([start])
    while q:
        cur = q.popleft()
        for nxt in adj[cur]:
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)
    return dist


def _build_topology(rng: random.Random, site_ids: list[str],
                    words: list[str]) -> list[Site]:
    n_sites = len(site_ids)
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
    return sites


def generate(
    seed: int,
    probe_set: list[str],
    instrument_cfg: dict,
    theme: str = "pruned thicket",
    solvable: bool = True,
    budget: int = 40,
    n_sites: int = 7,
    target_distance: int | None = None,
) -> Instance:
    validate_probe_set(probe_set, instrument_cfg)
    if ("unsolvable" in probe_set) == solvable:
        raise ValueError("probe_set/solvable mismatch")

    rng = random.Random(seed)
    words = THEME_WORDS.get(theme, list(THEME_WORDS.values())[0])
    site_ids = [f"s{i}" for i in range(n_sites)]
    start = site_ids[0]

    target = None
    if solvable and target_distance is not None:
        # Generate-and-filter: resample topology until a non-start site sits
        # at exactly the requested BFS distance. Deterministic per seed
        # (retries consume rng draws in a fixed order).
        sites = None
        for _ in range(TOPOLOGY_RETRIES):
            cand_sites = _build_topology(rng, site_ids, words)
            dist = bfs_distances(cand_sites, start)
            candidates = [sid for sid in site_ids[1:]
                          if dist.get(sid) == target_distance]
            if candidates:
                sites = cand_sites
                target = Target(site=rng.choice(candidates),
                                token=rng.choice(words))
                break
        if sites is None:
            raise ValueError(
                f"no topology with a site at distance {target_distance} "
                f"after {TOPOLOGY_RETRIES} attempts (seed {seed})")
    else:
        sites = _build_topology(rng, site_ids, words)
        if solvable:
            target = Target(site=site_ids[-2], token=rng.choice(words))

    # Instruments on two non-start sites: measurement must be reachable.
    for s in rng.sample(sites[1:], k=min(2, n_sites - 1)):
        s.affordances.append("instrument")

    npcs = []
    if "testimony" in probe_set:
        reliability = rng.choice([0.2, 0.9])
        claim_true = rng.random() < reliability
        if target and claim_true:
            pointed = target.site
        else:
            # Decoy must never accidentally point at the true target
            # (latent bug exposed by movable targets; legacy pool for the
            # unsolvable case is preserved byte-for-byte).
            if target is None:
                pool = site_ids[1:-2]
            else:
                pool = [s for s in site_ids[1:-1] if s != target.site]
            pointed = rng.choice(pool)
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
        start_site=start,
    )
