import streamlit as st
from sections.conclusions import show_conclusions
from utils.io import load_data
from utils.prep import make_tables
from sections.intro import show_intro
from sections.overview import show_overview
from sections.deep_dives import show_deep_dives

# Page settings
st.set_page_config(
    page_title="French Municipal Elections 2026",
    page_icon="🗳️",
    layout="wide"
)

# Data loading and cleaning
@st.cache_data(show_spinner=False)
def get_data():
    raw = load_data()
    clean = make_tables(raw)
    return raw, clean

raw_df, df = get_data()

# Sidebar
with st.sidebar:

    st.markdown("### **Ozgullu Lucie**")
    st.write("Promo 2028")
    st.write("lucie.ozgullu@efrei.net")

    st.markdown(
        "[GitHub - Lucie123456789]"
        "(https://github.com/Lucie123456789)"
    )

    st.write("DE, Data Analysis & Visualization")

    st.divider()

    st.header("Filters")

    # Department selection
    departments = sorted(
        df["libelle_departement"].dropna().unique()
    )

    selected_departments = st.multiselect(
        "Select Department(s)",
        departments,
        placeholder="All departments"
    )

    filtered_df = df.copy()

    if selected_departments:
        filtered_df = filtered_df[
            filtered_df["libelle_departement"].isin(
                selected_departments
            )
        ]

    # Municipality selection
    municipalities = sorted(
        filtered_df["libelle_commune"].dropna().unique()
    )

    selected_municipalities = st.multiselect(
        "Select Municipality(ies)",
        municipalities,
        placeholder="All municipalities"
    )

    if selected_municipalities:
        filtered_df = filtered_df[
            filtered_df["libelle_commune"].isin(
                selected_municipalities
            )
        ]

    st.divider()

    st.caption(
        "Data: French Municipal Elections 2026 - Second Round"
    )

#Introduction
show_intro()

st.divider()

# Election overview
show_overview(filtered_df, raw_df)

st.divider()

# Interactive charts
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    show_deep_dives(filtered_df)

# Data quality and conclusions
st.divider()

show_conclusions(filtered_df, raw_df)

# Footer
st.divider()

col1, col2 = st.columns([4, 1])

with col1:
    st.markdown("**MATHEW Mano Joseph**")
    st.caption("EFREI Paris | Data Analysis & Visualization")

with col2:
    st.image("assets/efrei.png", width=120)