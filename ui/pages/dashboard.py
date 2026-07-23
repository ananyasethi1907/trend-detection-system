import streamlit as st

from utils.queries import (
    get_dashboard_stats,
    get_trends,
    get_latest_posts,
)

from components.metrics import show_dashboard_metrics
from components.charts import show_trend_chart
from components.tables import show_trends_table


st.title("🏠 Dashboard")

# --------------------------
# Load Data
# --------------------------

stats = get_dashboard_stats()
trends_df = get_trends()
posts_df = get_latest_posts()

# --------------------------
# Metrics
# --------------------------

top_trend = "-"

if not trends_df.empty:
    top_trend = trends_df.iloc[0]["Topic"]

show_dashboard_metrics(
    stats,
    top_trend
)

st.divider()

# --------------------------
# Trend Chart
# --------------------------

show_trend_chart(trends_df)

st.divider()

# --------------------------
# Trending Topics
# --------------------------

show_trends_table(trends_df)

st.divider()

# --------------------------
# Latest Posts
# --------------------------

st.subheader("📝 Latest Posts")

if posts_df.empty:

    st.info("No posts found.")

else:

    display = posts_df.copy()

    display["caption"] = (
        display["caption"]
        .fillna("")
        .str.slice(0, 120)
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )