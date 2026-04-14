import pandas as pd
import numpy as np

print("🚀 Calculating Weighted Player Form Index...")

# Load the dataset
df = pd.read_csv("player_match_stats.csv")

# Convert date to datetime and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["player_name", "date"])

def calculate_weighted_form(group):
    # Select last 5 matches
    last5 = group.tail(5).sort_values(by="date", ascending=False).copy()
    
    # Assign weights: 5 (most recent) to 1
    weights = np.arange(len(last5), 0, -1)
    last5["weight"] = weights
    
    # Calculate weighted averages
    weighted_runs = np.average(last5["runs"], weights=last5["weight"])
    weighted_wickets = np.average(last5["wickets"], weights=last5["weight"])
    
    # Batting and Bowling Indices
    batting_index = weighted_runs
    bowling_index = weighted_wickets * 25
    
    # Overall Player Form Index
    overall_pfi = 0.7 * batting_index + 0.3 * bowling_index
    
    return pd.Series({
        "matches_considered": len(last5),
        "weighted_avg_runs": round(weighted_runs, 2),
        "weighted_avg_wickets": round(weighted_wickets, 2),
        "batting_form_index": round(batting_index, 2),
        "bowling_form_index": round(bowling_index, 2),
        "overall_player_form_index": round(overall_pfi, 2)
    })

# Apply the function to each player
player_form = df.groupby("player_name").apply(calculate_weighted_form).reset_index()

# Save the results
player_form.to_csv("weighted_player_form_index.csv", index=False)

print("✅ 'weighted_player_form_index.csv' created successfully!")
print("📊 Total players analyzed:", len(player_form))