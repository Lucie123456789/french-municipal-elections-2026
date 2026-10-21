import streamlit as st
from utils.styles import insight
from utils.styles import limitation

def show_intro():

    # Dashboard title
    st.title("French Municipal Elections 2026")
    st.caption("SECOND ROUND | VOTER PARTICIPATION ANALYSIS")
    st.divider()

    # Introduction
    st.subheader("Why Does Voter Participation Matter ?")
    st.write(
        """
        **One election, thousands of polling stations, but not the same
        level of participation everywhere.**

        During the second round of the 2026 French municipal elections,
        some communities mobilized more voters than others.
        What do these differences reveal about voter participation
        across France ?

        This dashboard explores turnout across municipalities and
        departments, highlighting geographical contrasts, local
        patterns and unusual results.
        """
    )

    # Main research question
    st.markdown(
        """
        <div style="
            background-color: #EDE0FA;
            border-left: 4px solid #A675D1;
            border-radius: 0px;
            padding: 18px 20px;
            margin: 16px 0;
            color: #39264C;
        ">
            <strong style="color: #653A91;">
                Main Question :
            </strong>
            Do people vote more in some French cities
            and departments than in others ?
        </div>
        """,
        unsafe_allow_html=True
    )

    # Project objectives
    with st.expander("Project Objectives"):
        st.markdown("""
        This project aims to :

        - Analyze voter turnout and abstention rates
        - Compare participation between departments and municipalities
        - Identify the top 10 and bottom 10 municipalities by turnout
        - Explore the distribution of voter turnout rates
        - Examine turnout variability between polling stations
        - Assess data quality by checking missing values, duplicates and invalid records
        """)

    # Dataset information
    with st.expander("About the Dataset"):
        st.write(
            "The dataset comes from data.gouv.fr, the French "
            "government's open data platform. It contains "
            "results from the second round of the 2026 "
            "municipal elections."
        )

        st.markdown("""
        **Available information:**
        - Registered voters
        - Total voters
        - Abstentions
        - Blank and invalid votes
        - Municipalities and departments
        """)
        
        st.caption(
            "Source: data.gouv.fr | Municipal Elections 2026 "
            "| Second Round"
        )

        # Dataset limitation
        limitation(
            "This dataset only includes polling stations "
            "covered by the second round. It does not represent "
            "all French municipalities."
        )

        # Target audience
        st.write(
            "This dashboard is for anyone interested in understanding "
            "voter participation and how it differs across French areas."
        )