import streamlit as st


def show_trends_table(df):

    st.subheader("📈 Trending Topics")

    if df.empty:

        st.info("No trend data available.")

        return

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )