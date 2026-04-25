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

def get_playoff_bracket(league_ids, seasons):
    playoff_brackets = {}
    for season in seasons:
        season_str = str(season)
        league_id = league_ids[season]
        full_url = f"{BASE}/league/{league_id}/winners_bracket"
        bracket = requests.get(full_url).json()
        playoff_brackets[season] = bracket
        
    return playoff_brackets



user_id = get_user_id("borhart9")


seasons = [2022, 2023, 2024, 2025]
league_ids = get_league_ids(user_id, seasons=seasons)

brackets = get_playoff_bracket(league_ids, seasons)
