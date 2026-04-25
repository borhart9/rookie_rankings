import nflreadpy as nfl
import polars as pl
import duckdb

draft_picks = nfl.load_draft_picks(2026)

print(draft_picks)