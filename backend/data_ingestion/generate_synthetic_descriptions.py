from __future__ import annotations
from typing import List, Tuple
import pandas as pd
import numpy as np
import time
from sentence_transformers import SentenceTransformer

from backend.config.db_config import fetch_df, executemany_sql

DESCRIPTION_TEMPLATE = (
    """
    The route from {src_city} ({src_iata}) to {dst_city} ({dst_iata}) is operated by {airline_name}.
    It typically has {stops} stop(s) and uses aircraft {equipment}. This route connects {src_country}
    to {dst_country} and serves both business and leisure passengers.
    """.strip()
)

# Load once
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_route_descriptions(limit: int = 50000) -> pd.DataFrame:
    sql = """
        SELECT r.route_id, r.stops, r.equipment,
               sa.city AS src_city, sa.iata AS src_iata, sa.country AS src_country,
               da.city AS dst_city, da.iata AS dst_iata, da.country AS dst_country,
               al.name AS airline_name
        FROM routes r
        LEFT JOIN airports sa ON r.source_airport_id = sa.airport_id
        LEFT JOIN airports da ON r.dest_airport_id = da.airport_id
        LEFT JOIN airlines al ON r.airline_id = al.airline_id
        LIMIT %s
    """
    df = fetch_df(sql, params=(limit,))

    def fmt(row: pd.Series) -> str:
        return DESCRIPTION_TEMPLATE.format(
            src_city=row.get("src_city") or "Unknown City",
            src_iata=row.get("src_iata") or "N/A",
            dst_city=row.get("dst_city") or "Unknown City",
            dst_iata=row.get("dst_iata") or "N/A",
            airline_name=row.get("airline_name") or "Unknown Airline",
            stops=int(row.get("stops") or 0),
            equipment=row.get("equipment") or "various equipment",
            src_country=row.get("src_country") or "Unknown Country",
            dst_country=row.get("dst_country") or "Unknown Country",
        )

    df["description"] = df.apply(fmt, axis=1)
    return df[["route_id", "description"]]


def embed_and_upsert_in_batches(df: pd.DataFrame, batch_size: int = 500):
    sql = """
        INSERT INTO route_embeddings (route_id, description, embedding)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            description=VALUES(description),
            embedding=VALUES(embedding)
    """
    total = len(df)
    for start in range(0, total, batch_size):
        batch = df.iloc[start:start + batch_size]
        print(f"🔹 Processing batch {start}–{min(start + batch_size, total)}...")

        descriptions = batch["description"].tolist()
        embeddings = model.encode(descriptions, normalize_embeddings=True)

        rows: List[Tuple[int, str, bytes]] = [
            (int(rid), desc, np.array(emb, dtype=np.float32).tobytes())
            for rid, desc, emb in zip(batch["route_id"], descriptions, embeddings)
        ]
        executemany_sql(sql, rows)
        print(f"✅ Inserted {len(rows)} routes.")
        time.sleep(0.3)  # small delay to reduce DB load


if __name__ == "__main__":
    print("🚀 Generating synthetic route descriptions & embeddings in batches...")
    df = build_route_descriptions(limit=10000)  # try 1000–5000 for first run
    embed_and_upsert_in_batches(df)
    print("🎯 Done! Embeddings populated in route_embeddings table.")
