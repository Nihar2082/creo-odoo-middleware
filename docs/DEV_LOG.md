# Development Log – Creo → Odoo Middleware

This document records the step-by-step development progress of the project.
It serves as an engineering log to explain **what was done, why it was done, what failed, and how it was fixed**.

---

## 2026-01-XX — Project Initialization & Environment Setup

**Goal**
Set up the basic project structure on Windows and verify that Python package imports work correctly before implementing business logic.

**What I attempted**

* Created the initial folder structure for:

  * `matching_logic`
  * `backend`
  * `UI (PySide)`
* Ran a simple Python sanity check to verify imports.

**What failed / Challenges**

* Created proper Python packages.
* Added `__init__.py` files to all relevant folders.
* Ensured correct imports.
* Imported functions directly instead of modules.
* Ran scripts from the project root.
* Used `python -m` as a fallback to ensure correct module resolution.

**Commands executed (PowerShell)**

```powershell
# Create folders
mkdir matching_logic -Force
mkdir matching_logic\core -Force
mkdir scripts -Force

# Create package markers
New-Item -ItemType File matching_logic\__init__.py -Force
New-Item -ItemType File matching_logic\core\__init__.py -Force
New-Item -ItemType File scripts\__init__.py -Force

# Create normalize.py
@'
def normalize_name(name: str) -> str:
    return name.strip().upper()
'@ | Set-Content matching_logic\core\normalize.py

# Create sanity_check.py
@'
from matching_logic.core.normalize import normalize_name
print("Imports OK:", normalize_name("motor housing"))
'@ | Set-Content scripts\sanity_check.py
```

**Files created / modified**

```
matching_logic/
├── __init__.py
├── core/
│   ├── __init__.py
│   └── normalize.py
scripts/
├── __init__.py
└── sanity_check.py
```

**Verification**

```powershell
# Command run
python .\scripts\sanity_check.py
```

**Output:**

```
Imports OK: MOTOR HOUSING
```

**Conclusion**

* Folder structure is correct.
* Python package imports work.
* Environment is ready for further development.

**Next planned steps**

1. Add first `pytest` unit test for normalization.
2. Implement alias → exact → similarity matching pipeline.
3. Introduce local SQLite registry.

---

## Python helper to add new log entries

```python
import datetime

def add_log_entry(filename: str, title: str, content: str):
    """Append a new dated development log entry in Markdown format."""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    entry = f"""
## {date_str} — {title}

{content}

---
"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"Log entry added to {filename}")

# Example usage
add_log_entry(
    "DEV_LOG.md",
    "Implemented Exact Match Logic",
    """**Goal**  
Implement exact matching step in the alias → exact → similarity pipeline.

**What I did**  
- Checked for exact part name matches in SQLite registry.
- Marked items as EXISTING if exact match found.
- Added logging for matched parts.

**Next steps**  
- Implement similarity-based matching for POSSIBLE_MATCH parts.
- Add pytest tests for exact matching."""
)
```
