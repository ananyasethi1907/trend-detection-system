import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Instagram Trend Detection",
    layout="wide",
    initial_sidebar_state="expanded"
)

css_path = Path(__file__).parent / "assets" / "style.css"

if css_path.exists():
    with open(css_path) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

st.title("Instagram Trend Detection")

st.markdown(
"""
Welcome to the **Instagram Trend Detection Dashboard**.

Use the navigation panel on the left to explore:

- Dashboard
- Trends
- Topics
- Posts
- Accounts
- Pipeline
- Analytics
"""
)
