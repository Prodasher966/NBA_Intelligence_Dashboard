import pandas as pd


# -----------------------------------
# Classification thresholds
# -----------------------------------
WIN_PCT_CONTENDER = 0.60
WIN_PCT_HIGH_RISK = 0.40

NET_RATING_CONTENDER = 5
NET_RATING_HIGH_RISK = -5

TURNOVER_RATIO_LIMIT = 0.15


# -----------------------------------
# Team strength classification
# -----------------------------------
def classify_team_strength(team_season_df: pd.DataFrame) -> pd.DataFrame:
    """
    Classifies teams into strength categories based on
    performance metrics.

    Categories:
    - Strong Contender
    - Inconsistent Performer
    - High Risk

    Args:
        team_season_df (pd.DataFrame): Team-season metrics

    Returns:
        pd.DataFrame: Team-season metrics with strength label
    """

    df = team_season_df.copy()

    conditions = [
        (
            (df["win_pct"] >= WIN_PCT_CONTENDER)
            & (df["net_rating"] >= NET_RATING_CONTENDER)
            & (df["turnover_ratio"] <= TURNOVER_RATIO_LIMIT)
        ),
        (
            (df["win_pct"] <= WIN_PCT_HIGH_RISK)
            & (df["net_rating"] <= NET_RATING_HIGH_RISK)
        ),
    ]

    choices = [
        "Strong Contender",
        "High Risk",
    ]

    df["team_strength"] = pd.Series(
        pd.NA, index=df.index
    )

    df.loc[conditions[0], "team_strength"] = choices[0]
    df.loc[conditions[1], "team_strength"] = choices[1]

    df["team_strength"] = df["team_strength"].fillna(
        "Inconsistent Performer"
    )

    return df
