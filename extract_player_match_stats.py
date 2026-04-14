import os
import json
import pandas as pd

print("🚀 Extracting player match statistics...")

folder_path = "."  # JSON files are in the same folder
records = []

# Loop through all JSON files
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        match_id = file_name.replace(".json", "")
        
        with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as f:
            data = json.load(f)

            # Extract match information
            info = data.get("info", {})
            date = info.get("dates", ["Unknown"])[0]
            venue = info.get("venue", "Unknown")
            teams = " vs ".join(info.get("teams", []))

            # Dictionaries to store runs and wickets per player
            player_runs = {}
            player_wickets = {}

            # Loop through innings
            for inning in data.get("innings", []):
                for over in inning.get("overs", []):
                    for delivery in over.get("deliveries", []):
                        # Batting runs
                        batter = delivery.get("batter")
                        runs = delivery.get("runs", {}).get("batter", 0)
                        if batter:
                            player_runs[batter] = player_runs.get(batter, 0) + runs

                        # Bowling wickets
                        for wicket in delivery.get("wickets", []):
                            bowler = delivery.get("bowler")
                            if bowler:
                                player_wickets[bowler] = player_wickets.get(bowler, 0) + 1

            # Combine batting and bowling data
            all_players = set(player_runs.keys()).union(player_wickets.keys())

            for player in all_players:
                records.append({
                    "match_id": match_id,
                    "date": date,
                    "player_name": player,
                    "runs": player_runs.get(player, 0),
                    "wickets": player_wickets.get(player, 0),
                    "venue": venue,
                    "teams": teams
                })

# Create DataFrame and save to CSV
df = pd.DataFrame(records)
df.to_csv("player_match_stats.csv", index=False)

print("✅ 'player_match_stats.csv' created successfully!")
print("📊 Total records:", len(df))