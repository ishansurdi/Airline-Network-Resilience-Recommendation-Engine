from __future__ import annotations
import pandas as pd

from backend.config.db_config import fetch_df


def busiest_hubs(limit: int = 20) -> pd.DataFrame:
    sql = """
        SELECT a.airport_id, a.name, a.city, a.country,
               COUNT(*) AS degree
        FROM routes r
        LEFT JOIN airports a ON r.source_airport_id = a.airport_id
        GROUP BY a.airport_id, a.name, a.city, a.country
        ORDER BY degree DESC
        LIMIT %s
    """
    return fetch_df(sql, params=(limit,))



def top_city_pairs_by_frequency(limit: int = 20) -> pd.DataFrame:
    sql = """
SELECT sa.city AS source_city, da.city AS dest_city, COUNT(*) AS flights
FROM routes r
LEFT JOIN airports sa ON r.source_airport_id = sa.airport_id
LEFT JOIN airports da ON r.dest_airport_id = da.airport_id
GROUP BY sa.city, da.city
ORDER BY flights DESC
LIMIT %s
"""
    return fetch_df(sql, params=(limit,))


def hub_load_and_delay(limit: int = 50) -> pd.DataFrame:
    sql = """
        SELECT a.airport_id, a.name, a.city, a.country,
               SUM(ps.passengers) AS total_passengers,
               AVG(ps.avg_delay_minutes) AS avg_delay
        FROM routes r
        JOIN passenger_stats ps ON ps.route_id = r.route_id
        JOIN airports a ON a.airport_id = r.source_airport_id
        GROUP BY a.airport_id, a.name, a.city, a.country
        ORDER BY total_passengers DESC
        LIMIT %s
    """
    return fetch_df(sql, params=(limit,))
