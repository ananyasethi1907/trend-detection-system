import streamlit as st

from utils.queries import get_trends

st.title("📈 Trend Explorer")

trends = get_trends(100)

if trends.empty:
    st.warning("No trend data available.")
    st.stop()

st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:
    search = st.text_input(
        "Search Topic",
        placeholder="Enter topic name..."
    )

with col2:
    window = st.selectbox(
        "Time Window",
        ["All"] + sorted(trends["Window"].dropna().unique().tolist())
    )

if search:
    trends = trends[
        trends["Topic"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

if window != "All":
    trends = trends[
        trends["Window"] == window
    ]

sort_by = st.selectbox(
    "Sort By",
    [
        "Trend Score",
        "Momentum",
        "Growth Rate"
    ]
)

ascending = st.toggle(
    "Ascending Order",
    value=False
)

trends = trends.sort_values(
    sort_by,
    ascending=ascending
)

st.markdown(f"### {len(trends)} Trending Topics")

st.dataframe(
    trends,
    use_container_width=True,
    hide_index=True
)

st.subheader("Top 10 Trends")

chart = (
    trends[
        ["Topic", "Trend Score"]
    ]
    .head(10)
    .set_index("Topic")
)

st.bar_chart(
    chart,
    use_container_width=True
)