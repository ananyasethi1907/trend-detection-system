import streamlit as st

from utils.queries import get_latest_posts


st.title("📝 Post Explorer")

posts = get_latest_posts(100)

if posts.empty:
    st.warning("No posts found.")
    st.stop()

# --------------------------------
# Filters
# --------------------------------

st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:

    search = st.text_input(
        "Search Caption",
        placeholder="Search by caption..."
    )

with col2:

    min_likes = st.number_input(
        "Minimum Likes",
        min_value=0,
        value=0,
        step=100
    )

if search:

    posts = posts[
        posts["caption"]
        .fillna("")
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

posts = posts[
    posts["likes"] >= min_likes
]

# --------------------------------
# Sorting
# --------------------------------

sort_by = st.selectbox(
    "Sort By",
    [
        "published_at",
        "likes",
        "comments",
        "views"
    ]
)

ascending = st.toggle(
    "Ascending Order",
    value=False
)

posts = posts.sort_values(
    sort_by,
    ascending=ascending
)

# --------------------------------
# Metrics
# --------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Posts",
        len(posts)
    )

with col2:

    st.metric(
        "Total Likes",
        f"{posts['likes'].sum():,}"
    )

with col3:

    st.metric(
        "Average Likes",
        f"{posts['likes'].mean():.0f}"
    )

st.divider()

# --------------------------------
# Display Table
# --------------------------------

display = posts.copy()

display["caption"] = (
    display["caption"]
    .fillna("")
    .str.replace("\n", " ", regex=False)
    .str.slice(0, 120)
)

display = display.rename(
    columns={
        "post_id": "Post ID",
        "caption": "Caption",
        "likes": "Likes",
        "comments": "Comments",
        "views": "Views",
        "published_at": "Published At"
    }
)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True
)