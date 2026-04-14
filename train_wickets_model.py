import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# -------------------------------
# Load the dataset
# -------------------------------
df = pd.read_csv("player_match_stats.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["player_name", "date"])

# -------------------------------
# Feature Engineering
# -------------------------------
# Average wickets in the last 5 matches
df["avg_wickets_last5"] = (
    df.groupby("player_name")["wickets"]
    .transform(lambda x: x.rolling(window=5, min_periods=1).mean())
)

# Extract opponent team
def get_opponent(row):
    team1, team2 = row["teams"].split(" vs ")
    # This assumes the player belongs to team1; for simplicity
    return team2

df["opponent"] = df.apply(get_opponent, axis=1)

# -------------------------------
# Encode Categorical Variables
# -------------------------------
le_venue = LabelEncoder()
le_opponent = LabelEncoder()

df["venue_enc"] = le_venue.fit_transform(df["venue"])
df["opponent_enc"] = le_opponent.fit_transform(df["opponent"])

# -------------------------------
# Prepare Features and Target
# -------------------------------
X = df[["avg_wickets_last5", "venue_enc", "opponent_enc"]]
y = df["wickets"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Train the Model
# -------------------------------
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------------------------------
# Evaluate the Model
# -------------------------------
score = model.score(X_test, y_test)
print(f"✅ Model R² Score: {score:.2f}")

# -------------------------------
# Save the Model and Encoders
# -------------------------------
joblib.dump(model, "wickets_prediction_model.pkl")
joblib.dump(le_venue, "venue_encoder.pkl")
joblib.dump(le_opponent, "opponent_encoder.pkl")

print("✅ Wickets prediction model saved successfully!")