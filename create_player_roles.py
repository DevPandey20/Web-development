import pandas as pd

# Load the dataset
df = pd.read_csv("player_match_stats.csv")

# Function to classify player roles
def classify_role(player_df):
    avg_runs = player_df["runs"].mean()
    avg_wickets = player_df["wickets"].mean()
    
    if avg_runs >= 25 and avg_wickets < 0.5:
        return "Batter"
    elif avg_wickets >= 1 and avg_runs < 20:
        return "Bowler"
    else:
        return "All-Rounder"

# Create a list to store roles
roles = []

# Loop through each unique player
for player in df["player_name"].unique():
    player_df = df[df["player_name"] == player]
    role = classify_role(player_df)
    roles.append({
        "player_name": player,
        "role": role
    })

# Convert to DataFrame
roles_df = pd.DataFrame(roles)

# Save to CSV
roles_df.to_csv("player_roles.csv", index=False)

print("✅ player_roles.csv created successfully!")
print("Total players:", len(roles_df))