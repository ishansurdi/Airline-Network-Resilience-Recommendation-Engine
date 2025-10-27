from __future__ import annotations
from typing import List, Tuple

import pandas as pd
import numpy as np
from backend.config.db_config import fetch_df
from .model_loader import embed_texts


def similar_routes_by_route_id(route_id: int, top_k: int = 10) -> pd.DataFrame:
    # Fetch all embeddings
    df = fetch_df("SELECT route_id, embedding FROM route_embeddings")
    
    # Drop rows with missing embeddings
    df = df[df['embedding'].notna()].copy()
    if df.empty:
        return pd.DataFrame(columns=['neighbor_route_id', 'cosine_distance'])
    
    # Convert BLOB -> NumPy array
    df['embedding'] = df['embedding'].apply(lambda b: np.frombuffer(b, dtype=np.float32))
    
    # Extract target embedding
    target_row = df.loc[df['route_id'] == route_id]
    if target_row.empty:
        raise ValueError(f"Route ID {route_id} not found in database or has no embedding.")
    
    target = target_row['embedding'].values[0]
    target_norm = np.linalg.norm(target)
    
    # Compute cosine distances efficiently
    df['cosine_distance'] = df['embedding'].apply(
        lambda x: 1 - (np.dot(target, x) / (target_norm * np.linalg.norm(x)))
    )
    
    # Filter out the route itself, sort by similarity, and pick top_k
    df = df[df['route_id'] != route_id].sort_values('cosine_distance').head(top_k)
    
    # Rename column for clarity
    df = df.rename(columns={'route_id': 'neighbor_route_id'})
    
    return df[['neighbor_route_id', 'cosine_distance']].reset_index(drop=True)



def similar_routes_by_text(query_text: str, top_k: int = 10) -> pd.DataFrame:
    # Compute query embedding
    query_vector = embed_texts([query_text])[0]
    query_norm = np.linalg.norm(query_vector)
    
    # Fetch all embeddings
    df = fetch_df("SELECT route_id, description, embedding FROM route_embeddings")
    df = df[df['embedding'].notna()].copy()
    if df.empty:
        return pd.DataFrame(columns=['route_id', 'description', 'cosine_distance'])
    
    # Convert BLOB -> NumPy arrays
    df['embedding'] = df['embedding'].apply(lambda b: np.frombuffer(b, dtype=np.float32))
    
    # Compute cosine similarity
    df['cosine_distance'] = df['embedding'].apply(
        lambda x: 1 - (np.dot(query_vector, x) / (query_norm * np.linalg.norm(x)))
    )
    
    # Sort by similarity and take top_k
    df = df.sort_values('cosine_distance').head(top_k)
    
    return df[['route_id', 'description', 'cosine_distance']].reset_index(drop=True)
