"""Op proposals: the interpretation layer's output schema and tolerant parsing.

Parse failures return None; the engine logs them as rejections. Failure
rates are themselves data on interpreter quality (SPEC section 2,
interpretation regime: soft but logged).
"""
from __future__ import annotations

import json
import re
from typing import Any, Optional

from pydantic import BaseModel, Field, ValidationError

from .state import OpName

CONFIDENCE_REQUIRED = {OpName.COMMIT, OpName.HALT}


class OpProposal(BaseModel):
    op: OpName
    args: dict[str, Any] = Field(default_factory=dict)
    confidence: Optional[float] = None

    def validated_dict(self) -> dict[str, Any]:
        return {"op": self.op.value, "args": self.args, "confidence": self.confidence}


def parse_proposal(raw: str) -> Optional[OpProposal]:
    """Tolerant parse of the interpreter's JSON output.

    Three outcomes: an OpProposal (parsed), OpProposal(op=UNMAPPABLE) (the
    interpreter EXPLICITLY declined — friction, not fault), or None (genuine
    parse failure — the only outcome the F9 breaker counts). Separating the
    explicit decline from garbage is F11 (2026-07-07): Haiku correctly
    emitted {} for underspecified commits ('step toward the pull' — a move
    with no site) rather than fabricating a destination, and the old code
    collapsed that into unparseable_proposal, tripping the breaker on a
    WORKING interpreter."""
    if "UNMAPPABLE" in raw:
        return OpProposal(op=OpName.UNMAPPABLE)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        prop = OpProposal.model_validate(json.loads(match.group(0)))
    except (json.JSONDecodeError, ValidationError):
        return None
    # F1 (2026-07-06): the interpreter places confidence stochastically --
    # top-level (canonical) or nested inside args. The nesting ate both
    # lu-700002 honest halts: 0.70/0.82 extracted correctly, validator saw
    # top-level None, rejected "HALT requires confidence". Accept either
    # location; top-level wins when both are present.
    if prop.confidence is None and "confidence" in prop.args:
        raw_conf = prop.args.pop("confidence")
        try:
            prop.confidence = float(raw_conf)
        except (TypeError, ValueError):
            pass  # junk value: confidence stays None, validator rejects loudly
    return prop
