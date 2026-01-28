from __future__ import annotations
from typing import List, Dict, Optional
from matching_logic.models.types import EBOMRow, ProcessedRow, MatchSuggestion
from matching_logic.core.normalize import normalize_name
from matching_logic.core.match import match_row
from backend.db.repo import Repo
from backend.services.id_generation import resolve_prefix, format_external_id

# Configure module prefixes here (edit for your team)
MODULE_PREFIX_MAP = {
    "PHOTOSTATION": "PS",
    "STANDARD": "STD",
}

def process_file(repo: Repo, module: str, ebom_rows: List[EBOMRow], threshold: float = 0.85) -> List[ProcessedRow]:
    registry = repo.load_registry()
    processed: List[ProcessedRow] = []

    for r in ebom_rows:
        status, ext, suggestions = match_row(r.name, r.item_type, registry, threshold=threshold)

        pr = ProcessedRow(
            qty=r.qty,
            name=r.name,
            item_type=r.item_type,
            revision=r.revision,
            description=r.description,
            status=status,
            external_id=ext,
            included=True,
        )

        if status == "POSSIBLE_MATCH":
            pr.suggestions = [
                MatchSuggestion(
                    external_id=s[0],
                    name=s[0],  # for PoC: show ext id; can fetch name later
                    score=s[1],
                    reason=s[2],
                )
                for s in suggestions
            ]

        processed.append(pr)

    return processed


def link_and_remember(repo: Repo, alias_name: str, canonical_external_id: str) -> None:
    alias_norm = normalize_name(alias_name)
    repo.upsert_alias(alias_norm, canonical_external_id)


def create_new_part(repo: Repo, module: str, row: ProcessedRow) -> str:
    prefix = resolve_prefix(module, MODULE_PREFIX_MAP)
    next_num = repo.increment_module_counter(module=module, prefix=prefix)
    new_ext = format_external_id(prefix, next_num, row.revision)

    # Save to DB so future runs exact-match against normalized name
    repo.insert_part(
        external_id=new_ext,
        module=module,
        prefix=prefix,
        number=next_num,
        revision=row.revision,
        name_original=row.name,
        name_norm=normalize_name(row.name),
        item_type=normalize_name(row.item_type),
        description=row.description,
    )
    return new_ext
