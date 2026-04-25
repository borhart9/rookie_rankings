import requests
import pandas as pd

BASE = "https://api.sleeper.app/v1"

def get_user_id(username):
    full_url = f"{BASE}/user/{username}"
    user = requests.get(full_url).json()
    user_id = user["user_id"]
    return user_id

def get_league_ids(user_id, seasons):
    league_ids = {}
    for season in seasons:
        full_url = f"{BASE}/user/{user_id}/leagues/nfl/{season}"
        leagues = requests.get(full_url).json()
        for league in leagues:
            if league["name"] == "Empire":
                league_ids[season] = (league["league_id"])

    return league_ids

# def get_playoff_bracket(league_ids):
#     playoff_brackets = []
#     for league_id in league_ids:
#         full_url = f"{BASE}/league/{league_id}/winners_bracket"
#         bracket = requests.get(full_url).json()
        



user_id = get_user_id("borhart9")
print(user_id)

seasons = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
league_ids = get_league_ids(user_id, seasons=seasons)
print(league_ids)