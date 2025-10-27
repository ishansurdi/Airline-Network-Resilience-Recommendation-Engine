from __future__ import annotations
import os
import pandas as pd
from typing import Any, Iterable, Optional, Tuple
import mysql.connector

from .settings import (
    MARIADB_DB,
    MARIADB_HOST,
    MARIADB_PASSWORD,
    MARIADB_PORT,
    MARIADB_USER,
    MARIADB_CONNECT_TIMEOUT,
)


def get_connection(database: Optional[str] = None) -> mysql.connector.connection.MySQLConnection:
    """Returns a MySQL connection using environment-backed settings."""
    conn = mysql.connector.connect(
        user=MARIADB_USER,
        password=MARIADB_PASSWORD,
        host=MARIADB_HOST,
        port=MARIADB_PORT,
        database=database or MARIADB_DB,
        connection_timeout=MARIADB_CONNECT_TIMEOUT,
        autocommit=True
    )
    return conn


def execute_sql(sql: str, params: Optional[Iterable[Any]] = None, database: Optional[str] = None) -> None:
    conn = get_connection(database)
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
    finally:
        cur.close()
        conn.close()


def executemany_sql(sql: str, rows: Iterable[Tuple[Any, ...]], database: Optional[str] = None) -> None:
    conn = get_connection(database)
    try:
        cur = conn.cursor()
        cur.executemany(sql, list(rows))
    finally:
        cur.close()
        conn.close()


def fetch_df(sql: str, params: Optional[Iterable[Any]] = None, database: Optional[str] = None) -> pd.DataFrame:
    conn = get_connection(database)
    try:
        df = pd.read_sql(sql, conn, params=params)
        return df
    finally:
        conn.close()


def run_sql_file(path: str, database: Optional[str] = None) -> None:
    with open(path, "r", encoding="utf-8") as f:
        script = f.read()
    statements = [s.strip() for s in script.split(";") if s.strip()]
    conn = get_connection(database)
    try:
        cur = conn.cursor()
        for stmt in statements:
            cur.execute(stmt)
    finally:
        cur.close()
        conn.close()
