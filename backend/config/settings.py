import os
from pathlib import Path

# Project settings
BASE_DIR: Path = Path(__file__).resolve().parents[2]
DATA_DIR: Path = BASE_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
SAMPLES_DIR: Path = DATA_DIR / "samples"
DOCS_DIR: Path = BASE_DIR / "docs"
SCRIPTS_DIR: Path = BASE_DIR / "scripts"

# Database settings (override via environment variables)
MARIADB_HOST: str = os.getenv("MARIADB_HOST", "127.0.0.1")
MARIADB_PORT: int = int(os.getenv("MARIADB_PORT", "3306"))
MARIADB_USER: str = os.getenv("MARIADB_USER", "root")
MARIADB_PASSWORD: str = os.getenv("MARIADB_PASSWORD", "123456789")
MARIADB_DB: str = os.getenv("MARIADB_DB", "airrouteiq")
MARIADB_CONNECT_TIMEOUT: int = int(os.getenv("MARIADB_CONNECT_TIMEOUT", "10"))

# ML / Embeddings
EMBEDDING_MODEL_NAME: str = os.getenv(
    "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
)
# All-MiniLM-L6-v2 outputs 384-dim embeddings
EMBEDDING_DIMENSIONS: int = int(os.getenv("EMBEDDING_DIMENSIONS", "384"))

# Feature flags
USE_MARIADB_VECTOR: bool = os.getenv("USE_MARIADB_VECTOR", "true").lower() in {"1", "true", "yes"}
USE_COLUMNSTORE: bool = os.getenv("USE_COLUMNSTORE", "true").lower() in {"1", "true", "yes"}

# Table names
TABLE_AIRPORTS: str = os.getenv("TABLE_AIRPORTS", "airports")
TABLE_AIRLINES: str = os.getenv("TABLE_AIRLINES", "airlines")
TABLE_ROUTES: str = os.getenv("TABLE_ROUTES", "routes")
TABLE_ROUTE_EMBEDDINGS: str = os.getenv("TABLE_ROUTE_EMBEDDINGS", "route_embeddings")
TABLE_PASSENGER_STATS: str = os.getenv("TABLE_PASSENGER_STATS", "passenger_stats")
TABLE_DELAY_RISKS: str = os.getenv("TABLE_DELAY_RISKS", "delay_risks")

# File names (OpenFlights)
OPENFLIGHTS_AIRPORTS: Path = RAW_DATA_DIR / "airports.dat"
OPENFLIGHTS_AIRLINES: Path = RAW_DATA_DIR / "airlines.dat"
OPENFLIGHTS_ROUTES: Path = RAW_DATA_DIR / "routes.dat"
OPENFLIGHTS_COUNTRIES: Path = RAW_DATA_DIR / "countries.dat"
OPENFLIGHTS_PLANES: Path = RAW_DATA_DIR / "planes.dat"

# Processed artifacts
ROUTES_CLEAN_CSV: Path = PROCESSED_DATA_DIR / "routes_clean.csv"
SYNTHETIC_RISKS_CSV: Path = PROCESSED_DATA_DIR / "synthetic_route_risks.csv"
EMBEDDINGS_CSV: Path = PROCESSED_DATA_DIR / "embeddings.csv"

# Streamlit settings
STREAMLIT_TITLE: str = "AirRouteIQ - Airline Network Analytics"


def ensure_directories() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
