import streamlit as st
import pandas as pd
import numpy as np

# =========================
# PAGE CONFIGURATION (ONLY ONCE)
# =========================
st.set_page_config(
    page_title="CricketAI Analytics - Player Form & Match Prediction",
    page_icon="🏏",
    layout="wide"
)

# =========================
# GOOGLE SEARCH CONSOLE VERIFICATION
# =========================
st.markdown(
    """
    <meta name="google-site-verification" content="4NjBAXWE0c2DOtAVxIaeZxHPEOK9VjFW8U_qVidyc4w" />
    """,
    unsafe_allow_html=True
)

# =========================
# APP TITLE & DESCRIPTION
# =========================
st.title("🏏 CricketAI Analytics")
st.markdown("""
### Player Form • Team Strength • Match Winner Prediction

Welcome to **CricketAI Analytics**, a platform that provides:
- 🔥 Player form analysis
- 📊 Team strength comparison
- 🏆 Match winner predictions for IPL and international cricket.
""")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("player_match_stats.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# =========================
# CREATE TEAM STRENGTH TABLE
# =========================
team_rows = []
for _, row in df.iterrows():
    if isinstance(row["teams"], str) and " vs " in row["teams"]:
        t1, t2 = row["teams"].split(" vs ")
        team_rows.append([t1.strip(), row["runs"], row["wickets"]])
        team_rows.append([t2.strip(), row["runs"], row["wickets"]])

team_df = pd.DataFrame(team_rows, columns=["team", "runs", "wickets"])

team_stats = team_df.groupby("team").agg(
    avg_runs=("runs", "mean"),
    avg_wickets=("wickets", "mean"),
    matches=("runs", "count")
).reset_index()

# =========================
# MATCH SETUP
# =========================
st.header("🏏 Match Setup")

teams = sorted(team_stats["team"].unique())
team_a = st.selectbox("Select Team A", teams)
team_b = st.selectbox(
    "Select Team B",
    teams,
    index=1 if len(teams) > 1 else 0
)

# Display team strengths
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"{team_a} Strength")
    st.dataframe(team_stats[team_stats["team"] == team_a])

with col2:
    st.subheader(f"{team_b} Strength")
    st.dataframe(team_stats[team_stats["team"] == team_b])

# =========================
# PLAYER FORM ANALYSIS
# =========================
st.header("🔥 Player Form")

player = st.selectbox(
    "Select Player",
    sorted(df["player_name"].unique())
)

player_df = df[df["player_name"] == player].sort_values(
    "date", ascending=False
)

last5 = player_df.head(5)

st.subheader("Last 5 Matches")
st.dataframe(
    last5[["date", "runs", "wickets", "venue", "teams"]]
)

avg_runs_last5 = last5["runs"].mean()
avg_wickets_last5 = last5["wickets"].mean()

col1, col2 = st.columns(2)
col1.metric("Average Runs (Last 5)", f"{avg_runs_last5:.2f}")
col2.metric("Average Wickets (Last 5)", f"{avg_wickets_last5:.2f}")

# Form classification
if avg_runs_last5 >= 40:
    form = "🔥 Excellent"
elif avg_runs_last5 >= 20:
    form = "👍 Good"
else:
    form = "⚠️ Needs Improvement"

st.success(f"Form Status: {form}")

# =========================
# MATCH WINNER PREDICTION
# =========================
st.header("🏆 Match Winner Prediction")

def get_team_strength(team):
    row = team_stats[team_stats["team"] == team]
    if not row.empty:
        return row["avg_runs"].values[0], row["avg_wickets"].values[0]
    return 0, 0

if st.button("Predict Winner"):
    a_runs, a_wickets = get_team_strength(team_a)
    b_runs, b_wickets = get_team_strength(team_b)

    # Strength score formula
    strength_a = (a_runs * 0.7) + (a_wickets * 10)
    strength_b = (b_runs * 0.7) + (b_wickets * 10)

    # Probability calculation
    total_strength = strength_a + strength_b
    prob_a = (strength_a / total_strength) * 100
    prob_b = (strength_b / total_strength) * 100

    if strength_a > strength_b:
        st.success(f"🏆 {team_a} is likely to win!")
    else:
        st.success(f"🏆 {team_b} is likely to win!")

    st.info(
        f"📊 Win Probability: {team_a} ({prob_a:.1f}%) "
        f"vs {team_b} ({prob_b:.1f}%)"
    )

    st.metric(
        "Strength Score Difference",
        f"{abs(strength_a - strength_b):.2f}"
    )

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Developed with ❤️ using Streamlit")
