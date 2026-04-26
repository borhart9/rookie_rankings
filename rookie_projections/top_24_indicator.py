import polars as pl 
import duckdb as db

stats = pl.read_csv('rookie_projections\stats.csv')



prospects = pl.read_csv('rookie_projections\prospects.csv')



indicator = db.query("""
    select 
        p.player,
    from 
        prospects p
        left join stats s
            on p.player = s.player
    where 
        s.season_rank is not null
""")

print(indicator)