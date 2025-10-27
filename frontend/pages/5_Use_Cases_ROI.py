from __future__ import annotations
import streamlit as st

from frontend.utils.helpers import apply_global_theme, render_navbar, render_footer, inject_nav_js

st.set_page_config(page_title="Use Cases & ROI", page_icon="📈", layout="wide")
render_navbar(active="usecases")
inject_nav_js()
apply_global_theme()

st.title("Use Cases & ROI")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Airline Network Planning")
    st.markdown(
        "- Identify underserved city pairs\n"
        "- Prioritize frequency increases\n"
        "- Evaluate seasonal opportunities"
    )
with col2:
    st.subheader("Operations & Resilience")
    st.markdown(
        "- Stress-test hub closures\n"
        "- Quantify spillover and alternates\n"
        "- Minimize passenger disruption"
    )

st.divider()

st.subheader("ROI Scenarios")
roi1, roi2, roi3 = st.columns(3)
with roi1:
    st.metric("+1% Load Factor", "$2.4M / year")
with roi2:
    st.metric("-5% Delay Minutes", "$1.1M / year")
with roi3:
    st.metric("+2 Routes Added", "$3.6M / year")

st.caption("Illustrative estimates. Connect to real data for precise ROI.")
st.write("")
render_footer()
