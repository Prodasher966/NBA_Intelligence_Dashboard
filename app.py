import streamlit as st
from pathlib import Path

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
# Page config
# -----------------------------------
st.set_page_config(
    page_title="NBA Team Intelligence Dashboard",
    page_icon="🏀",
    layout="wide",
)

# -----------------------------------
# Load global CSS
# -----------------------------------
def load_css():
    css_path = Path("assets/style.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )

load_css()

# -----------------------------------
# App Introduction
# -----------------------------------
st.title("🏀 NBA Team Intelligence Dashboard")

st.markdown(
    """
    **NBA Team Intelligence** is a data-driven analytics dashboard built to explore
    how team-level performance translates into winning outcomes across NBA seasons
    (2012–2024).

    This project focuses on **interpretability, insights, and decision-making**
    rather than just raw statistics.
    """
)

# -----------------------------------
# What this dashboard answers
# -----------------------------------
st.subheader("🔍 What This Dashboard Explores")

st.markdown(
    """
    - How competitive is the league across seasons?
    - How does a specific team perform over time?
    - Which metrics actually drive winning?
    - How can teams be objectively classified?
    - Can we predict wins using performance data?
    """
)

# -----------------------------------
# Page guide
# -----------------------------------
st.subheader("📂 Dashboard Sections")

st.markdown(
    """
    **League Overview**  
    High-level trends and league-wide performance metrics.

    **Team Performance Deep-Dive**  
    Analyze season-wise performance of individual teams.

    **What Wins Games?** ⭐  
    Identify the strongest performance drivers behind winning.

    **Team Strength Classification**  
    Rule-based categorization of teams into performance tiers.

    **Win Prediction**  
    Demonstration of an interpretable machine learning model.
    """
)

# -----------------------------------
# Footer note
# -----------------------------------
st.markdown(
    "---\n"
    "📌 *Built as a personal analytics portfolio project using Streamlit, "
    "Pandas, Plotly, and Scikit-learn.*"
)
