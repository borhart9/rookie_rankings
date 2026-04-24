import nflreadpy as nfl
import polars as pl
import duckdb

stats = nfl.load_player_stats(seasons=2020)

results = duckdb.query("""
    select
        team, sum(targets), position
    from 
        stats
    where 
        position in ('WR', 'TE', 'RB')
    group by
        team, position
    """)

pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_rows(-1)
print(results)