import os
import json
import pandas as pd

# "." means the current folder where JSON files are stored
folder_path = "."

# Set to store unique player names
players = set()

# Loop through all JSON files
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Extract players from both teams
            match_players = data["info"]["players"]
            for team in match_players:
                players.update(match_players[team])

# Convert the set to a sorted list
players_list = sorted(players)

# Save to CSV
df = pd.DataFrame(players_list, columns=["player_name"])
df.to_csv("players.csv", index=False)

print("✅ Total unique players:", len(players_list))
print("📁 'players.csv' has been created successfully!")