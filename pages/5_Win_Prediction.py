import streamlit as st
import plotly.express as px
import pandas as pd
from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.metrics import aggregate_team_season_metrics
from src.insights import explain_win_prediction
from src.model import (
    train_win_prediction_model,
    predict_win_probability,
)
from src.summaries import win_prediction_summary_v2


# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="Win Prediction | NBA Team Intelligence",
    layout="wide",
)

st.title("🎯 Win Prediction")
st.markdown(
    "This section demonstrates how team-level performance metrics "
    "can be used to predict game outcomes."
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
# Train model
# -----------------------------------
model_output = train_win_prediction_model(team_season_df)

model = model_output["model"]
accuracy = model_output["accuracy"]

# -----------------------------------
# Model performance
# -----------------------------------
st.subheader("📈 Model Performance")

st.metric(
    "Prediction Accuracy",
    f"{accuracy * 100:.2f}%"
)

# -----------------------------------
# Predict win probability (interactive)
# -----------------------------------
st.subheader("🔮 Predict Win Probability")

teams = sorted(team_season_df["TEAM_NAME"].unique())
selected_team = st.selectbox("Select Team", teams)

team_data = team_season_df[
    team_season_df["TEAM_NAME"] == selected_team
].sort_values("SEASON", ascending=False)

latest_team_data = team_data.head(1)

probability = predict_win_probability(
    model,
    latest_team_data,
).iloc[0]

st.metric(
    "Predicted Win Probability",
    f"{probability * 100:.1f}%"
)

# -----------------------------------
# Feature impact visualization
# -----------------------------------
st.subheader("📊 Feature Importance (Coefficients)")

coefficients = model.named_steps["model"].coef_[0]
features = model_output["feature_names"]

coef_df = pd.DataFrame(
    {
        "Feature": features,
        "Coefficient": coefficients,
    }
).sort_values(
    by="Coefficient",
    ascending=False,
)

fig_coef = px.bar(
    coef_df,
    x="Coefficient",
    y="Feature",
    orientation="h",
)

st.plotly_chart(fig_coef, use_container_width=True)

st.subheader("🔍 Why This Prediction?")

explanation = explain_win_prediction(
    team_row=latest_team_data.iloc[0],
    feature_names=model_output["feature_names"],
    coefficients=coefficients,
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✅ Positive Drivers")
    for _, row in explanation["positive"].iterrows():
        st.markdown(f"- **{row['feature']}**")

with col2:
    st.markdown("### ⚠️ Negative Drivers")
    for _, row in explanation["negative"].iterrows():
        st.markdown(f"- **{row['feature']}**")

# -----------------------------------
# Auto-generated summary ⭐
# -----------------------------------
st.subheader("🧠 Prediction Summary")

avg_probability = team_season_df["win_flag"].mean()

summary_text = win_prediction_summary_v2(
    team_name=selected_team,
    probability=probability,
    explanation=explanation,
    accuracy=accuracy,
)

st.markdown(summary_text)