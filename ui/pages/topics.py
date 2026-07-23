import streamlit as st

from utils.queries import get_topics

st.title("🏷️ Topic Explorer")

topics = get_topics()

if topics.empty:
    st.warning("No topics found.")
    st.stop()

# ----------------------------
# Filters
# ----------------------------

st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:

    search = st.text_input(
        "Search Topic",
        placeholder="Enter topic name..."
    )

with col2:

    category = st.selectbox(
        "Category",
        ["All"] + sorted(
            topics["category"]
            .dropna()
            .unique()
            .tolist()
        )
    )

# ----------------------------
# Apply Filters
# ----------------------------

if search:

    topics = topics[
        topics["canonical_name"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

if category != "All":

    topics = topics[
        topics["category"] == category
    ]

# ----------------------------
# Statistics
# ----------------------------

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Topics",
        len(topics)
    )

with col2:

    st.metric(
        "Categories",
        topics["category"].nunique()
    )

st.divider()

# ----------------------------
# Table
# ----------------------------

display = topics.copy()

display = display.rename(
    columns={
        "canonical_name": "Topic",
        "category": "Category",
        "first_detected": "First Detected",
        "last_active": "Last Active",
        "inactive_count": "Inactive Count"
    }
)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True
)