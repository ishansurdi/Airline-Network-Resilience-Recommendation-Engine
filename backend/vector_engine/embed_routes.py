from __future__ import annotations
from typing import List, Tuple

import numpy as np
import pandas as pd

from backend.config.db_config import fetch_df, executemany_sql
from backend.config.settings import EMBEDDING_DIMENSIONS
from .model_loader import embed_texts


def fetch_descriptions(limit: int = 50000) -> pd.DataFrame:
    sql = "SELECT route_id, description FROM route_embeddings WHERE description IS NOT NULL LIMIT ?"
    return fetch_df(sql, params=(limit,))


def upsert_embeddings(route_ids: List[int], embeddings: np.ndarray) -> None:
    sql = """
        INSERT INTO route_embeddings (route_id, embedding)
        VALUES (?, ?)
        ON DUPLICATE KEY UPDATE embedding=VALUES(embedding)
    """
    # MariaDB Python connector accepts bytes for VECTOR parameter (binary). For clarity, pass as Python list.
    rows: List[Tuple[int, list]] = [
        (int(rid), emb.astype(float).tolist()) for rid, emb in zip(route_ids, embeddings)
    ]
    executemany_sql(sql, rows)


def embed_all(limit: int = 50000) -> None:
    df = fetch_descriptions(limit=limit)
    if df.empty:
        return
    route_ids = df["route_id"].astype(int).tolist()
    texts = df["description"].astype(str).tolist()
    vectors = embed_texts(texts)
    if vectors.shape[1] != EMBEDDING_DIMENSIONS:
        # Re-encode without normalization to ensure shape, though model should match settings
        vectors = vectors.astype(float)
    upsert_embeddings(route_ids, vectors)


if __name__ == "__main__":
    embed_all()
