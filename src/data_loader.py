import pandas as pd
import streamlit as st
from pathlib import Path

# -----------------------------------
# File path configuration
# -----------------------------------
DATA_PATH = Path("data/nba_data_2012_2024.csv")


# -----------------------------------
# Expected schema (for validation)
# -----------------------------------
EXPECTED_COLUMNS = {
    "GAME_ID": "int64",
    "TEAM_ID": "int64",
    "TEAM_NAME": "object",
    "TEAM_ABBREVIATION": "object",
    "TEAM_CITY": "object",
    "HOME_TEAM": "object",
    "MIN": "object",
    "FGM": "int64",
    "FGA": "int64",
    "FG_PCT": "float64",
    "FG3M": "int64",
    "FG3A": "int64",
    "FG3_PCT": "float64",
    "FTM": "int64",
    "FTA": "int64",
    "FT_PCT": "float64",
    "OREB": "int64",
    "DREB": "int64",
    "REB": "int64",
    "AST": "int64",
    "STL": "int64",
    "BLK": "int64",
    "TO": "int64",
    "PF": "int64",
    "PTS": "int64",
    "PLUS_MINUS": "int64",
    "EFG_PCT": "float64",
    "PIE": "float64",
    "COVID_FLAG": "int64",
    "RESULT": "int64",
    "SEASON": "int64",
    "WIN_PCT": "float64",
}


# -----------------------------------
# Load & cache dataset
# -----------------------------------
@st.cache_data(show_spinner="Loading NBA data...")
def load_data() -> pd.DataFrame:
    """
    Loads the NBA dataset from CSV, validates schema,
    and returns a pandas DataFrame.

    Returns:
        pd.DataFrame: Raw NBA game-level team data
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at path: {DATA_PATH.resolve()}"
        )

    df = pd.read_csv(DATA_PATH)

    # -----------------------------------
    # Basic schema validation
    # -----------------------------------
    missing_cols = set(EXPECTED_COLUMNS.keys()) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Dataset is missing required columns: {missing_cols}"
        )

    # -----------------------------------
    # Enforce data types where safe
    # -----------------------------------
    for col, dtype in EXPECTED_COLUMNS.items():
        try:
            df[col] = df[col].astype(dtype)
        except Exception:
            # We don't fail hard here; preprocessing will handle edge cases
            pass

    return df
