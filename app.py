import streamlit as st
import pandas as pd
import joblib

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Cricket AI App", layout="wide")

st.title("🏏 Cricket Analytics & AI System")
st.header("🤖 Match Intelligence Engine")

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
# LOAD MODEL
# =========================
match_model = joblib.load("match_winner_model.pkl")

# =========================
# SPLIT TEAMS CORRECTLY
# =========================
def split_teams(row):
    if isinstance(row, str) and " vs " in row:
        return row.split(" vs ")
    return [None, None]

team_rows = []

for _, row in df.iterrows():
    t1, t2 = split_teams(row["teams"])
    if t1 and t2:
        team_rows.append([t1.strip(), row["runs"], row["wickets"]])
        team_rows.append([t2.strip(), row["runs"], row["wickets"]])

team_df = pd.DataFrame(team_rows, columns=["team", "runs", "wickets"])
team_stats = team_df.groupby("team").mean().reset_index()

# =========================
# TEAM SELECTION
# =========================
st.subheader("🏏 Match Setup")

teams = sorted(team_stats["team"].unique())

team_a = st.selectbox("Select Team A", teams)
team_b = st.selectbox("Select Team B", teams)

# =========================
# PLAYER FORM SECTION
# =========================
st.subheader("🔥 Player Form Analysis")

player = st.selectbox("Select Player", sorted(df["player_name"].unique()))

player_df = df[df["player_name"] == player].sort_values("date", ascending=False)

last5 = player_df.head(5)

st.write("📊 Last 5 Matches")
st.dataframe(last5[["date", "runs", "wickets", "venue", "teams"]])

avg_runs_5 = last5["runs"].mean()
avg_wickets_5 = last5["wickets"].mean()

st.metric("Avg Runs (Last 5)", f"{avg_runs_5:.2f}")
st.metric("Avg Wickets (Last 5)", f"{avg_wickets_5:.2f}")

# FORM LABEL
if avg_runs_5 >= 40:
    form = "🔥 Excellent Form"
elif avg_runs_5 >= 20:
    form = "👍 Good Form"
else:
    form = "⚠️ Poor Form"

st.subheader(f"Form Status: {form}")

# =========================
# TEAM STRENGTH FUNCTION
# =========================
def get_strength(team_name):
    row = team_stats[team_stats["team"] == team_name]
    if not row.empty:
        return row["runs"].values[0], row["wickets"].values[0]
    return 0, 0

# =========================
# MATCH PREDICTION
# =========================
st.subheader("🏆 Match Winner Prediction")

if st.button("Predict Winner"):

    try:
        a_runs, a_wickets = get_strength(team_a)
        b_runs, b_wickets = get_strength(team_b)

        input_data = pd.DataFrame({
            "team_a_avg_runs": [a_runs],
            "team_a_avg_wickets": [a_wickets],
            "team_b_avg_runs": [b_runs],
            "team_b_avg_wickets": [b_wickets]
        })

        prediction = match_model.predict(input_data)[0]

        if prediction == 0:
            st.success(f"🏆 {team_a} is Likely to Win")
        else:
            st.success(f"🏆 {team_b} is Likely to Win")

        # Strength score
        score = (a_runs + a_wickets * 10) - (b_runs + b_wickets * 10)
        st.info(f"📊 Strength Difference Score: {score:.0f}")

    except Exception as e:
        st.error(f"Error: {e}")