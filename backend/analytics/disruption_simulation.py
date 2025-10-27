from __future__ import annotations
from typing import Optional

import pandas as pd

from backend.config.db_config import fetch_df


def simulate_airport_closure(airport_id: int) -> pd.DataFrame:
    """
    Simulate closure of an airport by removing routes touching the airport
    and estimating impacted passengers.

    Args:
        airport_id (int): The ID of the airport to simulate closure for.

    Returns:
        pd.DataFrame: Routes affected by the closure with estimated passengers.
    """
    sql = """
        SELECT
            r.route_id,
            sa.name AS src_airport,
            da.name AS dst_airport,
            COALESCE(SUM(ps.passengers), 0) AS est_passengers
        FROM routes r
        LEFT JOIN airports sa ON r.source_airport_id = sa.airport_id
        LEFT JOIN airports da ON r.dest_airport_id = da.airport_id
        LEFT JOIN passenger_stats ps ON ps.route_id = r.route_id
        WHERE r.source_airport_id = %s OR r.dest_airport_id = %s
        GROUP BY r.route_id, src_airport, dst_airport
        ORDER BY est_passengers DESC
    """
    return fetch_df(sql, params=(airport_id, airport_id))


def suggest_alternate_routes(airport_id: int, top_k: int = 10) -> pd.DataFrame:
    """
    Suggest alternate routes avoiding the closed airport.

    Args:
        airport_id (int): Closed airport ID.
        top_k (int): Number of alternate routes.

    Returns:
        pd.DataFrame: Suggested alternate routes.
    """
    # Step 1: Get city and country of closed airport
    airport_sql = "SELECT city, country FROM airports WHERE airport_id = %s"
    closed_airport = fetch_df(airport_sql, params=(airport_id,))
    
    if closed_airport.empty:
        return pd.DataFrame()  # no such airport

    city = closed_airport.at[0, "city"]
    country = closed_airport.at[0, "country"]

    # Step 2: Query routes avoiding this airport
    sql = """
        SELECT
            r.route_id,
            sa.name AS src_airport,
            da.name AS dst_airport,
            sa.city AS src_city,
            da.city AS dst_city,
            sa.country AS src_country,
            da.country AS dst_country
        FROM routes r
        JOIN airports sa ON r.source_airport_id = sa.airport_id
        JOIN airports da ON r.dest_airport_id = da.airport_id
        WHERE (
            sa.city = %s OR da.city = %s
            OR sa.country = %s OR da.country = %s
        )
        AND sa.airport_id <> %s
        AND da.airport_id <> %s
        LIMIT %s
    """
    params = (city, city, country, country, airport_id, airport_id, top_k)
    return fetch_df(sql, params=params)