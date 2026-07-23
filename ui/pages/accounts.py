import streamlit as st

from utils.queries import get_accounts


st.title("👤 Account Explorer")

accounts = get_accounts()

if accounts.empty:
    st.warning("No accounts found.")
    st.stop()

# ------------------------------------
# Filters
# ------------------------------------

st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:

    search = st.text_input(
        "Search Account",
        placeholder="Enter account name..."
    )

with col2:

    verified_only = st.checkbox(
        "Verified Accounts Only"
    )

if search:

    accounts = accounts[
        accounts["account_name"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

if verified_only:

    accounts = accounts[
        accounts["is_verified"] == True
    ]

# ------------------------------------
# Sorting
# ------------------------------------

sort_by = st.selectbox(
    "Sort By",
    [
        "followers_count",
        "account_name",
        "first_seen",
        "last_updated"
    ]
)

ascending = st.toggle(
    "Ascending Order",
    value=False
)

accounts = accounts.sort_values(
    sort_by,
    ascending=ascending
)

# ------------------------------------
# Metrics
# ------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Accounts",
        len(accounts)
    )

with col2:

    st.metric(
        "Verified",
        int(accounts["is_verified"].sum())
    )

with col3:

    st.metric(
        "Followers",
        f"{accounts['followers_count'].sum():,}"
    )

st.divider()

# ------------------------------------
# Display Table
# ------------------------------------

display = accounts.copy()

display["is_verified"] = display["is_verified"].map(
    {
        True: "✅",
        False: ""
    }
)

display = display.rename(
    columns={
        "account_name": "Account",
        "followers_count": "Followers",
        "is_verified": "Verified",
        "first_seen": "First Seen",
        "last_updated": "Last Updated"
    }
)

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True
)