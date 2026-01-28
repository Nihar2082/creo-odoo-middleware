from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class EBOMRow:
    qty: float
    name: str
    item_type: str
    revision: Optional[str] = None
    description: Optional[str] = None

@dataclass
class MatchSuggestion:
    external_id: str
    name: str
    score: float
    reason: str

@dataclass
class ProcessedRow:
    qty: float
    name: str
    item_type: str
    revision: Optional[str] = None
    description: Optional[str] = None

    status: str = "NEW"  # NEW | EXISTING | POSSIBLE_MATCH
    external_id: Optional[str] = None  # also used as Odoo default_code
    suggestions: List[MatchSuggestion] = field(default_factory=list)

    included: bool = True  # export filter
