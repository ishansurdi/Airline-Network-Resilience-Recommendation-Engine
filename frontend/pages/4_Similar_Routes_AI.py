from __future__ import annotations
import os
import pandas as pd
import plotly.express as px
import streamlit as st

from frontend.utils.helpers import api_get, apply_global_theme, render_navbar, render_footer, inject_nav_js

render_navbar(active="ai")
inject_nav_js()
st.title("Similar Routes (AI)")
apply_global_theme()
api_base = st.session_state.get("api_base", os.getenv("AIRROUTEIQ_API", "http://localhost:8000"))

tab_route, tab_text = st.tabs(["By Route ID", "By Text"])

with tab_route:
    col1, col2 = st.columns([1, 2])
    with col1:
        route_id = st.number_input("Route ID", min_value=1, value=1000)
        top_k = st.slider("Top K", 3, 50, 10)
        run = st.button("Find Similar Routes")
    with col2:
        if run:
            try:
                df = pd.DataFrame(api_get(api_base, "/similar/by-route", {"route_id": route_id, "top_k": top_k}))
                st.dataframe(df, use_container_width=True)
                if not df.empty and {'score', 'distance_km'}.issubset(set(df.columns)):
                    fig = px.scatter(df, x="distance_km", y="score", hover_name=df.columns[0])
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Search failed: {e}")
st.write("")
render_footer()

with tab_text:
    col1, col2 = st.columns([1, 2])
    with col1:
        text = st.text_area("Describe the route", value="busy asian hub with high cargo volume")
        top_k_t = st.slider("Top K", 3, 50, 10, key="topk_text")
        run_t = st.button("Search by Text")
    with col2:
        if run_t:
            try:
                df_t = pd.DataFrame(api_get(api_base, "/similar/by-text", {"q": text, "top_k": top_k_t}))
                st.dataframe(df_t, use_container_width=True)
                if not df_t.empty and {'score', 'distance_km'}.issubset(set(df_t.columns)):
                    fig_t = px.scatter(df_t, x="distance_km", y="score", hover_name=df_t.columns[0])
                    st.plotly_chart(fig_t, use_container_width=True)
            except Exception as e:
                st.error(f"Search failed: {e}")
