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
    """Tolerant parse of the interpreter's JSON output."""
    if "UNMAPPABLE" in raw:
        return None
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        return OpProposal.model_validate(json.loads(match.group(0)))
    except (json.JSONDecodeError, ValidationError):
        return None
