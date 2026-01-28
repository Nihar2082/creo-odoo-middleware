from __future__ import annotations
from backend.db.repo import Repo
from backend.db.schema import init_db
from backend.parsers.ebom_parser import parse_ebom
from backend.services.pipeline import process_file, link_and_remember, create_new_part
from backend.export.odoo_export import export_odoo_csv

DB_PATH = "data/app.db"

def main():
    init_db(DB_PATH)
    repo = Repo(DB_PATH)

    module = input("Module (Photostation/Standard): ").strip()
    file_path = input("EBOM path (txt/csv): ").strip()

    rows = parse_ebom(file_path)
    processed = process_file(repo, module=module, ebom_rows=rows, threshold=0.85)

    # Simple interactive resolver for demo
    for i, r in enumerate(processed, start=1):
        print(f"\n[{i}] {r.name} | {r.item_type} | status={r.status} | ext={r.external_id} | included={r.included}")
        if r.status == "POSSIBLE_MATCH":
            print("  Suggestions:")
            for sidx, s in enumerate(r.suggestions, start=1):
                print(f"    {sidx}. {s.external_id} ({s.reason})")

            action = input("  Action: (l)ink+remember, (c)reate new, (e)xclude: ").strip().lower()
            if action == "l":
                choice = int(input("  Pick suggestion number: ").strip())
                canonical = r.suggestions[choice - 1].external_id
                link_and_remember(repo, alias_name=r.name, canonical_external_id=canonical)
                r.status = "EXISTING"
                r.external_id = canonical
            elif action == "c":
                new_ext = create_new_part(repo, module=module, row=r)
                r.status = "NEW"
                r.external_id = new_ext
            else:
                r.included = False

        elif r.status == "NEW":
            action = input("  NEW: (k)eep/create id, (e)xclude: ").strip().lower()
            if action == "k":
                new_ext = create_new_part(repo, module=module, row=r)
                r.external_id = new_ext
            else:
                r.included = False

        else:
            # EXISTING
            action = input("  EXISTING: (i)nclude, (e)xclude: ").strip().lower()
            r.included = (action != "e")

    out_path = "data/odoo_export.csv"
    export_odoo_csv(processed, out_path)
    print(f"\nExport written to: {out_path}")
    print("Note: Odoo Internal Reference (default_code) = External ID")

if __name__ == "__main__":
    main()
