from __future__ import annotations
import pandas as pd

from backend.config.db_config import fetch_df


def busiest_routes(limit: int = 50) -> pd.DataFrame:
    sql = """
        SELECT r.route_id,
               CONCAT(sa.city, ' → ', da.city) AS route_name,
               COUNT(*) AS frequency
        FROM routes r
        LEFT JOIN airports sa ON r.source_airport_id = sa.airport_id
        LEFT JOIN airports da ON r.dest_airport_id = da.airport_id
        GROUP BY r.route_id, route_name
        ORDER BY frequency DESC
        LIMIT ?
    """
    return fetch_df(sql, params=(limit,))


def delay_risk_overview(limit: int = 100) -> pd.DataFrame:
    sql = """
        SELECT r.route_id,
               CONCAT(sa.city, ' → ', da.city) AS route_name,
               dr.overall_risk,
               dr.weather_risk,
               dr.congestion_risk,
               dr.infra_risk
        FROM delay_risks dr
        JOIN routes r ON r.route_id = dr.route_id
        LEFT JOIN airports sa ON r.source_airport_id = sa.airport_id
        LEFT JOIN airports da ON r.dest_airport_id = da.airport_id
        ORDER BY dr.overall_risk DESC
        LIMIT ?
    """
    return fetch_df(sql, params=(limit,))
