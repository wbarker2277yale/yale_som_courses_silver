"""Build data/mgt409.db from data/yale_som_classes.json.

Run from backend/: python build_db.py
Rebuilding replaces the courses table, so it is safe to run repeatedly.
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
JSON_PATH = ROOT / "data" / "yale_som_classes.json"
DB_PATH = ROOT / "data" / "mgt409.db"


def column_name(key: str) -> str:
    """'Course Session Start date' -> 'course_session_start_date'."""
    return re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")


def main() -> None:
    courses = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    # Keep the JSON's key order; some keys only appear on some courses.
    keys: list[str] = []
    for course in courses:
        for key in course:
            if key not in keys:
                keys.append(key)
    columns = [f'"{column_name(k)}"' for k in keys]

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DROP TABLE IF EXISTS courses")
        conn.execute(
            "CREATE TABLE courses (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            + ", ".join(f"{c} TEXT" for c in columns)
            + ")"
        )
        conn.executemany(
            f"INSERT INTO courses ({', '.join(columns)}) "
            f"VALUES ({', '.join('?' for _ in columns)})",
            [[course.get(k) for k in keys] for course in courses],
        )
        count = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]

    print(f"Wrote {count} courses to {DB_PATH}")


if __name__ == "__main__":
    main()
