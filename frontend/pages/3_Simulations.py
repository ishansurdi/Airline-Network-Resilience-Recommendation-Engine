from __future__ import annotations
import os
import pandas as pd
import streamlit as st

from frontend.utils.helpers import api_get, apply_global_theme, render_navbar, render_footer, inject_nav_js

render_navbar(active="sims")
inject_nav_js()
st.title("Disruption Simulations")
apply_global_theme()
api_base = st.session_state.get("api_base", os.getenv("AIRROUTEIQ_API", "http://localhost:8000"))

col_a, col_b = st.columns([2, 1])
with col_b:
    airport_id = st.number_input("Airport ID to close", min_value=1, value=507)
    top_k = st.slider("Alternate routes (Top K)", 5, 50, 20)
    run = st.button("Run Simulation")

with col_a:
    if 'impacted_df' not in st.session_state:
        st.session_state['impacted_df'] = pd.DataFrame()
    if 'alternates_df' not in st.session_state:
        st.session_state['alternates_df'] = pd.DataFrame()

    if run:
        try:
            impacted = pd.DataFrame(api_get(api_base, "/simulate/closure", {"airport_id": airport_id}))
            st.session_state['impacted_df'] = impacted
        except Exception as e:
            st.error(f"Failed to simulate closure: {e}")
        try:
            alternates = pd.DataFrame(api_get(api_base, "/simulate/alternates", {"airport_id": airport_id, "top_k": int(top_k)}))
            st.session_state['alternates_df'] = alternates
        except Exception as e:
            st.error(f"Failed to fetch alternates: {e}")

    st.subheader("Impacted Routes")
    st.dataframe(st.session_state['impacted_df'], use_container_width=True)
    st.subheader("Alternate Routes")
    st.dataframe(st.session_state['alternates_df'], use_container_width=True)

st.download_button(
    label="Export Impacted as CSV",
    data=st.session_state['impacted_df'].to_csv(index=False).encode('utf-8'),
    file_name="impacted_routes.csv",
    mime="text/csv",
    disabled=st.session_state['impacted_df'].empty,
)

st.download_button(
    label="Export Alternates as CSV",
    data=st.session_state['alternates_df'].to_csv(index=False).encode('utf-8'),
    file_name="alternate_routes.csv",
    mime="text/csv",
    disabled=st.session_state['alternates_df'].empty,
)

st.write("")
render_footer()
