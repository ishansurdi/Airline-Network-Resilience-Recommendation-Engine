from __future__ import annotations
import os
import streamlit as st

# Import helpers robustly
try:
    import frontend.utils.helpers as _helpers
except Exception:
    import sys
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    _PROJECT_ROOT = os.path.dirname(_THIS_DIR)
    if _PROJECT_ROOT not in sys.path:
        sys.path.insert(0, _PROJECT_ROOT)
    import frontend.utils.helpers as _helpers

# Bind helper functions
def _bind(name: str):
    try:
        return getattr(_helpers, name)
    except AttributeError:
        raise ImportError(f"frontend.utils.helpers is missing '{name}'")

apply_global_theme = _bind("apply_global_theme")
render_navbar = _bind("render_navbar")
render_footer = _bind("render_footer")
inject_nav_js = _bind("inject_nav_js")

# Streamlit Config
st.set_page_config(
    page_title="Airline Network Resilience Recommendation Engine ✈️ | Airline Network Resilience Recommendation Engine",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply theming & UI components
apply_global_theme()
render_navbar(active="home")
inject_nav_js()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.text_input(
        "Backend API Base URL",
        value=os.getenv("AIRROUTEIQ_API", "http://localhost:8000"),
        key="api_base",
    )

# ---------- HERO SECTION ----------
st.markdown("""
<div class="page-container">

  <section class="hero">
    <h1>Airline Network Resilience Recommendation Engine</h1>
    <p class="sub">
      Intelligent analytics for airline network design, risk, and growth.
    </p>
    <div class="spacer"></div>
    <p class="muted">Powered by <strong>MariaDB Vector + ColumnStore</strong></p>
    <div class="muted">Developed by <a href="https://github.com/ishansurdi" target="_blank">Ishan Surdi</a></div>
  </section>

  <!-- METRICS -->
  <section class="metrics-cards">
    <div class="metric-card"><h2>3.2M+</h2><p>Routes</p></div>
    <div class="metric-card"><h2>3.3K</h2><p>Airports</p></div>
    <div class="metric-card"><h2>150+</h2><p>Hubs analyzed</p></div>
    <div class="metric-card"><h2>&lt; 300ms</h2><p>Avg. Query Latency</p></div>
  </section>

  <!-- CTA CARDS -->
  <section class="cta-cards">
    <div class="cta-card">
      <h3>Route Search</h3>
      <p>Explore connectivity, volumes, and top city pairs</p>
      <a href="frontend/pages/1_Route_Search.py" class="btn-primary">Open Route Search</a>
    </div>

    
  </section>

  <hr class="divider"/>

  <!-- WHY SECTION -->
  <section class="why">
    <h2>Why AirRouteIQ?</h2>
    <div class="cols">
      <ul>
        <li>Optimize network design with data-driven insights</li>
        <li>Quantify hub resilience and delay risk</li>
        <li>Accelerate planning with vector search over route semantics</li>
      </ul>
      <ul>
        <li>Built for analysts, planners, and ops teams</li>
        <li>SQL-friendly backend, fast APIs</li>
        <li>Secure deployment-ready architecture</li>
      </ul>
    </div>
  </section>

  <div class="info-tip">💡 Tip: Set your API base URL in the sidebar to connect to your backend.</div>

</div>
""", unsafe_allow_html=True)

render_footer()
