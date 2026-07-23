import streamlit as st


def show_trend_chart(df):
    """
    Display a bar chart of the Top 10 trend scores.
    """

    if df.empty:
        st.info("No trend data available.")
        return

    st.subheader("📊 Top 10 Trend Scores")

    chart_df = (
        df[["Topic", "Trend Score"]]
        .head(10)
        .set_index("Topic")
    )

    st.bar_chart(
        chart_df,
        use_container_width=True
    )