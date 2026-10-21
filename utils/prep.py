import pandas as pd

def make_tables(df):
    # Copy the original dataset
    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows with missing essential values
    df = df.dropna(subset=["inscrits", "votants"])

    # Keep valid voting data
    df = df[df["inscrits"] > 0]
    df = df[
        (df["votants"] >= 0) &
        (df["votants"] <= df["inscrits"])
    ]

    # Calculate voter turnout and abstention rates
    df["turnout_rate"] = (
        df["votants"] / df["inscrits"] * 100
    )

    df["abstention_rate"] = 100 - df["turnout_rate"]

    return df