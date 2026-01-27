# Development Log – Creo → Odoo Middleware

This document records the step-by-step development progress of the project.It serves as an engineering log to explain **what was done, why it was done, what failed, and how it was fixed**.

---

## 2026-01-XX — Project Initialization & Environment Setup

### Goal

Set up the basic project structure on Windows and verify that Python package imports work correctly before implementing business logic.

---

### What I attempted

-   Create the initial folder structure for:
    -   matching logic
    -   backend
    -   UI (PySide)
-   Run a simple Python sanity check to verify imports.

---

### What failed (and error messages)

1.  **Created proper Python packages**

-   Added `__init__.py` files to all relevant folders

2.  **Ensured correct imports**

-   Imported functions directly instead of modules
-   Ran scripts from the project root
-   Used `python -m` as a fallback to ensure correct module resolution

### Commands executed (PowerShell)

```powershell
# Create foldersmkdir matching_logic -Forcemkdir matching_logiccore -Forcemkdir scripts -Force# Create package markersNew-Item -ItemType File matching_logic__init__.py -ForceNew-Item -ItemType File matching_logiccore__init__.py -ForceNew-Item -ItemType File scripts__init__.py -Force# Create normalize.py@'def normalize_name(name: str) -> str: return name.strip().upper()'@ | Set-Content matching_logiccorenormalize.py# Create sanity_check.py@'from matching_logic.core.normalize import normalize_nameprint("Imports OK:", normalize_name("motor housing"))'@ | Set-Content scriptssanity_check.pyFiles created / modifiedmatching_logic/├── __init__.py├── core/│   ├── __init__.py│   └── normalize.pyscripts/├── __init__.py└── sanity_check.pyVerificationCommand run:python .scriptssanity_check.pyOutput:Imports OK: MOTOR HOUSINGThis confirmed:Folder structure is correctPython package imports workEnvironment is ready for further developmentNext planned stepsAdd first pytest unit test for normalizationImplement alias → exact → similarity matching pipelineIntroduce local SQLite registry---## ✅ How to use this going forwardEvery time you:- hit an error- change a design decision- add a new core feature👉 **Add a new dated section** at the top.Example:```md## 2026-01-XX — Implemented Exact Match Logic
```