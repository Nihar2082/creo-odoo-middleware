# Requirements — Creo → Middleware → Odoo Part-list Preparation Tool (PySide Desktop)

## Project objective
Build a **PySide desktop middleware** that ingests Creo-exported EBOM part lists and produces a **clean, deterministic, engineer-reviewed** part list ready for **Odoo import**.

The tool must:
- Parse a Creo-style part list file
- Detect existing parts using a local registry
- Assign module-scoped **External IDs** for new parts
- Force explicit user resolution for ambiguous matches
- Export only approved/included parts in an Odoo-friendly format

---

## Key concepts

### External ID
- **External ID (module-wise)** is the single human-readable part identifier.
- Example formats:
  - `PS_001`
  - `PS_002_A`
  - `STD_014`
- The same External ID is used as **Odoo Internal Reference** (`default_code`) to keep Odoo UI clean and consistent.

### Included flag
- An **Included** flag (`Yes/No`) controls export.
- Export includes **only** `Included=Yes`.

---

## Functional requirements

### 1) Input handling
- PySide desktop UI with **drag-and-drop upload** of `.txt` or `.csv` part list files (reuse in-house modules).
- File structure similar to Creo part list exports with fields like:
  - `Qty`, `Name`, `Item Type`, `Description`, `Rev`
- Parsing must include validation and optional trimming of whitespace.

### 2) Normalization & External ID generation
- Normalize part names by converting to **UPPERCASE** (optional trim). **No tokenization.**
- External ID format (module-scoped):
  - `<PREFIX>_<NNN>[_<REV>]`
- Prefix comes from selected module (examples):
  - Photostation → `PS`
  - Standard parts → `STD`
- Sequential numbering per module using a **counter stored in the local database**.
- External ID is generated **only** when a part is confirmed as **NEW** (kept/created), and reused for **EXISTING** parts.

### 3) Duplicate detection & matching logic (deterministic)
Matching must be deterministic and explainable (no ML/AI).

- **Level 0 – Alias lookup**
  - If a previously learned alias exists, resolve as **EXISTING**
- **Level 1 – Exact match**
  - Match by `UPPERCASE(name)` + `item type`
  - If found → status = **EXISTING**
- **Level 2 – Similarity suggestion**
  - Use string similarity on UPPERCASE names to propose candidates
  - If similarity exceeds threshold → status = **POSSIBLE_MATCH** (requires user decision)
  - Otherwise → status = **NEW**

### 4) States & inclusion rules
- Each part must end in exactly one status:
  - `NEW`, `EXISTING`, `POSSIBLE_MATCH`
- `Included=Yes/No` controls export.
- **Export must be blocked** if any `POSSIBLE_MATCH` remains unresolved.

### 5) Local part registry (persistence layer)
Maintain a local database (SQLite for PoC; PostgreSQL possible later) storing at minimum:
- External ID (module-wise)
- Original name
- Normalized name (UPPERCASE)
- Item type
- Module
- Revision (if applicable)
- Match reference (resolved canonical part)
- Alias mappings (alias name → canonical part)
- Included flag

This registry acts as long-term system memory and ensures deterministic re-imports.

### 6) UI (PySide desktop)
Single-window, table-first PySide UI:
- Central table columns:
  - `Qty | Part Name | Item Type | Status | External ID | Included`
- Filter by Status and search by Part Name
- A select/resolve dialog appears **only** for `POSSIBLE_MATCH` items
- Actions:
  - **EXISTING** → toggle Included
  - **NEW** → Create / Exclude
  - **POSSIBLE_MATCH** → Link & remember / Create new / Exclude

### 7) Export
Generate Odoo-import-ready Excel/CSV containing (at minimum):
- External ID (**also used as Odoo Internal Reference / `default_code`**)
- Name
- Item Type
- Quantity
- Revision (optional)
- Module (optional)

Rules:
- Export only rows where `Included=Yes`
- Export must fail/block if any `POSSIBLE_MATCH` is unresolved

---

## Proof of Concept (PoC) scope

### PoC objectives
- PySide drag-and-drop file ingest (reuse in-house modules)
- Parsing + UPPERCASE normalization
- Module-wise External ID generation with counters
- DB-backed registry + alias learning
- Deterministic duplicate detection (exact + similarity suggestions)
- Conflict resolution for POSSIBLE_MATCH via PySide dialog
- Excel/CSV export compatible with Odoo; **no unresolved POSSIBLE_MATCH**

### Explicitly out of scope (PoC)
- Direct Odoo API write (XML-RPC / JSON-RPC)
- Authentication / roles
- Revision control beyond simple suffix handling
- Web hosting/deployment (no web UI)

---

## Tech stack (PoC)
- UI: PySide (reuse in-house drag-and-drop modules)
- Backend/service layer: Python
- Database: SQLite
- Export: pandas → Excel/CSV

---

## Recommended implementation order
Backend-first development:
1. matching-logic: pure functions + tests (alias → exact → similarity)
2. backend: parsing + DB persistence + module counters + export
3. ui-pyside: wire existing widgets to backend service functions

---

## Non-functional requirements
- Deterministic behavior (same input → same output)
- No black-box automation; decisions are visible and reversible
- Clear separation between logic, UI, and persistence
- Designed to scale into API-based Odoo sync later
