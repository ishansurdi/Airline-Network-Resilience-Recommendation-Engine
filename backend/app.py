from __future__ import annotations
import os
import sys
from flask import Flask, jsonify, request

# Ensure the project root (one level up from this backend folder) is on sys.path
# so imports like `from backend.analytics...` work when running scripts from inside
# the `backend/` directory (for example: `streamlit run app.py`).
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)

# Import helper modules. Prefer relative imports when `backend` is a package,
# but if this file is executed as a top-level script (Streamlit often does this),
# fall back to inserting the project root and using absolute imports.
try:
    from .analytics.hub_analysis import busiest_hubs, top_city_pairs_by_frequency, hub_load_and_delay
    from .analytics.disruption_simulation import simulate_airport_closure, suggest_alternate_routes
    from .vector_engine.similarity_search import similar_routes_by_route_id, similar_routes_by_text
except (ImportError, ValueError):
    # Add project root to sys.path and import using package-style names
    if _PROJECT_ROOT not in sys.path:
        sys.path.insert(0, _PROJECT_ROOT)
    from backend.analytics.hub_analysis import busiest_hubs, top_city_pairs_by_frequency, hub_load_and_delay
    from backend.analytics.disruption_simulation import simulate_airport_closure, suggest_alternate_routes
    from backend.vector_engine.similarity_search import similar_routes_by_route_id, similar_routes_by_text

app = Flask(__name__)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hubs/busiest")
def hubs_busiest():
    limit = int(request.args.get("limit", 20))
    df = busiest_hubs(limit=limit)
    return jsonify(df.to_dict(orient="records"))


@app.get("/routes/top-city-pairs")
def routes_top_city_pairs():
    limit = int(request.args.get("limit", 20))
    df = top_city_pairs_by_frequency(limit=limit)
    return jsonify(df.to_dict(orient="records"))


@app.get("/hubs/load-delay")
def hubs_load_delay():
    limit = int(request.args.get("limit", 50))
    df = hub_load_and_delay(limit=limit)
    return jsonify(df.to_dict(orient="records"))


@app.get("/simulate/closure")
def simulate_closure():
    airport_id = int(request.args["airport_id"])  # required
    df = simulate_airport_closure(airport_id)
    return jsonify(df.to_dict(orient="records"))


@app.get("/simulate/alternates")
def simulate_alternates():
    airport_id = int(request.args["airport_id"])  # required
    top_k = int(request.args.get("top_k", 10))
    df = suggest_alternate_routes(airport_id, top_k=top_k)
    return jsonify(df.to_dict(orient="records"))


@app.get("/similar/by-route")
def similar_by_route():
    route_id = int(request.args["route_id"])  # required
    top_k = int(request.args.get("top_k", 10))
    df = similar_routes_by_route_id(route_id, top_k=top_k)
    return jsonify(df.to_dict(orient="records"))


@app.get("/similar/by-text")
def similar_by_text():
    query = request.args.get("q", "")
    top_k = int(request.args.get("top_k", 10))
    df = similar_routes_by_text(query, top_k=top_k)
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
