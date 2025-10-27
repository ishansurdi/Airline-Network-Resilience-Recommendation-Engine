# AirRouteIQ - Intelligent Airline Network Analytics (MariaDB)

Prototype web app for analyzing and simulating airline network resilience using MariaDB Vector and ColumnStore. Built for the MariaDB Python Hackathon.

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
- Start Flask API:
  ```bash
  python backend/app.py
  ```
- Start Streamlit UI:
  ```bash
  streamlit run frontend/streamlit_app.py
  ```
Set `AIRROUTEIQ_API` env to point Streamlit to the Flask API base URL (default `http://localhost:8000`).

## Notes
- If MariaDB Vector is unavailable, text search fallback is provided for similarity by text.
- This is a prototype: synthetic passenger and risk data should be generated/loaded for richer analytics.
