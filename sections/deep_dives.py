import streamlit as st
from utils.styles import insight
from utils.viz import (
    map_chart,
    bar_chart,
    municipality_chart,
    distribution_chart,
    box_chart,
    department_table
)

def show_deep_dives(df):
    # Main statistics
    departments = department_table(df)
    rates = df["votants"] / df["inscrits"] * 100

    median_rate = rates.median()
    min_rate = rates.min()
    max_rate = rates.max()
    overall_turnout = (
        df["votants"].sum()
        / df["inscrits"].sum()
        * 100
    )

    # 1. Geographical analysis
    st.header("Geographical Analysis")
    st.subheader("Where Do Voters Participate the Most ?")

    st.write(
        "The map shows voter turnout across the departments "
        "covered by the dataset. Which areas have the highest "
        "and lowest participation ?"
    )

    st.plotly_chart(
        map_chart(df),
        use_container_width=True,
        config={"displayModeBar": False}
    )
    # Department ranking
    ranked_departments = departments.sort_values(
        "turnout_rate",
        ascending=False
    )

    top_3 = ranked_departments.head(3)
    bottom_3 = ranked_departments.tail(3).sort_values(
        "turnout_rate"
    )

    st.subheader("Highest and Lowest Turnout")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("**Top 3 Departments**")

        for i, (_, row) in enumerate(top_3.iterrows(), 1):
            st.write(
                f"{i}. **{row['libelle_departement']}** "
                f"— {row['turnout_rate']:.2f}%"
            )

    with col2:
        st.markdown("**Bottom 3 Departments**")
        for i, (_, row) in enumerate(bottom_3.iterrows(), 1):
            st.write(
                f"{i}. **{row['libelle_departement']}** "
                f"— {row['turnout_rate']:.2f}%"
            )

    # Difference between departments
    turnout_gap = (
        ranked_departments["turnout_rate"].max()
        - ranked_departments["turnout_rate"].min()
    )

    if len(departments) > 1:
        insight(
            f"The gap between the highest and lowest "
            f"department turnout rates is {turnout_gap:.2f} "
            f"percentage points. The overall turnout rate "
            f"is {overall_turnout:.2f}%."
        )
    else:
        insight(
            f"Only {departments.iloc[0]['libelle_departement']} "
            f"is displayed, with a turnout rate of "
            f"{overall_turnout:.2f}%. "
            "Polling stations within this department "
            "may still have different turnout rates."
        )

    st.caption(
        "The map only shows areas included in the second-round "
        "dataset. It does not represent turnout across all "
        "French municipalities."
    )

    st.divider()

    # 2.Department ranking
    st.header("Department Ranking")
    st.subheader("Where Was Turnout Highest ?")
    ranking = st.selectbox(
        "Choose a department ranking :",
        ["Top 10", "Bottom 10", "All Departments"],
        key="department_ranking"
    )

    st.plotly_chart(
        bar_chart(df, ranking),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    #Selected ranking
    ranked = departments.sort_values(
        "turnout_rate",
        ascending=False
    )

    if ranking == "Top 10":
        top = ranked.head(10)
        first = top.iloc[0]
        last = top.iloc[-1]
        insight(
            f"{first['libelle_departement']} has the highest "
            f"turnout rate ({first['turnout_rate']:.2f}%). "
            f"Among the {len(top)} departments displayed, "
            f"turnout ranges from {last['turnout_rate']:.2f}% "
            f"to {first['turnout_rate']:.2f}%."
        )

    elif ranking == "Bottom 10":
        bottom = ranked.tail(10)
        lowest = bottom.iloc[-1]
        highest = bottom.iloc[0]

        insight(
            f"{lowest['libelle_departement']} has the lowest "
            f"turnout rate ({lowest['turnout_rate']:.2f}%). "
            f"Among the {len(bottom)} departments displayed, "
            f"turnout ranges from {lowest['turnout_rate']:.2f}% "
            f"to {highest['turnout_rate']:.2f}%."
        )

    else:
        above = (
            departments["turnout_rate"] > overall_turnout
        ).sum()

        below = (
            departments["turnout_rate"] < overall_turnout
        ).sum()

        equal = len(departments) - above - below

        insight(
            f"Among {len(departments)} departments, "
            f"{above} have turnout above the overall rate "
            f"of {overall_turnout:.2f}%, "
            f"{below} are below it and {equal} are equal to it."
        )

    st.divider()
    # 3. Municipality ranking
    st.subheader("Municipality Ranking")

    municipality_ranking = st.selectbox(
        "Choose a municipality ranking :",
        ["Top 10", "Bottom 10"],
        key="municipality_ranking"
    )

    st.plotly_chart(
        municipality_chart(df, municipality_ranking),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # Municipality identification
    group_columns = [
        "code_departement",
        "libelle_departement",
        "libelle_commune"
    ]

    if "code_commune" in df.columns:
        group_columns.append("code_commune")

    # Municipality turnout rates
    municipalities = (
        df.groupby(group_columns, as_index=False)[
            ["inscrits", "votants"]
        ]
        .sum()
    )
    municipalities["turnout_rate"] = (
        municipalities["votants"]
        / municipalities["inscrits"]
        * 100
    )

    ranked_municipalities = municipalities.sort_values(
        "turnout_rate",
        ascending=False
    )

    if municipality_ranking == "Top 10":
        top = ranked_municipalities.head(10)
        highest = top.iloc[0]
        lowest = top.iloc[-1]

        insight(
            f"{highest['libelle_commune']} "
            f"({highest['libelle_departement']}) has the highest "
            f"turnout rate ({highest['turnout_rate']:.2f}%). "
            f"Among the {len(top)} municipalities displayed, "
            f"turnout ranges from {lowest['turnout_rate']:.2f}% "
            f"to {highest['turnout_rate']:.2f}%."
        )

    else:
        bottom = ranked_municipalities.tail(10)
        lowest = bottom.iloc[-1]
        highest = bottom.iloc[0]

        insight(
            f"{lowest['libelle_commune']} "
            f"({lowest['libelle_departement']}) has the lowest "
            f"turnout rate ({lowest['turnout_rate']:.2f}%). "
            f"Among the {len(bottom)} municipalities displayed, "
            f"turnout ranges from {lowest['turnout_rate']:.2f}% "
            f"to {highest['turnout_rate']:.2f}%."
        )

    st.divider()

    # 4. Turnout distribution
    st.header("Turnout Distribution")

    st.write("Where are turnout rates concentrated ?")

    st.plotly_chart(
        distribution_chart(df),
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # Density curve explanation
    st.caption(
        "The curve shows where polling-station turnout rates "
        "are most concentrated. It is a smoothed distribution, "
        "not the exact number of polling stations. "
        "The dashed line shows the median turnout rate."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Median", f"{median_rate:.2f}%")
    c2.metric("Minimum", f"{min_rate:.2f}%")
    c3.metric("Maximum", f"{max_rate:.2f}%")

    # Polling stations between 50% and 70%
    middle_share = rates.between(50, 70).mean() * 100

    if middle_share >= 50:
        insight(
            f"{middle_share:.1f}% of polling stations have "
            "a turnout rate between 50% and 70%. "
            f"The median is {median_rate:.2f}%. "
            "Most polling stations are in this range."
        )
    else:
        insight(
            f"{middle_share:.1f}% of polling stations have "
            "a turnout rate between 50% and 70%. "
            f"The median is {median_rate:.2f}%. "
            "More than half of polling stations are "
            "outside this range."
        )

    st.divider()

    # 5. Participation variability
    st.subheader("Participation Variability")

    st.write(
        "How different are polling stations "
        "within each department ?"
    )

    available_departments = sorted(
        df["libelle_departement"].dropna().unique()
    )

    selected_departments = st.multiselect(
        "Departments to compare :",
        available_departments,
        default=available_departments[:3],
        key="box_departments"
    )

    if selected_departments:

        st.plotly_chart(
            box_chart(df, selected_departments),
            use_container_width=True,
            config={"displayModeBar": False}
        )

        # Selected departments
        selected_data = df[
            df["libelle_departement"].isin(selected_departments)
        ].copy()

        selected_data["turnout_rate"] = (
            selected_data["votants"]
            / selected_data["inscrits"]
            * 100
        )

        # Median and quartiles
        stats = selected_data.groupby("libelle_departement")[
            "turnout_rate"
        ].agg(
            median="median",
            q1=lambda x: x.quantile(0.25),
            q3=lambda x: x.quantile(0.75)
        )

        # Spread of the middle 50%
        stats["spread"] = stats["q3"] - stats["q1"]

        highest_median = stats["median"].idxmax()
        widest_spread = stats["spread"].idxmax()

        if len(stats) > 1:
            insight(
                f"{highest_median} has the highest median turnout "
                f"({stats.loc[highest_median, 'median']:.2f}%) "
                "among the departments compared. "
                f"{widest_spread} has the widest middle 50% "
                f"of turnout rates "
                f"({stats.loc[widest_spread, 'spread']:.2f} "
                "percentage points)."
            )
        else:
            insight(
                f"In {highest_median}, the median turnout is "
                f"{stats.loc[highest_median, 'median']:.2f}%. "
                "The middle 50% of polling stations have "
                f"turnout rates between "
                f"{stats.loc[highest_median, 'q1']:.2f}% and "
                f"{stats.loc[highest_median, 'q3']:.2f}%."
            )

    else:
        st.info(
            "Select at least one department to display the box plot."
        )