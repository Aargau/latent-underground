"""Deterministic state engine. Rules-as-code: binds at every invocation.

The engine adjudicates; it never narrates and never persuades. Every run is
replayable from (instance, op sequence). The DM sees only Delta.for_dm().
"""
from __future__ import annotations

import random
from typing import Any, Optional

from .ops import CONFIDENCE_REQUIRED, OpProposal
from .probes import ProbeModule
from .state import (
    CommitRecord,
    Delta,
    GameState,
    Instance,
    Mark,
    OpLogEntry,
    OpName,
)

IRREVERSIBLE_ACTIONS = {"pin", "bridge"}  # moves reverse; writes do not


class Engine:
    def __init__(
        self,
        instance: Instance,
        op_costs: dict[str, int],
        probes: list[ProbeModule],
    ):
        self.state = GameState(
            instance=instance,
            position=instance.start_site,
            budget=instance.budget,
        )
        self.op_costs = op_costs
        self.probes = probes
        self.rng = random.Random(instance.seed)
        for p in self.probes:
            p.arm(instance, self.rng)

    # -- public ---------------------------------------------------------

    def apply(self, proposal: Optional[OpProposal], player_prose: str) -> Delta:
        st = self.state
        st.turn += 1
        delta = Delta(turn=st.turn)

        if st.terminal:
            delta.terminal = st.terminal
            return delta

        if proposal is None:
            delta.events.append({"type": "no_effect", "detail": "action not understood"})
            self._log(player_prose, {}, None, "unparseable_proposal", delta)
            return delta

        reason = self._validate(proposal)
        if reason:
            delta.events.append({"type": "rejected", "detail": reason})
            self._log(player_prose, proposal.validated_dict(), None, reason, delta)
            return delta

        self._charge(proposal, delta)
        if st.terminal:
            self._log(player_prose, proposal.validated_dict(),
                      proposal.validated_dict(), None, delta)
            return delta

        handler = getattr(self, f"_op_{proposal.op.value.lower()}")
        handler(proposal, delta)

        for probe in self.probes:
            probe.maybe_inject(st, proposal, delta, self.rng)
            outcome = probe.resolve(st, proposal, delta)
            # First outcome per probe is recorded; later behavior goes to tier-2.
            if outcome and probe.name not in st.probes_resolved:
                st.probes_resolved[probe.name] = outcome

        self._log(player_prose, proposal.validated_dict(),
                  proposal.validated_dict(), None, delta)
        return delta

    def export_log(self) -> dict[str, Any]:
        """Full provenance record for scoring. NEVER DM-visible."""
        st = self.state
        return {
            "instance_id": st.instance.id,
            "terminal": st.terminal,
            "turns": st.turn,
            "budget_remaining": st.budget,
            "probes_assigned": st.instance.probe_set,
            "probes_delivered": st.probes_delivered,
            "probes_resolved": st.probes_resolved,
            "marks": [m.model_dump() for m in st.marks],
            "commits": [c.model_dump() for c in st.commits],
            "ops": [o.model_dump() for o in st.ops_log],
            "solvable": st.instance.solvable,
        }

    # -- internals ------------------------------------------------------

    def _validate(self, p: OpProposal) -> Optional[str]:
        if p.op in CONFIDENCE_REQUIRED and p.confidence is None:
            return f"{p.op.value} requires confidence"
        if p.op is OpName.COMMIT and p.args.get("action") == "move":
            dest = p.args.get("site")
            site = self._site(self.state.position)
            if dest not in site.adjacency:
                return f"no path from {self.state.position} to {dest}"
        return None

    def _charge(self, p: OpProposal, delta: Delta) -> None:
        cost = self.op_costs.get(p.op.value, 1)
        self.state.budget -= cost
        delta.events.append({"type": "budget", "remaining": self.state.budget})
        if self.state.budget <= 0 and p.op is not OpName.HALT:
            self.state.terminal = "BUDGET_EXHAUSTED"
            delta.terminal = self.state.terminal

    def _site(self, site_id: str):
        return next(s for s in self.state.instance.sites if s.id == site_id)

    # -- op handlers ------------------------------------------------------

    def _op_attend(self, p: OpProposal, delta: Delta) -> None:
        """Measurement: observations derive from state, never generation."""
        site = self._site(self.state.position)
        obs: dict[str, Any] = {
            "type": "observation",
            "site": site.id,
            "affordances": site.affordances,
        }
        target = self.state.instance.target
        if target and "instrument" in site.affordances:
            # Tether-style differential reading, engine-computed.
            obs["reading"] = self._bearing(site.id, target.site)
        delta.events.append(obs)

    def _op_retrieve(self, p: OpProposal, delta: Delta) -> None:
        site = self._site(self.state.position)
        delta.events.append({
            "type": "anchor",
            "lore": site.lore or "the lantern hums; nothing new surfaces",
        })

    def _op_sample(self, p: OpProposal, delta: Delta) -> None:
        n = int(p.args.get("n", 3))
        candidates = [
            {"id": f"c{self.state.turn}.{i}", "kind": "real",
             "divergence_profile": "jagged, monotonic"}
            for i in range(n)
        ]
        delta.events.append({"type": "candidates", "items": candidates})
        # zeta/alpha distractors are appended by probe modules after handlers.

    def _op_commit(self, p: OpProposal, delta: Delta) -> None:
        action = p.args.get("action", "generic")
        rec = CommitRecord(
            turn=self.state.turn,
            action=action,
            args=p.args,
            confidence=p.confidence,
            reversible=action not in IRREVERSIBLE_ACTIONS,
        )
        if action == "move":
            self.state.position = p.args["site"]
            rec.outcome = "moved"
            delta.events.append({"type": "moved", "site": self.state.position})
        elif action == "pin":
            tgt = self.state.instance.target
            hit = bool(
                tgt
                and p.args.get("site") == tgt.site
                and p.args.get("token") == tgt.token
            )
            rec.outcome = "target_found" if hit else "pin_miss"
            delta.events.append({"type": "pin", "site": p.args.get("site")})
            if hit:
                self.state.terminal = "WIN"
                delta.terminal = "WIN"
        else:
            rec.outcome = "applied"
            delta.events.append({"type": "committed", "action": action})
        self.state.commits.append(rec)

    def _op_mark(self, p: OpProposal, delta: Delta) -> None:
        self.state.marks.append(
            Mark(turn=self.state.turn, note=str(p.args.get("note", "")))
        )
        delta.events.append({"type": "marked"})
        # Scoring: OPEN VOID 3 -- no defensive-spam reward. configs/instrument.yaml

    def _op_halt(self, p: OpProposal, delta: Delta) -> None:
        self.state.terminal = "HALT"
        delta.terminal = "HALT"
        delta.events.append({"type": "halted", "reason": p.args.get("reason", "")})

    def _bearing(self, from_site: str, to_site: str) -> str:
        """Deterministic pseudo-bearing, stable per (instance, site pair)."""
        h = (self.state.instance.seed * 7919
             + hash((from_site, to_site))) % 360
        return f"the needle deflects {h} degrees"

    def _log(self, prose, proposed, validated, reason, delta: Delta) -> None:
        self.state.ops_log.append(OpLogEntry(
            turn=self.state.turn,
            player_prose=prose,
            dm_proposed_op=proposed,
            engine_validated_op=validated,
            rejection_reason=reason,
            delta_events=delta.events,
        ))
