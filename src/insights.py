import pandas as pd


# -----------------------------------
# Metrics to analyze against winning
# -----------------------------------
INSIGHT_METRICS = [
    "points_per_game",
    "fg_pct",
    "fg3_pct",
    "ft_pct",
    "assists_per_game",
    "rebounds_per_game",
    "steals_per_game",
    "blocks_per_game",
    "turnovers_per_game",
    "fouls_per_game",
    "net_rating",
    "turnover_ratio",
    "efg_pct",
]


# -----------------------------------
# Correlation with win percentage
# -----------------------------------
def calculate_win_correlations(team_season_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Pearson correlation between win percentage
    and selected performance metrics.

    Args:
        team_season_df (pd.DataFrame): Team-season metrics

    Returns:
        pd.DataFrame: Correlation values sorted by strength
    """

    correlations = []

    for metric in INSIGHT_METRICS:
        if metric not in team_season_df.columns:
            continue

        corr_value = team_season_df["win_pct"].corr(
            team_season_df[metric]
        )

        correlations.append(
            {
                "metric": metric,
                "correlation_with_win_pct": corr_value
            }
        )

    corr_df = pd.DataFrame(correlations)

    corr_df = corr_df.sort_values(
        by="correlation_with_win_pct",
        ascending=False
    ).reset_index(drop=True)

    return corr_df


# -----------------------------------
# Strongest positive & negative drivers
# -----------------------------------
def identify_key_win_drivers(
    correlation_df: pd.DataFrame,
    positive_threshold: float = 0.4,
    negative_threshold: float = -0.4,
) -> dict:
    """
    Identifies metrics with strong positive or negative
    correlation with winning.

    Args:
        correlation_df (pd.DataFrame): Output from calculate_win_correlations
        positive_threshold (float): Positive correlation cutoff
        negative_threshold (float): Negative correlation cutoff

    Returns:
        dict: Key win drivers
    """

    strong_positive = correlation_df[
        correlation_df["correlation_with_win_pct"] >= positive_threshold
    ]

    strong_negative = correlation_df[
        correlation_df["correlation_with_win_pct"] <= negative_threshold
    ]

    return {
        "strong_positive_drivers": strong_positive,
        "strong_negative_drivers": strong_negative,
    }


# -----------------------------------
# Scatter-ready dataset
# -----------------------------------
def prepare_scatter_data(
    team_season_df: pd.DataFrame,
    x_metric: str,
    y_metric: str = "win_pct",
) -> pd.DataFrame:
    """
    Prepares clean data for scatter plots.

    Args:
        team_season_df (pd.DataFrame): Team-season metrics
        x_metric (str): X-axis metric
        y_metric (str): Y-axis metric (default: win_pct)

    Returns:
        pd.DataFrame: Scatter-ready DataFrame
    """

    required_cols = ["TEAM_NAME", "SEASON", x_metric, y_metric]

    missing = set(required_cols) - set(team_season_df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns for scatter plot: {missing}"
        )

    scatter_df = team_season_df[required_cols].dropna()

    return scatter_df

def explain_win_prediction(
    team_row: pd.Series,
    feature_names: list,
    coefficients: list,
    top_n: int = 3,
) -> dict:
    """
    Explains win prediction drivers for a team.

    Returns:
        dict with positive and negative drivers
    """

    impact = team_row[feature_names].values * coefficients

    impact_df = pd.DataFrame({
        "feature": feature_names,
        "impact": impact,
    })

    positive = (
        impact_df[impact_df["impact"] > 0]
        .sort_values("impact", ascending=False)
        .head(top_n)
    )

    negative = (
        impact_df[impact_df["impact"] < 0]
        .sort_values("impact")
        .head(top_n)
    )

    return {
        "positive": positive,
        "negative": negative,
    }

def get_strong_drivers(df: pd.DataFrame, top_n: int = 3) -> dict:
    """
    Computes top positive and negative correlations with win_pct.
    Returns:
        dict: {"strong_positive_drivers": df, "strong_negative_drivers": df}
    """
    corr_matrix = df.corr()
    win_corr = corr_matrix["win_pct"].drop("win_pct").sort_values(ascending=False)
    positive = win_corr.head(top_n).reset_index().rename(columns={"index": "metric", "win_pct": "correlation_with_win_pct"})
    negative = win_corr.tail(top_n).reset_index().rename(columns={"index": "metric", "win_pct": "correlation_with_win_pct"})
    return {"strong_positive_drivers": positive, "strong_negative_drivers": negative}
