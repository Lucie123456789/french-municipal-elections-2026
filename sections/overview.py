import streamlit as st
from utils.styles import insight

def show_overview(df, raw_df=None):
    st.header("Election Overview")

    # Calculate KPIs
    total_registered = df["inscrits"].sum()
    total_voters = df["votants"].sum()

    if total_registered > 0:
        turnout_rate = total_voters / total_registered * 100
        abstention_rate = 100 - turnout_rate
    else:
        turnout_rate = 0
        abstention_rate = 0

    st.write(
        f"In the selected areas, **{turnout_rate:.2f}%** "
        "of registered voters participated. "
        "But was participation the same everywhere ?"
    )

    # Display KPIs
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        with st.container(border=True):
            st.metric("Registered Voters", f"{total_registered:,}")

    with c2:
        with st.container(border=True):
            st.metric("Total Voters", f"{total_voters:,}")

    with c3:
        with st.container(border=True):
            st.metric("Turnout Rate", f"{turnout_rate:.2f}%")

    with c4:
        with st.container(border=True):
            st.metric("Abstention Rate", f"{abstention_rate:.2f}%")

    # Overview insight
    if total_registered > 0:
        insight(
            f"Across the French areas covered by the dataset, "
            f"{turnout_rate:.2f}% of registered voters participated, "
            f"while {abstention_rate:.2f}% abstained. "
            f"But this does not show how "
            f"participation differs between municipalities "
            f"and departments."
        )

    # Information to explore the dashboard
    st.caption(
        "Use the filters in the left sidebar to explore "
        "voter participation by department or municipality."
    )

    # Reduce KPI number size
    st.markdown(
        """
        <style>
        div[data-testid="stMetricValue"] {
            font-size: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    st.subheader("Data Quality & Dataset Preview")

    # Dataset preview
    with st.expander("Dataset Preview"):
        st.write("First five rows :")
        st.dataframe(df.head(), use_container_width=True)

        st.write(f"Number of rows : {df.shape[0]}")
        st.write(f"Number of columns : {df.shape[1]}")

    # Check original data
    quality_df = raw_df if raw_df is not None else df

    # Missing values
    with st.expander("Missing Values"):
        missing = quality_df.isnull().sum()
        missing = missing[missing > 0]

        if missing.empty:
            st.success("No missing values found.")
        else:
            st.dataframe(
                missing.rename("Missing Values"),
                use_container_width=True
            )

    # Duplicate rows
    with st.expander("Duplicate Rows"):
        duplicates = quality_df.duplicated().sum()
        st.metric("Duplicate Rows", int(duplicates))

    # Validation checks
    with st.expander("Validation Checks"):
        invalid_votes = (
            (quality_df["inscrits"] <= 0) |
            (quality_df["votants"] < 0) |
            (quality_df["votants"] > quality_df["inscrits"])
        ).sum()

        st.metric("Invalid Voting Records", int(invalid_votes))

    # Cleaning summary
    with st.expander("Data Cleaning Summary"):
        original_rows = len(quality_df)
        cleaned_rows = len(df)

        st.write(f"Original rows : {original_rows:,}")
        st.write(f"Rows in current selection : {cleaned_rows:,}")

        st.caption(
            "Some rows were removed during data cleaning. "
            "Sidebar filters can further reduce the displayed data."
        )