import pandas as pd

print("🚀 Calculating Player Form Index...")

# Load player match statistics
df = pd.read_csv("player_match_stats.csv")

# Convert date column to datetime for proper sorting
df["date"] = pd.to_datetime(df["date"])

# Sort by player and date
df = df.sort_values(by=["player_name", "date"])

# Function to calculate Player Form Index for each player
def calculate_pfi(group):
    last_5_matches = group.tail(5)
    avg_runs = last_5_matches["runs"].mean()
    avg_wickets = last_5_matches["wickets"].mean()
    
    # Player Form Index formula
    pfi = (avg_runs * 0.7) + (avg_wickets * 25 * 0.3)
    
    return pd.Series({
        "matches_considered": len(last_5_matches),
        "avg_runs_last5": round(avg_runs, 2),
        "avg_wickets_last5": round(avg_wickets, 2),
        "player_form_index": round(pfi, 2)
    })

# Apply the function to each player
player_form = df.groupby("player_name").apply(calculate_pfi).reset_index()

# Save to CSV
player_form.to_csv("player_form_index.csv", index=False)

print("✅ 'player_form_index.csv' created successfully!")
print("📊 Total players analyzed:", len(player_form))