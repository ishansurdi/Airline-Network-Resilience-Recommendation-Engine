from __future__ import annotations
from typing import Any, Dict, Optional

import os
import requests
import streamlit as st
import streamlit.components.v1 as components


def api_get(base_url: str, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    url = base_url.rstrip("/") + path
    resp = requests.get(url, params=params or {}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def apply_global_theme() -> None:
    try:
        frontend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        css_path = os.path.join(frontend_dir, "static", "css", "styles.css")
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception:
        pass

def try_switch_page(page_path: str) -> bool:
    """Try to programmatically switch to a page by its file path.

    Returns True if the switch succeeded, False otherwise (e.g., older Streamlit).
    """
    try:
        # Available in newer Streamlit versions
        st.switch_page(page_path)
        return True
    except Exception:
        return False


def safe_page_link(page_path: str, label: str, icon: Optional[str] = None) -> None:
    """Render a link or a button that switches pages as fallback."""
    try:
        # Available in Streamlit 1.25+
        st.page_link(page_path, label=label, icon=icon)
    except Exception:
        if st.button(f"{icon or ''} {label}"):
            try_switch_page(page_path)


def render_navbar(active: str = "home") -> None:
    """Injected via HTML in main page now, so no buttons needed."""
    pass


def render_footer() -> None:
    st.markdown("""
    <footer class="air-footer">
      <div style="padding: 5rem 0;"></div>
      <div class="air-footer__content">
        <div style="margin-left: 20rem;"> &copy; Airline Network Resilience Recommendation Engine - 2025</div>
      </div>
    </footer>
    """, unsafe_allow_html=True)


def inject_nav_js() -> None:
    components.html("""
    <script>
    (function(){
      const blocks = parent.document.querySelectorAll('.block-container > div');
      if(!blocks.length) return;
      const nav = blocks[0];
      nav.classList.add('air-navbar');
      const onScroll = () => {
        if(parent.window.scrollY > 4) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
      };
      parent.window.addEventListener('scroll', onScroll, {passive:true});
      onScroll();
    })();
    </script>
    """, height=0)