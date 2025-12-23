import streamlit as st
import plotly.express as px

from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.metrics import aggregate_team_season_metrics
from src.classification import classify_team_strength
from src.summaries import team_strength_summary


# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="Team Strength Classification | NBA Team Intelligence",
    layout="wide",
)

st.title("🏷️ Team Strength Classification")
st.markdown(
    "Teams are classified based on win percentage, net rating, "
    "and ball control efficiency."
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
classified_df = classify_team_strength(team_season_df)

# -----------------------------------
# Season filter
# -----------------------------------
seasons = sorted(classified_df["SEASON"].unique())
selected_season = st.selectbox(
    "Select Season",
    seasons,
    index=len(seasons) - 1,
)

season_df = classified_df[
    classified_df["SEASON"] == selected_season
]

# -----------------------------------
# Distribution of team strength
# -----------------------------------
st.subheader("📊 Team Strength Distribution")

fig_dist = px.pie(
    season_df,
    names="team_strength",
    title="Team Strength Breakdown",
)

st.plotly_chart(fig_dist, use_container_width=True)

# -----------------------------------
# Table view
# -----------------------------------
st.subheader("📋 Team Classification Table")

display_cols = [
    "TEAM_NAME",
    "win_pct",
    "net_rating",
    "turnover_ratio",
    "team_strength",
]

st.dataframe(
    season_df[display_cols].sort_values(
        by="win_pct",
        ascending=False,
    ),
    use_container_width=True,
)

# -----------------------------------
# Auto-generated summary ⭐
# -----------------------------------
st.subheader("🧠 Classification Summary")

summary_text = team_strength_summary(classified_df)  # classified_df has team_strength column
st.markdown(summary_text)