import streamlit as st
import plotly.express as px

from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.metrics import aggregate_team_season_metrics
from src.classification import classify_team_strength
from src.summaries import team_performance_summary
from src.metric_definitions import METRIC_DEFINITIONS

# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="Team Performance Deep-Dive | NBA Team Intelligence",
    layout="wide",
)

st.title("📊 Team Performance Deep-Dive")
st.markdown(
    "Analyze a team's season-level performance across key metrics."
)

# ---------------------------------
# Side Bar Customization
# ---------------------------------
st.markdown(
    """
    <style>
    /* Sidebar spacing */
    section[data-testid="stSidebar"] ul {
        gap: 12px;
    }

    /* Sidebar text size */
    section[data-testid="stSidebar"] span {
        font-size: 16px;
    }

    /* Sidebar page labels spacing */
    section[data-testid="stSidebar"] li {
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Metric Definitions Panel
# -----------------------------------
with st.expander("ℹ️ Metric Definitions"):
    for metric, definition in METRIC_DEFINITIONS.items():
        st.markdown(f"**{metric}**: {definition}")

# -----------------------------------
# Load & prepare data
# -----------------------------------
df_raw = load_data()
df_clean = preprocess_data(df_raw)

team_season_df = aggregate_team_season_metrics(df_clean)
classified_df = classify_team_strength(team_season_df)

# -----------------------------------
# Filters: Team & Season
# -----------------------------------
teams = sorted(classified_df["TEAM_NAME"].unique())
selected_team = st.selectbox("Select Team", teams)

team_df = classified_df[
    classified_df["TEAM_NAME"] == selected_team
].sort_values("SEASON")

seasons = sorted(team_df["SEASON"].unique())
selected_season = st.selectbox("Select Season", seasons)

selected_team_df = team_df[
    team_df["SEASON"] == selected_season
]

# -----------------------------------
# KPI Metrics
# -----------------------------------
st.subheader("🏀 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Win %",
        f"{selected_team_df['win_pct'].iloc[0] * 100:.1f}%"
    )

with col2:
    st.metric(
        "Points / Game",
        f"{selected_team_df['points_per_game'].iloc[0]:.1f}"
    )

with col3:
    st.metric(
        "Net Rating",
        f"{selected_team_df['net_rating'].iloc[0]:.2f}"
    )

with col4:
    st.metric(
        "Team Strength",
        selected_team_df["team_strength"].iloc[0]
    )

# -----------------------------------
# Season Trend: Win %
# -----------------------------------
st.subheader("📈 Season Trend: Win Percentage")

fig_trend = px.line(
    team_df,
    x="SEASON",
    y="win_pct",
    markers=True,
    labels={"win_pct": "Win Percentage"},
    title=f"{selected_team} Win % Over Seasons"
)

st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------------
# Season Trend Analytics: Multiple Metrics
# -----------------------------------
st.subheader("📊 Season Trends: Key Metrics")

metrics_to_plot = [
    "win_pct",
    "points_per_game",
    "net_rating",
    "efg_pct",
    "pie"
]

fig_metrics = px.line(
    team_df,
    x="SEASON",
    y=metrics_to_plot,
    markers=True,
    labels={
        "value": "Metric Value",
        "variable": "Metric",
        "SEASON": "Season"
    },
    title=f"{selected_team} Key Metrics Over Seasons"
)

st.plotly_chart(fig_metrics, use_container_width=True)

# -----------------------------------
# Season Trend Summary
# -----------------------------------
st.subheader("🧠 Season Trend Summary")

latest = selected_team_df.iloc[0]
previous_season = team_df[team_df["SEASON"] < selected_season].sort_values("SEASON", ascending=False).head(1)

trend_text = ""
if not previous_season.empty:
    prev = previous_season.iloc[0]
    for metric in metrics_to_plot:
        change = latest[metric] - prev[metric]
        trend_text += f"- **{metric}** changed by {change:.2f} from last season.\n"
else:
    trend_text = "No previous season data available for comparison."

st.markdown(trend_text)

# -----------------------------------
# Auto-generated dynamic summary ⭐
# -----------------------------------
st.subheader("🧠 Team Summary")

summary_text = team_performance_summary(selected_team_df)
st.markdown(summary_text)