import pandas as pd
from pathlib import Path

def load_data():
    file_path = Path(__file__).resolve().parent.parent / "data" / "elections_2026.csv"
    df = pd.read_csv(file_path, sep=None, engine="python")
    return df