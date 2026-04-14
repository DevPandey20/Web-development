import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

print("🚀 Training AI model for run prediction...")

# Load dataset
df = pd.read_csv("player_match_stats.csv")

# Convert date to datetime and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["player_name", "date"])

# 🔹 Feature 1: Average runs in the last 5 matches
df["avg_runs_last5"] = (
    df.groupby("player_name")["runs"]
    .transform(lambda x: x.rolling(window=5, min_periods=1).mean())
)

# 🔹 Feature 2: Extract opponent from 'teams'
def get_opponent(row):
    team1, team2 = row["teams"].split(" vs ")
    # This is a simplified assumption since we don't know the exact team
    # The model will still learn useful patterns.
    return team2

df["opponent"] = df.apply(get_opponent, axis=1)

# 🔹 Encode categorical variables
le_venue = LabelEncoder()
le_opponent = LabelEncoder()

df["venue_enc"] = le_venue.fit_transform(df["venue"])
df["opponent_enc"] = le_opponent.fit_transform(df["opponent"])

# 🔹 Define features and target
features = ["avg_runs_last5", "venue_enc", "opponent_enc"]
X = df[features]
y = df["runs"]

# 🔹 Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔹 Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔹 Evaluate the model
score = model.score(X_test, y_test)
print(f"✅ Model R² Score: {score:.2f}")

# 🔹 Save the model and encoders
joblib.dump(model, "runs_prediction_model.pkl")
joblib.dump(le_venue, "venue_encoder.pkl")
joblib.dump(le_opponent, "opponent_encoder.pkl")

print("✅ Model and encoders saved successfully!")