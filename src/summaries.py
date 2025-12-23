import pandas as pd


# -----------------------------------
# Utility helpers
# -----------------------------------
def _format_percentage(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value * 100:.1f}%"


def _format_number(value: float, decimals: int = 2) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimals}f}"


# -----------------------------------
# League Overview Summary
# -----------------------------------
def league_overview_summary(league_df: pd.DataFrame) -> str:
    """
    Generates summary for League Overview page.
    """

    avg_win_pct = league_df["win_pct"].mean()
    avg_points = league_df["points_per_game"].mean()
    avg_net_rating = league_df["net_rating"].mean()

    top_team_row = league_df.sort_values("win_pct", ascending=False).iloc[0]
    top_team = top_team_row["TEAM_NAME"]
    top_team_win_pct = top_team_row["win_pct"]

    return (
        f"Across the league, teams won an average of "
        f"{_format_percentage(avg_win_pct)} of their games. "
        f"Offensively, teams scored about {_format_number(avg_points)} "
        f"points per game on average, with an overall net rating around "
        f"{_format_number(avg_net_rating)}, indicating a competitively balanced league. "
        f"The top performing team this season was **{top_team}**, "
        f"winning {_format_percentage(top_team_win_pct)} of its games."
    )


# -----------------------------------
# Team Performance Summary
# -----------------------------------
def team_performance_summary(team_df: pd.DataFrame) -> str:
    """
    Generates summary for Team Performance Deep-Dive page.
    """

    team_name = team_df["TEAM_NAME"].iloc[0]
    season = team_df["SEASON"].iloc[0]

    win_pct = team_df["win_pct"].iloc[0]
    net_rating = team_df["net_rating"].iloc[0]
    strength = team_df.get("team_strength", pd.Series(["Unknown"])).iloc[0]

    return (
        f"In the {season} season, **{team_name}** posted a win percentage of "
        f"{_format_percentage(win_pct)}. "
        f"Their net rating of {_format_number(net_rating)} indicates "
        f"that the team was classified as a **{strength}** overall."
    )


# -----------------------------------
# What Wins Games Summary ⭐
# -----------------------------------
def insight_summary(drivers: dict) -> str:
    """
    Generates summary for What Wins Games page.
    """

    positive = drivers.get("strong_positive_drivers", pd.DataFrame())
    negative = drivers.get("strong_negative_drivers", pd.DataFrame())

    summary_parts = []

    if not positive.empty:
        top_positive = positive.iloc[0]
        summary_parts.append(
            f"The strongest positive contributor to winning was "
            f"**{top_positive['metric']}**, showing a correlation of "
            f"{_format_number(top_positive['correlation_with_win_pct'])} "
            f"with win percentage."
        )

    if not negative.empty:
        top_negative = negative.iloc[0]
        summary_parts.append(
            f"On the negative side, **{top_negative['metric']}** showed "
            f"a strong inverse relationship with winning "
            f"({_format_number(top_negative['correlation_with_win_pct'])})."
        )

    if not summary_parts:
        return (
            "No single metric showed a dominant relationship with winning, "
            "indicating that team success is influenced by a combination "
            "of multiple performance factors."
        )

    return " ".join(summary_parts)


# -----------------------------------
# Team Strength Classification Summary
# -----------------------------------
def team_strength_summary(classified_df: pd.DataFrame) -> str:
    """
    Generates summary for Team Strength Classification page.
    """

    counts = classified_df["team_strength"].value_counts()
    total = counts.sum()

    parts = []
    for strength, count in counts.items():
        pct = count / total
        parts.append(f"{strength}: {_format_percentage(pct)}")

    return (
        "Team strength classification shows the following distribution — "
        + ", ".join(parts)
        + ". This highlights the competitive spread across the league."
    )


# -----------------------------------
# Win Prediction Summary (Dynamic)
# -----------------------------------
def win_prediction_summary_v2(
    team_name: str,
    probability: float,
    explanation: dict,
    accuracy: float,
) -> str:
    """
    Generates dynamic, team-aware summary for Win Prediction page.
    """

    pos_features = [f['feature'] for _, f in explanation["positive"].iterrows()]
    neg_features = [f['feature'] for _, f in explanation["negative"].iterrows()]

    pos_text = ", ".join(pos_features) if pos_features else "no major positive drivers"
    neg_text = ", ".join(neg_features) if neg_features else "no major negative drivers"

    confidence_text = (
        "very high" if probability > 0.7 else
        "moderate" if probability > 0.55 else
        "low"
    )

    summary = (
        f"**{team_name}** has a predicted win probability of {probability*100:.1f}%. "
        f"This is considered **{confidence_text} confidence** based on the model.\n\n"
        f"Top positive drivers: {pos_text}.\n"
        f"Top negative drivers: {neg_text}.\n"
        f"Model overall accuracy: {accuracy*100:.1f}%."
    )

    return summary
