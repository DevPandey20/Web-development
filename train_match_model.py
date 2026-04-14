import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("match_data.csv")

# =========================
# FEATURES (INPUTS)
# =========================
X = df[[
    "team_a_avg_runs",
    "team_a_avg_wickets",
    "team_b_avg_runs",
    "team_b_avg_wickets"
]]

# =========================
# TARGET (OUTPUT)
# =========================
y = df["winner"]

# =========================
# TRAIN MODEL
# =========================
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "match_winner_model.pkl")

print("✅ Match winner model trained successfully!")