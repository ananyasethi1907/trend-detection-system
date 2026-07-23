import streamlit as st


def show_dashboard_metrics(stats, top_trend):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📝 Total Posts",
            value=f"{stats['posts']:,}"
        )

    with col2:
        st.metric(
            label="🏷 Total Topics",
            value=f"{stats['topics']:,}"
        )

    with col3:
        st.metric(
            label="👤 Total Accounts",
            value=f"{stats['accounts']:,}"
        )

    with col4:
        st.metric(
            label="🔥 Top Trend",
            value=top_trend
        )