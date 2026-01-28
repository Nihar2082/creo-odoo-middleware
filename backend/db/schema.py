import sqlite3

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS parts (
  external_id TEXT PRIMARY KEY,
  module TEXT NOT NULL,
  prefix TEXT NOT NULL,
  number INTEGER NOT NULL,
  revision TEXT,
  name_original TEXT NOT NULL,
  name_norm TEXT NOT NULL,
  item_type TEXT NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS aliases (
  alias_norm TEXT PRIMARY KEY,
  external_id TEXT NOT NULL,
  FOREIGN KEY(external_id) REFERENCES parts(external_id)
);

CREATE TABLE IF NOT EXISTS module_counters (
  module TEXT PRIMARY KEY,
  prefix TEXT NOT NULL,
  last_number INTEGER NOT NULL
);
"""

def init_db(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()
