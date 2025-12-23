import streamlit as st
import plotly.express as px

from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.metrics import aggregate_team_season_metrics
from src.summaries import league_overview_summary


# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="League Overview | NBA Team Intelligence",
    layout="wide",
)

st.title("🏀 NBA League Overview")
st.markdown(
    "A high-level view of league-wide performance trends across seasons."
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

# 🔧 Correct metrics function
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
# KPI Metrics (validated outputs)
# -----------------------------------
st.subheader("📊 League KPIs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Win %",
        f"{filtered_df['win_pct'].mean() * 100:.1f}%"
    )

with col2:
    st.metric(
        "Avg Points per Game",
        f"{filtered_df['points_per_game'].mean():.1f}"
    )

with col3:
    st.metric(
        "Avg Net Rating",
        f"{filtered_df['net_rating'].mean():.2f}"
    )

# -----------------------------------
# Win % distribution
# -----------------------------------
st.subheader("🏆 Win Percentage Distribution")

fig_win_dist = px.histogram(
    filtered_df,
    x="win_pct",
    nbins=20,
    labels={"win_pct": "Win Percentage"},
)

st.plotly_chart(fig_win_dist, use_container_width=True)

# -----------------------------------
# Points vs Net Rating
# -----------------------------------
st.subheader("📈 Offense vs Impact")

fig_scatter = px.scatter(
    filtered_df,
    x="points_per_game",
    y="net_rating",
    hover_name="TEAM_NAME",
    color="SEASON",
    labels={
        "points_per_game": "Points per Game",
        "net_rating": "Net Rating",
    },
)

st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------------
# Auto-generated summary ⭐
# -----------------------------------
st.subheader("🧠 League Summary")

summary_text = league_overview_summary(team_season_df)
st.markdown(summary_text)