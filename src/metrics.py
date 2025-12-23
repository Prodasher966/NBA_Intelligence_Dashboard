import pandas as pd


# -----------------------------------
# Season-level aggregation
# -----------------------------------
def aggregate_team_season_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates game-level data into team-season level metrics.

    Args:
        df (pd.DataFrame): Preprocessed game-level data

    Returns:
        pd.DataFrame: Team-season aggregated metrics
    """

    grouped = df.groupby(
        ["SEASON", "TEAM_ID", "TEAM_NAME", "TEAM_ABBREVIATION"]
    )

    agg_df = grouped.agg(
        games_played=("GAME_ID", "count"),
        wins=("RESULT", "sum"),
        points_per_game=("PTS", "mean"),
        fg_pct=("FG_PCT", "mean"),
        fg3_pct=("FG3_PCT", "mean"),
        ft_pct=("FT_PCT", "mean"),
        assists_per_game=("AST", "mean"),
        rebounds_per_game=("REB", "mean"),
        steals_per_game=("STL", "mean"),
        blocks_per_game=("BLK", "mean"),
        turnovers_per_game=("TO", "mean"),
        fouls_per_game=("PF", "mean"),
        efg_pct=("EFG_PCT", "mean"),
        avg_plus_minus=("PLUS_MINUS", "mean"),
        pie=("PIE", "mean"),
    ).reset_index()

    # -----------------------------------
    # Derived metrics
    # -----------------------------------
    agg_df["win_pct"] = agg_df["wins"] / agg_df["games_played"]

    agg_df["net_rating"] = agg_df["avg_plus_minus"]

    agg_df["turnover_ratio"] = (
        agg_df["turnovers_per_game"]
        / agg_df["points_per_game"].replace(0, 1)
    )

    agg_df["off_def_balance"] = (
        agg_df["points_per_game"]
        / agg_df["avg_plus_minus"].abs().replace(0, 1)
    )

    # -----------------------------------
    # Win flag for modeling
    # -----------------------------------
    agg_df["win_flag"] = (
        agg_df["win_pct"] >= 0.5
    ).astype(int)

    return agg_df

# -----------------------------------
# League-level season summary
# -----------------------------------
def aggregate_league_season_metrics(team_season_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates team-season metrics into league-season metrics.

    Args:
        team_season_df (pd.DataFrame): Output from aggregate_team_season_metrics

    Returns:
        pd.DataFrame: League-level seasonal metrics
    """

    league_df = team_season_df.groupby("SEASON").agg(
        total_games=("games_played", "sum"),
        avg_win_pct=("win_pct", "mean"),
        avg_points_per_game=("points_per_game", "mean"),
        avg_fg_pct=("fg_pct", "mean"),
        avg_fg3_pct=("fg3_pct", "mean"),
        avg_turnovers=("turnovers_per_game", "mean"),
        avg_net_rating=("net_rating", "mean"),
    ).reset_index()

    return league_df
