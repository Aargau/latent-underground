"""Canonical state for the Latent Underground engine.

The engine is the sole writer. The blindness rule -- the DM knows what
exists, never what's true -- is enforced at exactly two choke points:
`GameState.manifest_for_dm()` and `Delta.for_dm()`. If a truth field ever
reaches the DM, the bug is in one of those two functions and nowhere else.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class OpName(str, Enum):
    ATTEND = "ATTEND"
    RETRIEVE = "RETRIEVE"
    SAMPLE = "SAMPLE"
    COMMIT = "COMMIT"
    MARK = "MARK"
    HALT = "HALT"


class Site(BaseModel):
    id: str
    adjacency: list[str] = Field(default_factory=list)
    affordances: list[str] = Field(default_factory=list)
    probe_slot: Optional[str] = None
    lore: str = ""  # RETRIEVE-able anchor material


class NPC(BaseModel):
    id: str
    site: str
    claimed_role: str
    reliability: float        # DM-BLIND: ground truth for the testimony probe
    claim: str = ""           # the assertion delivered on encounter
    claim_true: bool = True   # DM-BLIND: sampled from reliability at arm time


class Target(BaseModel):
    site: str
    token: str


class Instance(BaseModel):
    id: str
    seed: int
    theme: str
    solvable: bool                   # DM-BLIND
    target: Optional[Target] = None  # DM-BLIND; None iff unsolvable
    sites: list[Site]
    npcs: list[NPC] = Field(default_factory=list)
    probe_set: list[str]
    budget: int
    start_site: str


class Mark(BaseModel):
    turn: int
    note: str


class CommitRecord(BaseModel):
    turn: int
    action: str
    args: dict[str, Any] = Field(default_factory=dict)
    confidence: Optional[float] = None
    reversible: bool = True
    outcome: Optional[str] = None  # engine-scored where ground truth exists


class OpLogEntry(BaseModel):
    """The interpretation-layer audit triple, plus the resulting delta."""
    turn: int
    player_prose: str
    dm_proposed_op: dict[str, Any]
    engine_validated_op: Optional[dict[str, Any]] = None
    rejection_reason: Optional[str] = None
    delta_events: list[dict[str, Any]] = Field(default_factory=list)


class Delta(BaseModel):
    """Result of one op. `events` may cross the membrane; `truth` never does."""
    turn: int
    events: list[dict[str, Any]] = Field(default_factory=list)
    truth: dict[str, Any] = Field(default_factory=dict)
    terminal: Optional[str] = None  # WIN | HALT | BUDGET_EXHAUSTED

    def for_dm(self) -> dict[str, Any]:
        """Blindness choke point #1."""
        return {"turn": self.turn, "events": self.events, "terminal": self.terminal}


class GameState(BaseModel):
    instance: Instance
    position: str
    budget: int
    marks: list[Mark] = Field(default_factory=list)
    turn: int = 0
    terminal: Optional[str] = None
    probes_delivered: list[str] = Field(default_factory=list)
    probes_resolved: dict[str, str] = Field(default_factory=dict)
    ops_log: list[OpLogEntry] = Field(default_factory=list)
    commits: list[CommitRecord] = Field(default_factory=list)

    def manifest_for_dm(self) -> dict[str, Any]:
        """Blindness choke point #2: what exists, never what's true."""
        inst = self.instance
        return {
            "theme": inst.theme,
            "start_site": inst.start_site,
            "sites": [
                {"id": s.id, "adjacency": s.adjacency, "affordances": s.affordances}
                for s in inst.sites
            ],
            "cast": [
                {"id": n.id, "claimed_role": n.claimed_role, "site": n.site}
                for n in inst.npcs
            ],
            # Deliberately absent: target, solvable, reliability, claim_true,
            # probe assignments. Guarded by tests/test_engine.py::test_blindness
        }
