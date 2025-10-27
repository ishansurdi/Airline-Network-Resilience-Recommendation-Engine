from __future__ import annotations
import csv
from pathlib import Path
from typing import Iterator, Tuple

from backend.config.db_config import executemany_sql
from backend.config.settings import OPENFLIGHTS_AIRLINES


def read_airlines(path: Path) -> Iterator[Tuple]:
    """
    Reads the airlines CSV and yields tuples with proper None handling.
    """
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            # skip empty or malformed rows
            if not row or len(row) < 8:
                continue
            yield (
                int(row[0]) if row[0] not in ("", "\\N") else None,  # id
                row[1] or None,  # name
                row[2] if row[2] not in ("", "\\N") else None,  # alias
                row[3] if row[3] not in ("", "\\N") else None,  # IATA
                row[4] if row[4] not in ("", "\\N") else None,  # ICAO
                row[5] if row[5] not in ("", "\\N") else None,  # Callsign
                row[6] if row[6] not in ("", "\\N") else None,  # Country
                row[7] if row[7] not in ("", "\\N") else None,  # Active
            )


def load_airlines() -> None:
    sql = """
    INSERT INTO airlines (
      airline_id, name, alias, iata, icao, callsign, country, active
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      name=VALUES(name),
      alias=VALUES(alias),
      iata=VALUES(iata),
      icao=VALUES(icao),
      callsign=VALUES(callsign),
      country=VALUES(country),
      active=VALUES(active)
    """

    rows = list(read_airlines(OPENFLIGHTS_AIRLINES))
    if not rows:
        print("No rows to insert.")
        return

    print("First 5 rows to insert/update:", rows[:5])

    executemany_sql(sql, rows)
    print(f"Inserted/Updated {len(rows)} airlines successfully.")


if __name__ == "__main__":
    load_airlines()
