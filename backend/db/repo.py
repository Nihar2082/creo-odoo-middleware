from __future__ import annotations
import sqlite3
from typing import Dict, List, Optional, Tuple

class Repo:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def load_registry(self) -> Dict:
        conn = self._connect()
        try:
            aliases = {}
            for r in conn.execute("SELECT alias_norm, external_id FROM aliases"):
                aliases[r["alias_norm"]] = r["external_id"]

            parts = []
            for r in conn.execute(
                "SELECT external_id, name_norm, item_type, module, revision FROM parts"
            ):
                parts.append(
                    {
                        "external_id": r["external_id"],
                        "name_norm": r["name_norm"],
                        "item_type": r["item_type"],
                        "module": r["module"],
                        "revision": r["revision"],
                    }
                )
            return {"aliases": aliases, "parts": parts}
        finally:
            conn.close()

    def get_module_counter(self, module: str, prefix: str) -> int:
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT last_number FROM module_counters WHERE module = ?",
                (module,),
            ).fetchone()
            if row is None:
                conn.execute(
                    "INSERT INTO module_counters(module, prefix, last_number) VALUES(?,?,?)",
                    (module, prefix, 0),
                )
                conn.commit()
                return 0
            return int(row["last_number"])
        finally:
            conn.close()

    def increment_module_counter(self, module: str, prefix: str) -> int:
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT last_number FROM module_counters WHERE module = ?",
                (module,),
            ).fetchone()
            if row is None:
                new_num = 1
                conn.execute(
                    "INSERT INTO module_counters(module, prefix, last_number) VALUES(?,?,?)",
                    (module, prefix, new_num),
                )
            else:
                new_num = int(row["last_number"]) + 1
                conn.execute(
                    "UPDATE module_counters SET last_number = ?, prefix = ? WHERE module = ?",
                    (new_num, prefix, module),
                )
            conn.commit()
            return new_num
        finally:
            conn.close()

    def insert_part(
        self,
        external_id: str,
        module: str,
        prefix: str,
        number: int,
        revision: str | None,
        name_original: str,
        name_norm: str,
        item_type: str,
        description: str | None,
    ) -> None:
        conn = self._connect()
        try:
            conn.execute(
                """
                INSERT INTO parts(external_id, module, prefix, number, revision, name_original, name_norm, item_type, description)
                VALUES(?,?,?,?,?,?,?,?,?)
                """,
                (
                    external_id,
                    module,
                    prefix,
                    number,
                    revision,
                    name_original,
                    name_norm,
                    item_type,
                    description,
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def upsert_alias(self, alias_norm: str, external_id: str) -> None:
        conn = self._connect()
        try:
            conn.execute(
                """
                INSERT INTO aliases(alias_norm, external_id)
                VALUES(?,?)
                ON CONFLICT(alias_norm) DO UPDATE SET external_id=excluded.external_id
                """,
                (alias_norm, external_id),
            )
            conn.commit()
        finally:
            conn.close()
