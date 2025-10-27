from __future__ import annotations
import csv
from pathlib import Path
from typing import Iterator, Tuple

from backend.config.db_config import executemany_sql
from backend.config.settings import OPENFLIGHTS_AIRPORTS  # Path to airports.dat


def read_airports(path: Path) -> Iterator[Tuple]:
    """Read airports CSV and yield tuples of 14 columns."""
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, quotechar='"')
        for row in reader:
            if not row or len(row) < 14:
                continue
            yield (
                int(row[0]) if row[0] not in ("", "\\N") else None,  # airport_id
                row[1] or None,  # name
                row[2] or None,  # city
                row[3] or None,  # country
                row[4] if row[4] != "\\N" else None,  # IATA
                row[5] if row[5] != "\\N" else None,  # ICAO
                float(row[6]) if row[6] not in ("", "\\N") else None,  # latitude
                float(row[7]) if row[7] not in ("", "\\N") else None,  # longitude
                int(float(row[8])) if row[8] not in ("", "\\N") else None,  # altitude
                float(row[9]) if row[9] not in ("", "\\N") else None,  # timezone
                row[10] or None,  # DST
                row[11] or None,  # tz_db
                row[12] or None,  # type
                row[13] or None,  # source
            )


def load_airports() -> None:
    # Use VALUES() in UPDATE so we don't have to duplicate Python tuples
    sql = """
        INSERT INTO airports (
            airport_id, name, city, country, iata, icao, latitude, longitude,
            altitude, timezone, dst, tz_db, type, source
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name=VALUES(name),
            city=VALUES(city),
            country=VALUES(country),
            iata=VALUES(iata),
            icao=VALUES(icao),
            latitude=VALUES(latitude),
            longitude=VALUES(longitude),
            altitude=VALUES(altitude),
            timezone=VALUES(timezone),
            dst=VALUES(dst),
            tz_db=VALUES(tz_db),
            type=VALUES(type),
            source=VALUES(source)
    """

    rows = list(read_airports(OPENFLIGHTS_AIRPORTS))
    if not rows:
        print("No rows found in the CSV.")
        return

    print("First 5 rows to insert/update:", rows[:5])
    executemany_sql(sql, rows)
    print(f"Inserted/Updated {len(rows)} rows successfully.")


if __name__ == "__main__":
    load_airports()
