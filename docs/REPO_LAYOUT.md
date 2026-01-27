creo-odoo-middleware/
  matching_logic/                # pure logic (alias -> exact -> similarity), unit-testable
    core/
    scoring/
    models/

  backend/                       # orchestration (DB, parsing, export, services)
    db/
    parsers/
    services/
    export/

  ui-pyside/                     # PySide wiring only (thin UI)
    app/
    widgets/
    dialogs/

  tests/                         # pytest tests for matching_logic + backend/services

  docs/                          # ALL documentation lives here
    SETUP.md                     # “how to run on Windows”
    DEV_LOG.md                   # your step-by-step progress log
    decisions/                   # design decisions (IDs, thresholds, statuses)
      ID_STRATEGY.md
      MATCHING_RULES.md
    diagrams/                    # PlantUML files
      swimlane_simplified.puml
    prompts/                     # all ChatGPT prompts, kept versioned
      ui_pyside_prompt.md
      backend_prompt.md
      matching_logic_prompt.md

  samples/                       # sample EBOM input files (txt/csv)
  scripts/                       # CLI tools: init_db, run_pipeline, export_demo
  data/                          # local sqlite db (gitignored)
  README.md
  .gitignore
  requirements.txt (or pyproject.toml)
