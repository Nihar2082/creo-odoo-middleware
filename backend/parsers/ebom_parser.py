from __future__ import annotations
import csv
from pathlib import Path
from typing import List
from matching_logic.models.types import EBOMRow

def _to_float(x: str) -> float:
    try:
        return float(str(x).strip().replace(",", "."))
    except Exception:
        return 1.0

def parse_ebom(path: str) -> List[EBOMRow]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    # CSV path
    if p.suffix.lower() in {".csv"}:
        with p.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows: List[EBOMRow] = []
            for r in reader:
                rows.append(
                    EBOMRow(
                        qty=_to_float(r.get("Qty") or r.get("Quantity") or "1"),
                        name=(r.get("Name") or r.get("Part Name") or "").strip(),
                        item_type=(r.get("Item Type") or r.get("Type") or "PART").strip(),
                        revision=(r.get("Rev") or r.get("Revision") or "").strip() or None,
                        description=(r.get("Description") or "").strip() or None,
                    )
                )
            return rows

    # TXT: try delimiter detection (tab, semicolon, pipe, comma)
    text = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    if not text:
        return []

    delimiters = ["\t", ";", "|", ","]
    header = text[0]
    delim = max(delimiters, key=lambda d: header.count(d))

    # Assume header-like first line; if not, still parse positions by index
    headers = [h.strip() for h in header.split(delim)]
    def idx(name: str) -> int:
        for i, h in enumerate(headers):
            if h.lower() == name.lower():
                return i
        return -1

    i_qty = idx("Qty")
    if i_qty < 0: i_qty = idx("Quantity")
    i_name = idx("Name")
    if i_name < 0: i_name = idx("Part Name")
    i_type = idx("Item Type")
    if i_type < 0: i_type = idx("Type")
    i_rev = idx("Rev")
    if i_rev < 0: i_rev = idx("Revision")
    i_desc = idx("Description")

    rows: List[EBOMRow] = []
    for line in text[1:]:
        if not line.strip():
            continue
        cols = [c.strip() for c in line.split(delim)]
        rows.append(
            EBOMRow(
                qty=_to_float(cols[i_qty]) if i_qty >= 0 and i_qty < len(cols) else 1.0,
                name=cols[i_name] if i_name >= 0 and i_name < len(cols) else (cols[0] if cols else ""),
                item_type=cols[i_type] if i_type >= 0 and i_type < len(cols) else "PART",
                revision=cols[i_rev] if i_rev >= 0 and i_rev < len(cols) and cols[i_rev] else None,
                description=cols[i_desc] if i_desc >= 0 and i_desc < len(cols) and cols[i_desc] else None,
            )
        )
    return rows
