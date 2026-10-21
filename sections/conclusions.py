
import streamlit as st
import pandas as pd

from utils.viz import department_table


def show_conclusions(df, raw_df):
    # 1. Data quality
    st.header("Data Quality & Limitations")
    st.write(
        "Before drawing conclusions, we need to check "
        "the data and understand what it can tell us."
    )

    # Missing values and duplicates
    missing_values = raw_df.isna().sum().sum()
    duplicates = raw_df.duplicated().sum()

    #Missing values in voting columns
    registered = pd.to_numeric(
        raw_df["inscrits"], errors="coerce"
    )
    voters = pd.to_numeric(
        raw_df["votants"], errors="coerce"
    )

    missing_voting = (
        registered.isna().sum()
        + voters.isna().sum()
    )

    # Completely empty columns
    missing_by_column = raw_df.isna().sum()
    empty_columns = missing_by_column[
        missing_by_column == len(raw_df)
    ].index.tolist()

    # Invalid voting records
    invalid_records = (
        (registered <= 0)
        | (voters < 0)
        | (voters > registered)
        | registered.isna()
        | voters.isna()
    ).sum()

    # Quality indicators
    c1, c2, c3 = st.columns(3)

    c1.metric("Missing Values", f"{missing_values:,}")
    c2.metric("Duplicate Rows", f"{duplicates:,}")
    c3.metric("Invalid Records", f"{invalid_records:,}")

    # Quality results
    st.write(
        f"The original dataset contains {missing_values:,} "
        f"empty cells, including {len(empty_columns)} "
        "completely empty columns. "
        f"There are {missing_voting:,} missing or non-numeric "
        "values in the registered-voter and voter columns."
    )

    st.write(
        f"The dataset has {duplicates:,} duplicate rows "
        f"and {invalid_records:,} invalid voting records. "
        "These records are excluded during cleaning "
        "and are not used in the turnout calculations."
    )

    # 2. Data limitations
    st.subheader("Data Limitations")

    # Purple box with the main limitations
    st.markdown(
        """
        <div style="
            background-color: #332345;
            border-left: 4px solid #9C6CC7;
            border-radius: 0px;
            padding: 20px 24px;
            margin: 16px 0 24px 0;
            color: #F1E8FA;
            line-height: 1.8;
        ">
            <ul style="margin: 0; padding-left: 20px;">
                <li>
                    The dataset only includes the second round.
                    Not all French municipalities are represented.
                </li>
                <li>
                    Some polling stations have very few registered voters.
                    Their turnout rates can be unusually high or low.
                </li>
                <li>
                    Department turnout rates can hide differences
                    between municipalities and polling stations.
                </li>
                <li>
                    The data shows where participation is higher
                    or lower, but not why.
                </li>
                <li>
                    Results may change when filters are applied.
                    Comparisons only concern the areas displayed.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    # No results with these filters
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    # 3. Main statistics

    # Department turnout rates
    departments = department_table(df)

    #Highest and lowest department turnout
    highest = departments.loc[
        departments["turnout_rate"].idxmax()
    ]

    lowest = departments.loc[
        departments["turnout_rate"].idxmin()
    ]

    # Total registered voters and voters
    total_registered = df["inscrits"].sum()
    total_voters = df["votants"].sum()

    # Overall turnout rate
    overall_turnout = (
        total_voters / total_registered * 100
    )

    # Turnout rate for each polling station
    rates = df["votants"] / df["inscrits"] * 100

    #Median turnout
    median_rate = rates.median()

    # Gap in percentage points
    turnout_gap = (
        highest["turnout_rate"]
        - lowest["turnout_rate"]
    )

    #Percentage of polling stations between 50% and 70%
    middle_share = rates.between(50, 70).mean() * 100

    # 4. Key findings
    st.header("Key Findings")
    st.write(
        "The results show three important patterns "
        "in voter participation."
    )
    # Differences between departments
    st.subheader("1. Department Turnout Differences")

    if len(departments) > 1:
        st.write(
            f"**{highest['libelle_departement']}** has the highest "
            f"turnout rate ({highest['turnout_rate']:.2f}%), "
            f"while **{lowest['libelle_departement']}** has the lowest "
            f"({lowest['turnout_rate']:.2f}%). "
            f"The gap is **{turnout_gap:.2f} percentage points**."
        )

        st.write(
            "This shows that participation is not the same "
            "across the departments displayed."
        )

    else:
        st.write(
            f"Only **{highest['libelle_departement']}** is displayed, "
            f"with a turnout rate of "
            f"**{highest['turnout_rate']:.2f}%**. "
            "We can still compare participation "
            "between its polling stations."
        )

    # Overall participation
    st.subheader("2. Overall Voter Participation")
    if overall_turnout > 50:
        st.write(
            f"The overall turnout rate is **{overall_turnout:.2f}%**. "
            "More than half of registered voters "
            "took part in the election."
        )
    else:
        st.write(
            f"The overall turnout rate is **{overall_turnout:.2f}%**. "
            f"{100 - overall_turnout:.2f}% of registered voters "
            "did not participate."
        )

    st.write(
        f"The median polling-station turnout is "
        f"**{median_rate:.2f}%**. "
        "The overall rate takes the number of registered voters "
        "into account, while the median represents "
        "the middle polling-station turnout rate."
    )

    # Polling-station distribution
    st.subheader("3. Polling-Station Turnout Distribution")

    st.write(
        f"**{middle_share:.1f}%** of polling stations have "
        "a turnout rate between 50% and 70%. "
        f"The lowest observed rate is {rates.min():.2f}%, "
        f"and the highest is {rates.max():.2f}%."
    )

    if middle_share >= 50:
        st.write(
            "Most polling stations have turnout rates "
            "between 50% and 70%, but some have higher "
            "or lower participation."
        )
    else:
        st.write(
            "Less than half of polling stations have "
            "turnout rates between 50% and 70%. "
            "Participation is more spread across "
            "different turnout rates."
        )

    st.divider()

    # 5. Possible explanations
    st.header("What Could Explain These Differences ?")

    st.write(
        "Several factors could influence voter participation, "
        "such as the age of voters, income, education or "
        "local political competition."
    )
    st.write(
        "However, our dataset does not include enough information "
        "to test these explanations. We can observe differences "
        "between areas, but we cannot say what caused them."
    )

    st.divider()
    # 6. Conclusion
    st.header("Conclusion")

    st.write(
        "**Voter participation is not the same across all "
        "the areas covered by the dataset.**"
    )

    st.write(
        f"The overall turnout rate is {overall_turnout:.2f}% "
        "for the selected data. "
        "This gives a general picture of participation, "
        "but polling-station results show more local details."
    )

    st.write(
        "Looking at different geographical levels helps "
        "us better understand voter participation."
    )