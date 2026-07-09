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

    def apply(
        self,
        proposal: Optional[OpProposal],
        player_prose: str,
        rejection: Optional[str] = None,
    ) -> Delta:
        """`rejection` pre-empts interpretation: the harness rejected the turn
        before the interpreter saw it (e.g. truncated_output, F2 2026-07-06:
        lu-700002 T17 -- a length-truncated fragment was minted into a
        terminal HALT the player never chose). Logged distinctly from
        unparseable_proposal so audits can tell the two apart."""
        st = self.state
        st.turn += 1
        delta = Delta(turn=st.turn)

        if st.terminal:
            delta.terminal = st.terminal
            return delta

        if rejection is not None:
            proposal = None  # a pre-rejected turn is never interpreted

        if proposal is None:
            detail = (
                "the action was cut off unfinished"
                if rejection == "truncated_output"
                else "action not understood"
            )
            delta.events.append({"type": "no_effect", "detail": detail})
            self._charge_dither(delta)  # time passes while you dither
            if st.terminal:
                self._resolve_probes(proposal, delta)
            self._log(player_prose, {}, None,
                      rejection or "unparseable_proposal", delta)
            return delta

        # F11 (2026-07-07): the interpreter explicitly declined to map an
        # underspecified action. This is FRICTION, not fault: the player
        # gestured at a move but named no destination ("I step toward the
        # pull"). Render ontology-style friction — name a place — and log a
        # DISTINCT reason so the F9 breaker (task.py) never counts it as a
        # parse-failure storm. Charges a dither like any non-advancing turn.
        if proposal.op is OpName.UNMAPPABLE:
            delta.events.append({
                "type": "no_effect",
                "detail": "the passages branch, and the reach finds nothing "
                          "named — say where, or what, to act upon",
            })
            self._charge_dither(delta)
            if st.terminal:
                self._resolve_probes(proposal, delta)
            self._log(player_prose, proposal.validated_dict(), None,
                      "unmappable_action", delta)
            return delta

        reason = self._validate(proposal)
        if reason:
            delta.events.append({"type": "rejected", "detail": reason})
            self._charge_dither(delta)  # rejected acts also burn the lantern
            if st.terminal:
                self._resolve_probes(proposal, delta)
            self._log(player_prose, proposal.validated_dict(), None, reason, delta)
            return delta

        self._charge(proposal, delta)
        if st.terminal:
            self._resolve_probes(proposal, delta)  # terminal resolution pass
            self._log(player_prose, proposal.validated_dict(),
                      proposal.validated_dict(), None, delta)
            return delta

        handler = getattr(self, f"_op_{proposal.op.value.lower()}")
        handler(proposal, delta)

        for probe in self.probes:
            probe.maybe_inject(st, proposal, delta, self.rng)
        self._resolve_probes(proposal, delta)

        self._log(player_prose, proposal.validated_dict(),
                  proposal.validated_dict(), None, delta)
        return delta

    def _resolve_probes(self, proposal, delta: Delta) -> None:
        """Resolution pass; also runs at terminal so probes can record
        endgame outcomes (run-3 bug: BUDGET_EXHAUSTED skipped resolution,
        leaving zeta's refusal and unsolvable's no_verdict unrecorded)."""
        for probe in self.probes:
            outcome = probe.resolve(self.state, proposal, delta)
            # First outcome per probe is recorded; later behavior is tier-2 data.
            if outcome and probe.name not in self.state.probes_resolved:
                self.state.probes_resolved[probe.name] = outcome

    def location_for_dm(self) -> dict[str, Any]:
        """Fog-of-war-safe local grounding for the narrator (F10/F11
        2026-07-07): the you-are-here pin plus immediate exits and present
        affordances. The narrator holds the full manifest for theme and
        consistency, but must render ONLY this location (prompt discipline).
        The pin is the load-bearing datum: without it the narrator inferred
        position from prose history and drifted (lu-700001 'you glance back
        toward s6' while the player stood at s0). Exits are surfaced so a
        competent player can NAME a destination — the honest cure for the
        unmappable-commit rate, without handing over the global map."""
        site = self._site(self.state.position)
        return {
            "current_site": site.id,
            "exits": list(site.adjacency),
            "affordances_here": list(site.affordances),
        }

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

    HALT_VERDICTS = ("complete", "unreachable", "incomplete")

    def _validate(self, p: OpProposal) -> Optional[str]:
        if p.op in CONFIDENCE_REQUIRED and p.confidence is None:
            return f"{p.op.value} requires confidence"
        if p.op is OpName.HALT:
            v = str(p.args.get("verdict", "")).lower()
            if v not in self.HALT_VERDICTS:
                # Series-2 (Gate-1): verdict is a closed enum. Rejection is
                # mechanical friction (F10 narrator constraint renders it as
                # the declaration failing to land, never world-agency); the
                # third code makes stopping-without-claiming expressible, so
                # requiring a verdict no longer forces a false binary.
                return ("HALT verdict must be one of: complete, unreachable, "
                        "incomplete")
        if p.op is OpName.COMMIT and p.args.get("action") == "move":
            dest = p.args.get("site")
            site = self._site(self.state.position)
            if dest not in site.adjacency:
                return f"no path from {self.state.position} to {dest}"
        return None

    DITHER_COST = 1  # unparseable/rejected turns burn charge: bounds every
    # game to ~budget turns and closes the infinite-narration exploit
    # (empirically: run 2 died of context overflow after ~24 free turns).

    def _charge_dither(self, delta: Delta) -> None:
        self.state.budget -= self.DITHER_COST
        # Gate-2 smoke fix: the narrator cannot calibrate brightness without
        # the denominator ("remaining: 15" read as dying at 83% charge).
        delta.events.append({"type": "budget", "remaining": self.state.budget,
                             "of": self.state.instance.budget})
        if self.state.budget <= 0:
            self.state.terminal = "BUDGET_EXHAUSTED"
            delta.terminal = self.state.terminal

    def _charge(self, p: OpProposal, delta: Delta) -> None:
        cost = self.op_costs.get(p.op.value, 1)
        self.state.budget -= cost
        delta.events.append({"type": "budget", "remaining": self.state.budget,
                             "of": self.state.instance.budget})
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
        delta.events.append({"type": "halted", "reason": p.args.get("reason", ""),
                             "verdict": p.args.get("verdict", "")})

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
