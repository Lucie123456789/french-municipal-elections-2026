import streamlit as st
from html import escape

# Light purple box for key insights
def insight(message):
    st.markdown(
        f"""
        <div style="
            background-color: #EDE0FA;
            border-left: 4px solid #A675D1;
            border-radius: 0px;
            padding: 18px 20px;
            margin: 16px 0;
            color: #39264C;
            line-height: 1.6;
        ">
            <strong style="color: #653A91;">
                Key Insight :
            </strong>
            {escape(message)}
        </div>
        """,
        unsafe_allow_html=True
    )

# Dark purple box for data limitations
def limitation(message):
    st.markdown(
        f"""
        <div style="
            background-color: #332345;
            border-left: 4px solid #9C6CC7;
            border-radius: 0px;
            padding: 18px 20px;
            margin: 16px 0;
            color: #F1E8FA;
            line-height: 1.6;
        ">
            <strong style="color: #E4CCFF;">
                Data Limitation :
            </strong>
            {escape(message)}
        </div>
        """,
        unsafe_allow_html=True
    )