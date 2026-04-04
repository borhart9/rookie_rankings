# import nfl_data_py as nfl
import nflreadpy as nfl
import polars as pl


# Pull draft picks for 2023 and 2024
# 'years' parameter accepts a list of years
draft_picks = nfl.load_draft_picks([2025])

# Display the first few rows
export_df = draft_picks.filter(pl.col("position") == "WR")["pfr_player_name", "round", "pick", "team"]

export_df.write_csv("2025_draft_picks.csv")