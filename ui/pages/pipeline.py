import streamlit as st
import subprocess
import sys
import time
from pathlib import Path

from utils.queries import get_dashboard_stats


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def run_script(script_name):

    script_path = SCRIPTS_DIR / script_name

    if not script_path.exists():
        st.error(f"Script not found:\n{script_path}")
        return

    start = time.time()

    with st.spinner(f"Running {script_name}..."):

        module = f"scripts.{Path(script_name).stem}"

        process = subprocess.run(
        [sys.executable, "-m", module],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    runtime = time.time() - start

    if process.returncode == 0:
        st.success(f"Completed in {runtime:.2f} seconds")
    else:
        st.error(f"Execution failed ({runtime:.2f}s)")

    if process.stdout:
        with st.expander("Output", expanded=True):
            st.code(process.stdout)

    if process.stderr:
        with st.expander("Errors", expanded=True):
            st.code(process.stderr)


st.title("⚙️ Pipeline Control Center")

stats = get_dashboard_stats()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Posts", stats["posts"])

with c2:
    st.metric("Topics", stats["topics"])

with c3:
    st.metric("Accounts", stats["accounts"])

st.divider()

st.subheader("Pipeline Actions")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🚀 Run Data Ingestion",
        use_container_width=True
    ):
        run_script("run_ingestion.py")

    if st.button(
        "🧠 Run NLP Pipeline",
        use_container_width=True
    ):
        run_script("run_nlp.py")

with col2:

    if st.button(
        "📈 Calculate Trends",
        use_container_width=True
    ):
        run_script("calculate_trends.py")

    if st.button(
        "🗑 Reset Topics",
        use_container_width=True
    ):
        run_script("reset_topics.py")

st.divider()

st.info(
    """
Run the pipeline in the following order:

1. Data Ingestion
2. NLP Pipeline
3. Calculate Trends

Reset Topics only when starting a fresh analysis.
"""
)