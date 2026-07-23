import streamlit as st
import pandas as pd

from utils.queries import (
    get_topics,
    get_trends,
    get_accounts,
    get_latest_posts,
)

st.title("📊 Analytics Dashboard")

topics = get_topics()
trends = get_trends(100)
accounts = get_accounts()
posts = get_latest_posts(500)

# -------------------------
# Overview Metrics
# -------------------------

st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Topics", len(topics))

with col2:
    st.metric("Trends", len(trends))

with col3:
    st.metric("Accounts", len(accounts))

with col4:
    st.metric("Posts", len(posts))

st.divider()

# -------------------------
# Topic Categories
# -------------------------

st.subheader("🏷️ Topic Categories")

if (
    not topics.empty
    and "category" in topics.columns
):
    category_counts = (
        topics["category"]
        .fillna("Unknown")
        .value_counts()
    )

    st.bar_chart(category_counts)

else:
    st.info("No category data available.")

st.divider()

# -------------------------
# Trend Scores
# -------------------------

st.subheader("📈 Top Trend Scores")

if (
    not trends.empty
    and "Trend Score" in trends.columns
):
    chart = (
        trends[
            ["Topic", "Trend Score"]
        ]
        .head(10)
        .set_index("Topic")
    )

    st.bar_chart(chart)

else:
    st.info("No trend score data available.")

st.divider()

# -------------------------
# Top Accounts
# -------------------------

st.subheader("👤 Top Accounts")

if (
    not accounts.empty
    and "followers_count" in accounts.columns
):
    chart = (
        accounts[
            ["account_name", "followers_count"]
        ]
        .sort_values(
            "followers_count",
            ascending=False
        )
        .head(10)
        .set_index("account_name")
    )

    st.bar_chart(chart)

else:
    st.info("No account data available.")

st.divider()

# -------------------------
# Likes vs Comments
# -------------------------

st.subheader("❤️ Likes vs 💬 Comments")

if (
    not posts.empty
    and {"likes", "comments"}.issubset(posts.columns)
):
    scatter = pd.DataFrame(
        {
            "Likes": posts["likes"],
            "Comments": posts["comments"]
        }
    )

    st.scatter_chart(scatter)

else:
    st.info("No engagement data available.")

st.divider()

# -------------------------
# Posting Activity
# -------------------------

st.subheader("📅 Posting Activity")

if (
    not posts.empty
    and "published_at" in posts.columns
):
    activity = posts.copy()

    activity["published_at"] = pd.to_datetime(
        activity["published_at"],
        errors="coerce"
    )

    activity = (
        activity
        .dropna(subset=["published_at"])
        .groupby(
            activity["published_at"].dt.date
        )
        .size()
    )

    st.line_chart(activity)

else:
    st.info("No publishing history available.")

st.divider()

# -------------------------
# Dataset Summary
# -------------------------

st.subheader("📌 Dataset Summary")

st.write(f"**Total Topics:** {len(topics):,}")
st.write(f"**Total Trends:** {len(trends):,}")
st.write(f"**Total Accounts:** {len(accounts):,}")
st.write(f"**Total Posts:** {len(posts):,}")

if not posts.empty and "likes" in posts.columns:
    st.write(f"**Average Likes:** {posts['likes'].mean():.0f}")

if not posts.empty and "comments" in posts.columns:
    st.write(f"**Average Comments:** {posts['comments'].mean():.0f}")

if not accounts.empty and "followers_count" in accounts.columns:
    st.write(
        f"**Average Followers:** {accounts['followers_count'].mean():,.0f}"
    )