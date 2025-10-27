from __future__ import annotations
import os
import pandas as pd
import plotly.express as px
import streamlit as st

from frontend.utils.helpers import api_get, apply_global_theme, render_navbar, render_footer, inject_nav_js

render_navbar(active="hubs")
inject_nav_js()
st.title("Hub Analytics")
apply_global_theme()
api_base = st.session_state.get("api_base", os.getenv("AIRROUTEIQ_API", "http://localhost:8000"))

st.caption("Benchmark hubs by connectivity, passenger load, and delay risk.")

metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    st.metric("Global hubs analyzed", "150")
with metric_col2:
    st.metric("Avg. degree", "48")
with metric_col3:
    st.metric("Avg. delay (min)", "14.2")

tab_busiest, tab_delay = st.tabs(["Busiest Hubs", "Load & Delay"])

with tab_busiest:
    st.subheader("Busiest Hubs (by degree)")
    col1, col2 = st.columns([2, 1])
    with col2:
        limit = st.slider("How many hubs?", 5, 50, 20, key="hubs_limit")
    try:
        df = pd.DataFrame(api_get(api_base, "/hubs/busiest", {"limit": limit}))
        st.dataframe(df, use_container_width=True)
        if not df.empty:
            fig = px.bar(df, x="name", y="degree", color="country", title="Busiest Hubs")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to fetch hubs: {e}")

with tab_delay:
    st.subheader("Hub Load and Delay")
    col1, col2 = st.columns([2, 1])
    with col2:
        limit2 = st.slider("How many entries?", 5, 100, 50, key="load_limit")
    try:
        df2 = pd.DataFrame(api_get(api_base, "/hubs/load-delay", {"limit": limit2}))
        st.dataframe(df2, use_container_width=True)
        if not df2.empty:
            fig2 = px.scatter(
                df2,
                x="total_passengers",
                y="avg_delay",
                hover_name="name",
                color="country",
                title="Passengers vs Average Delay",
            )
            st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to fetch load/delay: {e}")
st.write("")
render_footer()
