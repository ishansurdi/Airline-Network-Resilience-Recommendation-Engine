from __future__ import annotations
import os
import pandas as pd
import plotly.express as px
import streamlit as st
import sys

# --- Import helpers ---
try:
    from frontend.utils.helpers import api_get, apply_global_theme, render_navbar, render_footer, inject_nav_js
except ModuleNotFoundError:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    _PROJECT_ROOT = os.path.dirname(os.path.dirname(_THIS_DIR))
    if _PROJECT_ROOT not in sys.path:
        sys.path.insert(0, _PROJECT_ROOT)
    from frontend.utils.helpers import api_get, apply_global_theme, render_navbar, render_footer, inject_nav_js

# --- Page Config & Theme ---
st.set_page_config(page_title="Route Search", layout="wide")
apply_global_theme()
render_navbar(active="route")
inject_nav_js()

api_base = st.session_state.get("api_base", os.getenv("AIRROUTEIQ_API", "http://localhost:8000"))

# --- Page Container ---
st.markdown('<div class="page-container">', unsafe_allow_html=True)

st.title("Route Search & Connectivity")

# --- Filters ---
with st.expander("Filters", expanded=True):
    colf1, colf2, colf3 = st.columns(3)
    with colf1:
        min_flights = st.number_input("Min flights", 0, 100000, 100)
    with colf2:
        source_q = st.text_input("Source city contains", "")
    with colf3:
        dest_q = st.text_input("Dest city contains", "")
    limit = st.slider("Rows", 10, 1000, 100)

# --- Tabs ---
tab1, tab2 = st.tabs(["Top City Pairs", "By City/Country"])

with tab1:
    st.subheader("Top City Pairs by Frequency")
    try:
        data = api_get(api_base, "/routes/top-city-pairs", {"limit": limit})
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        if not df.empty:
            fig = px.bar(
                df.head(30),
                x="source_city",
                y="flights",
                color="dest_city",
                title="Top City Pairs",
            )
            fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")

with tab2:
    st.subheader("Filter by City Pair")
    try:
        data2 = api_get(api_base, "/routes/top-city-pairs", {"limit": max(limit, 500)})
        df2 = pd.DataFrame(data2)
        if source_q:
            df2 = df2[df2["source_city"].str.contains(source_q, case=False, na=False)]
        if dest_q:
            df2 = df2[df2["dest_city"].str.contains(dest_q, case=False, na=False)]
        if min_flights:
            df2 = df2[df2["flights"] >= int(min_flights)]
        df2 = df2.head(limit)
        st.dataframe(df2, use_container_width=True)
        if not df2.empty:
            fig2 = px.bar(
                df2.head(30),
                x="source_city",
                y="flights",
                color="dest_city",
                title="Filtered City Pairs",
            )
            fig2.update_layout(margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to filter: {e}")

# --- Close Page Container ---
st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.write("")
render_footer()
