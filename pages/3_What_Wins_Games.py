import streamlit as st
import plotly.express as px

from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.metrics import aggregate_team_season_metrics
from src.insights import (
    calculate_win_correlations,
    identify_key_win_drivers,
    prepare_scatter_data,
)
from src.summaries import insight_summary


# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="What Wins Games? | NBA Team Intelligence",
    layout="wide",
)

st.title("🧠 What Wins Games?")
st.markdown(
    "This section explores which team-level performance metrics "
    "have the strongest relationship with winning."
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
# Load & prepare data
# -----------------------------------
df_raw = load_data()
df_clean = preprocess_data(df_raw)
team_season_df = aggregate_team_season_metrics(df_clean)

# -----------------------------------
# Season filter
# -----------------------------------
seasons = sorted(team_season_df["SEASON"].unique())
selected_seasons = st.multiselect(
    "Select Seasons",
    seasons,
    default=seasons,
)

filtered_df = team_season_df[
    team_season_df["SEASON"].isin(selected_seasons)
]

# -----------------------------------
# Correlation analysis
# -----------------------------------
st.subheader("📊 Metric Correlation with Winning")

corr_df = calculate_win_correlations(filtered_df)

fig_corr = px.bar(
    corr_df,
    x="correlation_with_win_pct",
    y="metric",
    orientation="h",
    labels={
        "correlation_with_win_pct": "Correlation with Win %",
        "metric": "Metric",
    },
)

st.plotly_chart(fig_corr, use_container_width=True)

# -----------------------------------
# Identify key drivers
# -----------------------------------
drivers = identify_key_win_drivers(corr_df)

# -----------------------------------
# Scatter relationship explorer
# -----------------------------------
st.subheader("🔍 Explore Metric vs Winning")

available_metrics = corr_df["metric"].tolist()
selected_metric = st.selectbox(
    "Select Metric",
    available_metrics,
)

scatter_df = prepare_scatter_data(
    filtered_df,
    x_metric=selected_metric,
)

fig_scatter = px.scatter(
    scatter_df,
    x=selected_metric,
    y="win_pct",
    hover_name="TEAM_NAME",
    color="SEASON",
    labels={
        selected_metric: selected_metric.replace("_", " ").title(),
        "win_pct": "Win Percentage",
    },
)

st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------------
# Auto-generated insight summary ⭐
# -----------------------------------
st.subheader("🧠 Insight Summary")

summary_text = insight_summary(drivers)  # drivers is dict of strong positive/negative metrics
st.markdown(summary_text)
