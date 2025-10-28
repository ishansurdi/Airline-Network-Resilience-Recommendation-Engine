<!-- Top logos: MariaDB (left) and HackerRank (right). Replace URLs with local assets if desired. -->
<div style="display:flex; align-items:center; justify-content:space-between;">
   <img src="output_logo_images/mariadb.png" alt="MariaDB" height="48" style="margin:8px;" />
   <img src="output_logo_images/hackerearth.svg" alt="HackerEarth" height="48" style="margin:8px;" />
</div>


# Airline Network Resilience Recommendation Engine

Prototype web app for analyzing and simulating airline network resilience using MariaDB Vector and ColumnStore. Built for the MariaDB Python Hackathon.

---
## 📋 Table of Contents

- [Airline Network Resilience Recommendation Engine](#airline-network-resilience-recommendation-engine)
  - [Features](#features)
  - [Repository Layout](#repository-layout)
  - [Setup](#setup)
  - [Running](#running)
- [AirRouteIQ — Airline Network Resilience Recommendation Engine](#airrouteiq--airline-network-resilience-recommendation-engine)
  - [📋 Table of Contents](#-table-of-contents)
  - [📊 Project at a Glance](#-project-at-a-glance)
  - [🏗️ Repository Structure \& Rationale](#️-repository-structure--rationale)
  - [⚙️ How It Works — Data Pipeline \& Runtime Flow](#️-how-it-works--data-pipeline--runtime-flow)
  - [🗄️ MariaDB: What We Use and Why](#️-mariadb-what-we-use-and-why)
  - [🚀 Quick Start — Download to Running](#-quick-start--download-to-running)
  - [🔧 Configuration \& Environment Variables](#-configuration--environment-variables)
  - [📸 Output Examples \& Sample Screenshots](#-output-examples--sample-screenshots)
    - [🔍 Route Search](#-route-search)
    - [🛫 Hub Analytics](#-hub-analytics)
    - [🎯 Simulations](#-simulations)
    - [🤖 Similar Routes AI](#-similar-routes-ai)
  - [🔍 Troubleshooting](#-troubleshooting)
  - [🚀 Contribution \& Extension Ideas](#-contribution--extension-ideas)
  - [📄 License](#-license)
  - [👨‍💻 Contact \& Author](#-contact--author)
---

## Features
- OpenFlights data ingestion (airports, airlines, routes)
- Vector-based similar route search (MariaDB Vector)
- ColumnStore analytics (busiest hubs, delays, passenger loads)
- Disruption simulation (airport closure + alternates)
- Streamlit multi-page UI + optional Flask API

## Repository Layout
See the structured tree in the project brief. Key folders:
- `backend/`: data ingestion, analytics, vector engine, API
- `frontend/`: Streamlit app and pages
- `data/`: raw OpenFlights and processed artifacts
- `scripts/`: schema setup, seeding, exports
- `docs/`: diagrams and deck placeholders

## Setup
1. Install MariaDB with Vector and ColumnStore (or use a server with these plugins).
2. Python 3.10+ recommended. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Configure database via environment variables as needed:
   - `MARIADB_HOST`, `MARIADB_PORT`, `MARIADB_USER`, `MARIADB_PASSWORD`, `MARIADB_DB`
4. Initialize schema and load data:
   ```bash
   python scripts/seed_database.py --all
   ```

## Running
# AirRouteIQ — Airline Network Resilience Recommendation Engine



![AirRouteIQ architecture](frontend/static/images/architecture_diagram.png)

AirRouteIQ is a hackathon-ready prototype for analyzing, visualizing, and simulating airline network resilience. It combines OpenFlights data, MariaDB ColumnStore analytics, and MariaDB Vector embeddings to deliver fast similarity search, hub analytics, and disruption simulations through a Streamlit UI and an optional Flask API.

This README is written to be comprehensive and reproducible for judges and reviewers: it explains the repository structure, why every major file/folder exists, how the system works end-to-end, how MariaDB is used (Vector + ColumnStore), and exactly how to reproduce results from a fresh checkout.




---

## 📊 Project at a Glance

- Input data: OpenFlights datasets (airports, airlines, routes)
- Vector embeddings: semantic descriptions for routes (stored in MariaDB Vector)
- ColumnStore: large analytical tables for fast OLAP-style queries (hubs, passenger stats, risks)
- Frontend: Streamlit multi-page app with pages for Route Search, Hub Analytics, Simulations and AI
- Backend: Flask API exposing analytics endpoints and helper functions (optional; frontend can also read processed CSVs)

Why this design

- Streamlit provides rapid UI iteration and a clean multi-page experience for judges.
- MariaDB ColumnStore enables fast aggregation queries suitable for hub analytics at scale.
- MariaDB Vector (when available) provides vector search where semantic similarity matters (similar-route search).

--

## 🏗️ Repository Structure & Rationale

Top-level layout (abridged):

```
README.md
backend/
   app.py                 # Flask API and HTTP endpoints (optional)
   requirements.txt       # Python deps used by backend and frontend
   analytics/             # Query modules and analytics/reporting logic
   vector_engine/         # Embedding & similarity code (model loader / search helpers)
data/
   raw/                   # Original OpenFlights files used as input
   processed/             # Cleaned CSVs and embeddings (ready for analytics)
frontend/
   streamlit_app.py       # Streamlit entrypoint (pages + layout)
   pages/                 # Per-page UI code (Route Search, Hub Analytics, Simulations, AI)
   static/css/styles.css  # Global UI theme injected at runtime
scripts/
   seed_database.py       # Convenience script to create schema and seed data (calls SQL + loaders)
   setup_mariadb.sql      # SQL schema and ColumnStore/Vector table definitions
docs/
   architecture.png
   ERD.png
```

Why each major file/folder exists (short rationale)

- `backend/app.py` — Provides an optional Flask API used by the Streamlit frontend for search and analytics endpoints. Judges can run the backend to demonstrate separation of concerns (backend does heavy lifting; frontend renders). Running the backend is optional: the frontend will read from `data/processed` when an API isn’t available.

- `backend/analytics/*.py` — Encapsulates SQL queries, hub scoring, and disruption-simulation logic. These modules produce the numbers and charts you see in the UI.

- `backend/vector_engine/` — Contains the code to create text descriptions for each route, embed them with a sentence-transformers model, and persist embeddings. Files:
   - `model_loader.py` — loads a sentence-transformer model (offline friendly)
   - `embed_routes.py` — creates embeddings for routes and writes CSV or pushes into MariaDB vector table
   - `similarity_search.py` — local nearest-neighbor helpers (fallback) and MariaDB Vector query wiring

- `data/processed/embeddings.csv` — The generated embeddings for routes (used by fallback search and for seeding the MariaDB vector table). This is a key output artifact: judges can inspect this CSV to see the route text and vector columns.

- `frontend/streamlit_app.py` — Streamlit entry; responsible for page layout, applying the global theme (injects `styles.css`), and rendering hero/metrics/footer. It also wires safe navigation for Streamlit pages.

- `frontend/pages/*` — The interactive pages. They call backend APIs (if available) via `frontend.utils.helpers.api_get` or operate directly on `data/processed` for a fully offline demo.

- `scripts/seed_database.py` + `scripts/setup_mariadb.sql` — Schema creation and sample data seeding (ColumnStore table creation, route_embeddings vector table). Use these to reproduce the MariaDB state required for full demos.

--

## ⚙️ How It Works — Data Pipeline & Runtime Flow

1. Data ingestion
    - The repository includes OpenFlights source files in `data/raw/` (airlines.dat, airports.dat, routes.dat).
    - `data_ingestion/` helpers parse these files and produce cleaned CSVs in `data/processed/`.

2. Embedding generation (semantic layer)
    - `backend/vector_engine/embed_routes.py` builds a short description for each route (e.g., "JFK → LHR, daily long-haul transatlantic service") and computes an embedding using a SentenceTransformers model.
    - Embeddings are written to `data/processed/embeddings.csv` and can be optionally inserted into MariaDB's `route_embeddings` vector table.

3. Database & analytics
    - `scripts/setup_mariadb.sql` defines ColumnStore tables (airports, airlines, routes, passenger_stats, delay_risks) and a `route_embeddings` VECTOR column when MariaDB Vector is available.
    - ColumnStore is used for large-scale aggregations and analytical queries (e.g., busiest hubs, passenger distributions, delay risk summaries).
    - When MariaDB Vector is enabled, vector similarity queries are executed server-side for high-performance semantic search.

4. Runtime (UI)
    - The Streamlit frontend (`frontend/streamlit_app.py` and `frontend/pages/*`) renders pages and calls either the Flask backend (`backend/app.py`) or local CSV files for data.
    - Key UI features:
       - Route Search: semantic search over routes (vector search when available, fallback to nearest neighbor over `embeddings.csv`)
       - Hub Analytics: aggregation views powered by ColumnStore queries
       - Simulations: run synthetic disruptions and visualize alternate routings and risk impact

--

## 🗄️ MariaDB: What We Use and Why

- ColumnStore (MariaDB ColumnStore)
   - Purpose: scale analytical queries (OLAP), store large passenger statistics and route tables, and perform fast aggregations across millions of rows.
   - Where: `scripts/setup_mariadb.sql` uses `ENGINE=ColumnStore` for tables intended for analytics (airports, airlines, routes, passenger_stats, delay_risks).

- MariaDB Vector (plugin)
   - Purpose: store vector embeddings (VECTOR datatype) and perform efficient approximate nearest neighbor (ANN) or cosine-similarity queries directly in the database. This avoids shipping embeddings to the app and allows DB-side indexing/optimization.
   - Where: `route_embeddings` table in `setup_mariadb.sql` contains a `VECTOR(384)` column (384 is an example embedding size matching the embedding model). If Vector is not available, the project falls back to storing embeddings in CSV and running an in-memory nearest-neighbor search.

Notes about MariaDB setup

- ColumnStore and Vector are plugins/features of MariaDB; installing/configuring them depends on your MariaDB distribution. See `scripts/setup_mariadb.sql` for required tables. The project will work in a degraded mode (CSV + in-memory search) if Vector/ColumnStore are not available locally — this is useful for hackathon judges who may not have DB admin privileges.

--

## 🚀 Quick Start — Download to Running

Minimum requirements

- Python 3.10+ (3.11/3.12 also supported)
- MariaDB server with ColumnStore & Vector (optional — the app falls back to CSVs)
- ~2–4 GB RAM for small local demos; more for large datasets

Step-by-step (recommended for judges)

1. Clone the repo

```bash
git clone https://github.com/ishansurdi/Airline-Network-Resilience-Recommendation-Engine.git
cd Airline-Network-Resilience-Recommendation-Engine
```

2. Create a virtual environment and install dependencies

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

macOS / Linux:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

3. (Optional) Prepare MariaDB

- If you have a MariaDB server with ColumnStore and Vector installed, run the SQL schema:

```bash
# adjust host/credentials as needed (see environment variables below)
mysql -u <user> -p < scripts/setup_mariadb.sql
```

4. Seed small demo data (optional but recommended)

```bash
python scripts/seed_database.py --sample
```

The `--sample` argument loads a small subset suitable for a fast demo. For full ingestion, use `--all` (requires time and a larger dataset).

5. Run the backend API (optional)

```bash
# from the repository root
python backend/app.py
```

Alternatively, you can run with the module flag:
```bash
python -m backend.app
```

6. Run the Streamlit frontend

```powershell
streamlit run frontend/streamlit_app.py
```

7. Point the frontend to the backend (if using the API)

By default the frontend expects the API at `http://localhost:8000`. You may change it by setting an environment variable before launching Streamlit:

Windows PowerShell:
```powershell
$env:AIRROUTEIQ_API = 'http://localhost:8000'
streamlit run frontend/streamlit_app.py
```

macOS / Linux:
```bash
export AIRROUTEIQ_API='http://localhost:8000'
streamlit run frontend/streamlit_app.py
```

--

## 🔧 Configuration & Environment Variables

- `MARIADB_HOST` — MariaDB host (default: `localhost`)
- `MARIADB_PORT` — MariaDB port (default: `3306`)
- `MARIADB_USER` — DB user
- `MARIADB_PASSWORD` — DB password
- `MARIADB_DB` — DB name (default: `airrouteiq`)
- `AIRROUTEIQ_API` — Base URL for Flask API (default `http://localhost:8000`)
- `AIRROUTEIQ_DEV` — Set to `1` to enable developer warnings in the UI

Put these in a `.env` file or export them in your shell. The backend reads these variables via `python-dotenv` if present.

--

## 📸 Output Examples & Sample Screenshots

The UI produces several visual outputs that are central to the demo. Below are brief descriptions of each screen, why the output matters, and a sample screenshot — replace the sample images with real screenshots from your local run for final submission.

### 🔍 Route Search

- What it does: semantic and attribute-based search across routes. Users can search by source/destination city, airline, volume, and natural-language descriptions ("transatlantic daily service"). When MariaDB Vector is available, results are returned via a DB-side vector similarity query; otherwise the app falls back to nearest-neighbor search on `data/processed/embeddings.csv`.
- Why we need it: helps analysts find similar services, identify redundant links, and discover potential new city-pair matches. Useful for scenario planning and network growth.

![Route Search sample](output_logo_images/RS-1.PNG)
![Route Search sample](output_logo_images/RS-2.PNG)

Output artifacts produced: ranked route table, embedding similarity scores, and a small map/snippet showing route geometry.

### 🛫 Hub Analytics

- What it does: aggregates passenger volumes, computes hub centrality (connectivity), and highlights congestion/risk metrics per airport. Uses ColumnStore queries for fast aggregation across large tables (`passenger_stats`, `routes`).
- Why we need it: identifies critical airports to prioritize for resilience investments and capacity upgrades. Judges can see which hubs contribute most to network connectivity and where single-point failures live.

![Hub Analytics sample](output_logo_images/HA-1.PNG)
![Hub Analytics sample](output_logo_images/HA-2.PNG)

Output artifacts produced: ranked hub table, interactive charts (time-series, top inbound/outbound routes), and downloadable CSV of hub metrics.

### 🎯 Simulations

- What it does: runs disruption scenarios (e.g., airport closure, weather event) and simulates flight reroutes, passenger displacement, and aggregate delay impacts. Visualizes results on maps and summary tables.
- Why we need it: demonstrates the system's capability to stress-test the network and estimate operational impacts under disruptions — essential for resilience planning and contingency budgeting.

![Simulations sample](output_logo_images/SM-1.PNG)

Output artifacts produced: alternative routing lists, aggregated delay/risk numbers, and scenario comparison visualizations.

### 🤖 Similar Routes AI

- What it does: uses vector embeddings to find routes that are semantically similar (e.g., similar city pairs, market characteristics, or service profiles), enabling quick discovery of comparable services.
- Why we need it: helps planners find comparable routes for benchmarking, estimating demand or pricing, and proposing network expansions based on similar markets.

![Similar Routes AI sample](output_logo_images/SR-1.PNG)

Output artifacts produced: per-route similarity lists (with scores), nearest-neighbor visualizations, and an option to export similar-route bundles for downstream analysis.

--

## 🔍 Troubleshooting

- ModuleNotFoundError / ImportError when running Streamlit:
   - Always run `streamlit run frontend/streamlit_app.py` from the repository root. Many import issues come from running files as scripts from subfolders. If you must run from elsewhere, add the project root to `PYTHONPATH` or use the `-m` module flag.

- MariaDB Vector/ColumnStore not available:
   - The app falls back to a CSV + in-memory nearest-neighbor search. You can still demo functionality, but server-side vector indexing will be unavailable.

- Port conflicts:
   - Flask default is `8000` in this project; change `AIRROUTEIQ_API` if your host is already serving on that port.

--

## 🚀 Contribution & Extension Ideas

- Add authentication and user profiles to save query presets.
- Support incremental embedding (only new/changed routes) and DB-side indexing tuning for MariaDB Vector.
- Distributed seeding into ColumnStore for larger datasets.

--

## 📄 License

This repository includes code and assets intended for hackathon submission. You may choose an open source license for the final project — MIT is a common choice. Add a `LICENSE` file if you want to make the project open-source.

--

## 👨‍💻 Contact & Author

Ishan Surdi — Developer & maintainer

Connect with me:

[![GitHub](https://img.shields.io/badge/GitHub-ishansurdi-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ishansurdi)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/your-linkedin/)
[![Website](https://img.shields.io/badge/Website-Visit-orange?style=for-the-badge&logo=google-chrome&logoColor=white)](https://yourwebsite.example)

I built this to showcase how database-native vector search and ColumnStore analytics can supercharge airline network planning and resilience analysis. If you'd like, I can help prepare the presentation slides or live demo script for the hackathon.
