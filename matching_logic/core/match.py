from __future__ import annotations
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional
from matching_logic.core.normalize import normalize_name


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def match_row(
    name: str,
    item_type: str,
    registry: Dict,
    threshold: float = 0.85,
    max_suggestions: int = 5,
) -> Tuple[str, Optional[str], List[Tuple[str, float, str]]]:
    """
    Returns: (status, external_id_if_existing, suggestions)
    suggestions: list of (external_id, score, reason)
    registry expects:
      registry["aliases"]: dict[alias_name_norm] -> external_id
      registry["parts"]: list of dict {external_id, name_norm, item_type, module, revision}
    """
    name_norm = normalize_name(name)
    item_type_norm = normalize_name(item_type)

    # 0) alias
    ext = registry.get("aliases", {}).get(name_norm)
    if ext:
        return "EXISTING", ext, []

    # 1) exact
    for p in registry.get("parts", []):
        if p["name_norm"] == name_norm and normalize_name(p["item_type"]) == item_type_norm:
            return "EXISTING", p["external_id"], []

    # 2) similarity (same item type only)
    candidates: List[Tuple[str, float, str]] = []
    for p in registry.get("parts", []):
        if normalize_name(p["item_type"]) != item_type_norm:
            continue
        s = similarity(name_norm, p["name_norm"])
        if s >= threshold:
            reason = f"name similarity {s:.2f}"
            candidates.append((p["external_id"], s, reason))

    candidates.sort(key=lambda x: x[1], reverse=True)

    if candidates:
        return "POSSIBLE_MATCH", None, candidates[:max_suggestions]

    return "NEW", None, []
