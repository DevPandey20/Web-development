import os
import json

folder_path = "."  # Current folder

# List all JSON files
json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]

print("Total JSON files found:", len(json_files))

# Open the first JSON file
if json_files:
    with open(os.path.join(folder_path, json_files[0]), "r", encoding="utf-8") as f:
        data = json.load(f)
        print("Teams:", data["info"]["teams"])
        print("Venue:", data["info"]["venue"])
else:
    print("No JSON files found.")