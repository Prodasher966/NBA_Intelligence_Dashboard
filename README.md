# 🏀 NBA Team Intelligence Dashboard

**A data-driven exploration of what wins games in the NBA (2012–2024)**

---

## 📌 Project Overview

The **NBA Team Intelligence Dashboard** is an interactive analytics application built using **Streamlit** that transforms raw NBA game data into actionable insights at the league and team level.

This project goes beyond basic visualizations by answering deeper analytical questions such as:

- What truly drives winning in the NBA?
- How do teams evolve across seasons?
- Can team-level performance metrics predict winning outcomes?
- How can complex analytics be summarized clearly for non-technical users?

The dashboard is designed as a **portfolio-grade analytics product** — clean, minimalistic, modern, and insight-focused.

---

## 🎯 Objectives

- Analyze NBA team performance trends from 2012 to 2024  
- Identify key performance metrics that correlate with winning  
- Classify teams based on overall strength  
- Build a machine learning model to predict win probability  
- Generate auto-written summaries that explain insights in simple language  

---

## 📂 Dataset

**Source:** Kaggle – NBA Data (2012–2024)  
**Granularity:** Game-level data  

**Coverage:**
- Team statistics  
- Shooting efficiency  
- Advanced metrics (EFG%, PIE, Net Rating)  
- Game results  

The dataset is intentionally large and realistic, making it suitable for real-world analytics workflows.

---

## 🧠 Dashboard Pages & Features

### 1️⃣ League Overview

- Big-picture view of the NBA  
- League-wide averages and distributions  
- Overall competitiveness analysis  
- Auto-generated league summary  

📌 **Purpose:** Understand how balanced or dominant the league is across seasons.

---

### 2️⃣ Team Performance Deep-Dive

- Detailed analysis of a selected team  
- Season-level KPIs (Win %, Net Rating, Points/Game)  
- Multi-season performance trends  
- Team strength classification  
- Metric Definitions Panel for clarity  
- Dynamic team summary  

📌 **Purpose:** Tell a clear performance story for any NBA team.

---

### 3️⃣ What Wins Games? ⭐

- Core insight section  
- Correlation analysis between metrics and win percentage  
- Identification of strongest positive & negative drivers  
- Clear interpretation of results via auto summaries  

📌 **Purpose:** Answer the most important question — what actually matters for winning?

---

### 4️⃣ Team Strength Classification

- Team categorization  
- Teams classified as:
  - Elite  
  - Strong  
  - Average  
  - Weak  
- Distribution analysis across the league  
- Insight-driven summary  

📌 **Purpose:** Quickly understand competitive tiers within the NBA.

---

### 5️⃣ Win Prediction

- Machine Learning application  
- Logistic Regression model  
- Uses team-season metrics to predict win probability  
- Model accuracy reporting  
- Feature importance visualization  
- Explainable predictions (no black box)  

📌 **Purpose:** Demonstrate applied machine learning with explainability.

---

## 🤖 Machine Learning Details

- **Model:** Logistic Regression  
- **Target:** Win Flag (Win % ≥ 50%)  

**Features Used:**
- FG%  
- 3PT%  
- FT%  
- Assists/Game  
- Rebounds/Game  
- Turnovers/Game  
- Net Rating  
- EFG%  
- PIE  

**Preprocessing:**
- Feature scaling using StandardScaler  

**Evaluation Metric:** Accuracy  

The model is intentionally simple and interpretable — clarity over complexity.

---

## 🧠 Auto Summary Engine (Key Highlight)

Each dashboard page includes an auto-generated narrative summary that:

- Translates charts into plain English  
- Highlights the most important insights  
- Makes the dashboard accessible to non-technical users  

📌 This feature simulates how analytics insights are presented to stakeholders in real-world environments.

---
## 🗂️ Project Structure

```text
NBA_Team_Intelligence_Dashboard/
│
├── app.py                      # Main Streamlit app
│
├── pages/                      # Dashboard pages
│   ├── 1_League_Overview.py
│   ├── 2_Team_Performance_DeepDive.py
│   ├── 3_What_Wins_Games.py
│   ├── 4_Team_Strength_Classification.py
│   └── 5_Win_Prediction.py
│
├── src/                        # Core analytics logic
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── metrics.py
│   ├── insights.py
│   ├── classification.py
│   ├── model.py
│   ├── summaries.py
│   └── metric_definitions.py
│
├── assets/                     # Custom CSS / styling
│
├── requirements.txt
├── .gitignore
└── README.md
```

📌 Clean separation between logic, presentation, and analytics.

---

## ⚙️ How to Run the Project

### 1️⃣ Install dependencies

pip install -r requirements.txt

### 2️⃣ Run the dashboard

streamlit run app.py


📌 No need to run src files manually — they are imported by the app.

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Pandas  
- Plotly  
- Scikit-learn  
- Kaggle Dataset  

---

## 📈 Why This Project Matters (For Recruiters)

This project demonstrates:

✅ End-to-end data analytics workflow  
✅ Clean modular code structure  
✅ Business-oriented insight generation  
✅ Explainable machine learning  
✅ Strong data storytelling  
✅ Production-style dashboard design  

📌 It reflects how real analytics products are built — not just notebooks.

---

## 🚀 Future Improvements (Optional)

- Team-to-team comparison mode  
- Playoff-specific analysis  
- Advanced ML models  
- Player-level integration  

*(Project intentionally considered complete for portfolio use.)*

---

## 🙌 Acknowledgements

- NBA & Kaggle community for the dataset  
- Streamlit & open-source ecosystem  

⭐ If you liked this project, feel free to star the repository!
