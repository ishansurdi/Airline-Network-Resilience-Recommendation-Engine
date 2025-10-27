from __future__ import annotations
import argparse
import sys

from backend.config.db_config import run_sql_file
from backend.config.settings import SCRIPTS_DIR
from backend.data_ingestion.load_airports import load_airports
from backend.data_ingestion.load_airlines import load_airlines
from backend.data_ingestion.load_routes import load_routes
from backend.data_ingestion.generate_synthetic_descriptions import (
    build_route_descriptions,
    upsert_descriptions,
)
from backend.vector_engine.embed_routes import embed_all


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed MariaDB with OpenFlights data and embeddings")
    parser.add_argument("--schema", action="store_true", help="Create schema")
    parser.add_argument("--load", action="store_true", help="Load airports, airlines, routes")
    parser.add_argument("--describe", action="store_true", help="Generate synthetic descriptions")
    parser.add_argument("--embed", action="store_true", help="Generate embeddings")
    parser.add_argument("--all", action="store_true", help="Run all steps")
    args = parser.parse_args()

    if args.all or args.schema:
        run_sql_file(str(SCRIPTS_DIR / "setup_mariadb.sql"))
        print("Schema created/ensured")

    if args.all or args.load:
        load_airports()
        print("Airports loaded")
        load_airlines()
        print("Airlines loaded")
        load_routes()
        print("Routes loaded")

    if args.all or args.describe:
        df = build_route_descriptions()
        upsert_descriptions(df)
        print("Descriptions generated")

    if args.all or args.embed:
        embed_all()
        print("Embeddings generated")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
