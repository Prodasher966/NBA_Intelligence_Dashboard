import pandas as pd


# -----------------------------------
# Columns to keep for analysis
# -----------------------------------
COLUMNS_TO_KEEP = [
    # Identifiers
    "GAME_ID",
    "TEAM_ID",
    "TEAM_NAME",
    "TEAM_ABBREVIATION",
    "SEASON",
    "HOME_TEAM",

    # Outcome
    "RESULT",

    # Offensive metrics
    "PTS",
    "FGM",
    "FGA",
    "FG_PCT",
    "FG3M",
    "FG3A",
    "FG3_PCT",
    "FTM",
    "FTA",
    "FT_PCT",
    "AST",
    "EFG_PCT",

    # Defensive & control metrics
    "OREB",
    "DREB",
    "REB",
    "STL",
    "BLK",
    "TO",
    "PF",

    # Advanced / contextual
    "PLUS_MINUS",
    "PIE",
]


# -----------------------------------
# Main preprocessing function
# -----------------------------------
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and validates raw NBA data for analysis.

    Steps:
    - Select relevant columns
    - Validate RESULT column
    - Handle missing values
    - Sort data for consistency

    Args:
        df (pd.DataFrame): Raw dataset

    Returns:
        pd.DataFrame: Cleaned dataset
    """

    df = df.copy()

    # -----------------------------------
    # Keep only relevant columns
    # -----------------------------------
    df = df[COLUMNS_TO_KEEP]

    # -----------------------------------
    # Validate RESULT column
    # -----------------------------------
    valid_results = {0, 1}
    if not set(df["RESULT"].unique()).issubset(valid_results):
        raise ValueError(
            "RESULT column must contain only 0 (loss) or 1 (win)"
        )

    # -----------------------------------
    # Handle missing values
    # -----------------------------------
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    categorical_cols = df.select_dtypes(include="object").columns
    df[categorical_cols] = df[categorical_cols].fillna("Unknown")

    # -----------------------------------
    # Ensure logical consistency
    # -----------------------------------
    df = df[df["FGA"] >= df["FGM"]]
    df = df[df["FG3A"] >= df["FG3M"]]
    df = df[df["FTA"] >= df["FTM"]]

    # -----------------------------------
    # Sort for deterministic behavior
    # -----------------------------------
    df = df.sort_values(
        by=["SEASON", "TEAM_NAME", "GAME_ID"]
    ).reset_index(drop=True)

    return df
