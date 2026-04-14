import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load data
df = pd.read_csv("player_match_stats.csv")

# -------------------------
# Create simple match dataset
# -------------------------
df["team"] = df["teams"].apply(lambda x: x.split(" vs ")[0])

match_data = df.groupby(["match_id", "team"]).agg({
    "runs": "sum",
    "wickets": "sum"
}).reset_index()

# Create winner label (simple logic: higher runs = winner)
match_data["opponent_runs"] = match_data["runs"].shift(-1)
match_data["winner"] = (match_data["runs"] > match_data["opponent_runs"]).astype(int)

match_data = match_data.dropna()

# Encode team
le_team = LabelEncoder()
match_data["team_enc"] = le_team.fit_transform(match_data["team"])

# Features & target
X = match_data[["team_enc", "runs", "wickets"]]
y = match_data["winner"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

# Save model
joblib.dump(model, "match_winner_model.pkl")
joblib.dump(le_team, "team_encoder.pkl")

print("✅ Match winner model saved!")