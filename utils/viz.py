import json
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Dashboard colors
PURPLE = "#A675D1"
DARK_PURPLE = "#67329B"
LIGHT_PURPLE = "#E4CCFF"
PURPLE_SCALE = [
    [0.00, "#F0E5FA"],
    [0.25, "#CBA8EC"],
    [0.50, "#9861CC"],
    [0.75, "#67329B"],
    [1.00, "#371452"]
]


# Common chart style
def chart_style(fig, height=400):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#EAE4F0"),
        margin=dict(l=20, r=20, t=30, b=30),
        hoverlabel=dict(
            bgcolor="#332345",
            font_color="#F1E8FA"
        )
    )

    return fig

# Department turnout rates
def department_table(df):

    # Total voters and registered voters by department
    departments = (
        df.groupby(
            ["code_departement", "libelle_departement"],
            as_index=False
        )[["inscrits", "votants"]]
        .sum()
    )

    # Weighted turnout rate
    departments["turnout_rate"] = (
        departments["votants"]
        / departments["inscrits"]
        * 100
    )

    # Department codes for GeoJSON
    departments["code_departement"] = (
        departments["code_departement"]
        .astype(str)
        .str.strip()
        .str.zfill(2)
    )

    return departments

# Geographical boundaries
@st.cache_data(show_spinner=False)
def load_geojson():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "departements.geojson"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        geojson = json.load(file)

    return geojson

# Department turnout map
def map_chart(df):
    departments = department_table(df)
    geojson = load_geojson()

    fig = px.choropleth_map(
        departments,
        geojson=geojson,
        locations="code_departement",
        featureidkey="properties.code",
        color="turnout_rate",
        color_continuous_scale=PURPLE_SCALE,
        hover_name="libelle_departement",
        hover_data={
            "code_departement": False,
            "turnout_rate": ":.2f",
            "inscrits": ":,",
            "votants": ":,"
        },
        labels={
            "turnout_rate": "Turnout (%)",
            "inscrits": "Registered voters",
            "votants": "Voters"
        },
        map_style="carto-darkmatter",
        center={"lat": 46.6, "lon": 2.5},
        zoom=4.5,
        opacity=0.9
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Turnout (%)",
            ticksuffix="%"
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return chart_style(fig, height=550)


#Department ranking
def bar_chart(df, ranking="Top 10"):
    departments = department_table(df)

    # Departments by turnout rate
    departments = departments.sort_values(
        "turnout_rate",
        ascending=False
    )

    if ranking == "Top 10":
        departments = departments.head(10)

    elif ranking == "Bottom 10":
        departments = departments.tail(10)

    # Order for horizontal bars
    departments = departments.sort_values("turnout_rate")

    fig = px.bar(
        departments,
        x="turnout_rate",
        y="libelle_departement",
        orientation="h",
        color_discrete_sequence=[PURPLE],
        hover_data={
            "turnout_rate": ":.2f",
            "inscrits": ":,",
            "votants": ":,"
        },
        labels={
            "turnout_rate": "Turnout rate (%)",
            "libelle_departement": "Department",
            "inscrits": "Registered voters",
            "votants": "Voters"
        }
    )

    fig.update_traces(
        marker_color=PURPLE,
        marker_line_color=DARK_PURPLE,
        marker_line_width=0.5
    )

    fig.update_layout(
        yaxis_title=None,
        xaxis_title="Turnout rate (%)",
        xaxis=dict(range=[0, 100], ticksuffix="%"),
        showlegend=False
    )

    height = max(400, len(departments) * 30 + 100)

    return chart_style(fig, height=height)


# Municipality ranking
def municipality_chart(df, ranking="Top 10"):

    #Municipality identification
    group_columns = [
        "code_departement",
        "libelle_departement",
        "libelle_commune"
    ]

    if "code_commune" in df.columns:
        group_columns.append("code_commune")

    # Total votes by municipality
    municipalities = (
        df.groupby(group_columns, as_index=False)[
            ["inscrits", "votants"]
        ]
        .sum()
    )

    # Municipality turnout rates
    municipalities["turnout_rate"] = (
        municipalities["votants"]
        / municipalities["inscrits"]
        * 100
    )

    municipalities = municipalities.sort_values(
        "turnout_rate",
        ascending=False
    )

    if ranking == "Top 10":
        municipalities = municipalities.head(10)

    else:
        municipalities = municipalities.tail(10)

    municipalities = municipalities.sort_values("turnout_rate")

    # Municipality and department names
    municipalities["municipality_label"] = (
        municipalities["libelle_commune"]
        + " ("
        + municipalities["libelle_departement"]
        + ")"
    )

    fig = go.Figure()

    # Lollipop lines
    for _, row in municipalities.iterrows():
        fig.add_trace(
            go.Scatter(
                x=[0, row["turnout_rate"]],
                y=[
                    row["municipality_label"],
                    row["municipality_label"]
                ],
                mode="lines",
                line=dict(
                    color="#765391",
                    width=3
                ),
                hoverinfo="skip",
                showlegend=False
            )
        )

    # Lollipop points
    fig.add_trace(
        go.Scatter(
            x=municipalities["turnout_rate"],
            y=municipalities["municipality_label"],
            mode="markers",
            marker=dict(
                color=PURPLE,
                size=12,
                line=dict(
                    color=LIGHT_PURPLE,
                    width=1
                )
            ),
            customdata=municipalities[
                ["inscrits", "votants"]
            ].to_numpy(),
            hovertemplate=(
                "%{y}<br>"
                "Turnout : %{x:.2f}%<br>"
                "Registered voters : %{customdata[0]:,}<br>"
                "Voters : %{customdata[1]:,}"
                "<extra></extra>"
            ),
            showlegend=False
        )
    )

    fig.update_layout(
        xaxis_title="Turnout rate (%)",
        yaxis_title=None,
        xaxis=dict(range=[0, 100], ticksuffix="%"),
        margin=dict(l=300, r=20, t=30, b=40)
    )

    return chart_style(fig, height=500)


# Polling-station turnout distribution
def distribution_chart(df):

    # Turnout rate for each polling station
    rates = (
        df["votants"] / df["inscrits"] * 100
    ).dropna()

    values = rates.to_numpy(dtype=float)
    x = np.linspace(0, 100, 250)

    # Density curve
    if len(values) > 1:
        std = np.std(values, ddof=1)

        # Bandwidth for the smooth curve
        bandwidth = (
            1.06 * std * len(values) ** (-1 / 5)
        )

        if bandwidth <= 0 or not np.isfinite(bandwidth):
            bandwidth = 1.0

        density = np.zeros_like(x)

        # Gaussian density estimation
        for value in values:
            density += np.exp(
                -0.5 * ((x - value) / bandwidth) ** 2
            )

        density /= (
            len(values)
            * bandwidth
            * np.sqrt(2 * np.pi)
        )

    else:
        density = np.zeros_like(x)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=density,
            mode="lines",
            fill="tozeroy",
            line=dict(
                color=PURPLE,
                width=3
            ),
            fillcolor="rgba(166,117,209,0.25)",
            name="Turnout distribution",
            hovertemplate=(
                "Turnout : %{x:.1f}%<br>"
                "Density : %{y:.4f}"
                "<extra></extra>"
            )
        )
    )

    # Median line
    if len(values) > 0:
        median = np.median(values)

        fig.add_vline(
            x=median,
            line_color=LIGHT_PURPLE,
            line_dash="dash",
            line_width=2,
            annotation_text=f"Median : {median:.2f}%",
            annotation_position="top right"
        )

    fig.update_layout(
        xaxis_title="Turnout rate (%)",
        yaxis_title="Density",
        xaxis=dict(range=[0, 100], ticksuffix="%"),
        showlegend=False
    )

    return chart_style(fig, height=430)

# Turnout variability by department
def box_chart(df, selected_departments):

    # Selected departments
    filtered = df[
        df["libelle_departement"].isin(
            selected_departments
        )
    ].copy()

    # Polling-station turnout rates
    filtered["turnout_rate"] = (
        filtered["votants"]
        / filtered["inscrits"]
        * 100
    )

    fig = px.box(
        filtered,
        x="turnout_rate",
        y="libelle_departement",
        orientation="h",
        color_discrete_sequence=[PURPLE],
        points="outliers",
        labels={
            "turnout_rate": "Turnout rate (%)",
            "libelle_departement": "Department"
        }
    )

    fig.update_traces(
        line_color=LIGHT_PURPLE,
        fillcolor="rgba(166,117,209,0.45)",
        marker_color=DARK_PURPLE,
        marker_size=5
    )

    fig.update_layout(
        xaxis_title="Turnout rate (%)",
        yaxis_title=None,
        xaxis=dict(range=[0, 100], ticksuffix="%"),
        showlegend=False
    )

    height = max(400, len(selected_departments) * 55 + 120)

    return chart_style(fig, height=height)