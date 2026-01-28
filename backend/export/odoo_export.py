from __future__ import annotations
import csv
from typing import List
from matching_logic.models.types import ProcessedRow

def export_odoo_csv(rows: List[ProcessedRow], out_path: str) -> None:
    """
    Minimal Odoo-friendly export:
    - external_id
    - default_code (Internal Reference) = external_id
    - name
    - item_type
    - qty
    """
    included = [r for r in rows if r.included]
    unresolved = [r for r in included if r.status == "POSSIBLE_MATCH"]
    if unresolved:
        raise RuntimeError("Cannot export: unresolved POSSIBLE_MATCH rows exist.")

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["external_id", "default_code", "name", "item_type", "qty", "revision"],
        )
        w.writeheader()
        for r in included:
            ext = r.external_id or ""
            w.writerow(
                {
                    "external_id": ext,
                    "default_code": ext,  # Odoo Internal Reference = External ID
                    "name": r.name,
                    "item_type": r.item_type,
                    "qty": r.qty,
                    "revision": r.revision or "",
                }
            )
