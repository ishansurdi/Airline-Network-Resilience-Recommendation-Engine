from __future__ import annotations
import csv
from pathlib import Path
from typing import Iterator, Tuple

from backend.config.db_config import executemany_sql
from backend.config.settings import OPENFLIGHTS_ROUTES


def read_routes(path: Path) -> Iterator[Tuple]:
    """
    Reads routes.dat and yields cleaned tuples ready for DB insertion.
    """
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 9:
                continue

            airline = row[0] if row[0] != "\\N" else None
            airline_id = int(row[1]) if row[1] not in ("", "\\N") else None
            source_airport = row[2] if row[2] != "\\N" else None
            source_airport_id = int(row[3]) if row[3] not in ("", "\\N") else None
            dest_airport = row[4] if row[4] != "\\N" else None
            dest_airport_id = int(row[5]) if row[5] not in ("", "\\N") else None
            codeshare = row[6] if row[6] != "\\N" else None
            stops = int(row[7]) if row[7] not in ("", "\\N") else 0
            equipment = row[8] if row[8] != "\\N" else None

            

            yield (
                airline,
                airline_id,
                source_airport,
                source_airport_id,
                dest_airport,
                dest_airport_id,
                codeshare,
                stops,
                equipment,
            )


def load_routes() -> None:
    """
    Loads all routes into the database.
    """
    sql = """
        INSERT INTO routes (
            airline, airline_id, source_airport, source_airport_id,
            dest_airport, dest_airport_id, codeshare, stops, equipment
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            airline = VALUES(airline),
            airline_id = VALUES(airline_id),
            source_airport = VALUES(source_airport),
            source_airport_id = VALUES(source_airport_id),
            dest_airport = VALUES(dest_airport),
            dest_airport_id = VALUES(dest_airport_id),
            codeshare = VALUES(codeshare),
            stops = VALUES(stops),
            equipment = VALUES(equipment)
    """

    rows = list(read_routes(OPENFLIGHTS_ROUTES))
    if rows:
        executemany_sql(sql, rows)
        print(f"Inserted/Updated {len(rows)} routes.")


if __name__ == "__main__":
    load_routes()
