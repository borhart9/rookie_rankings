import polars as pl 
import duckdb as db

stats = pl.read_csv('rookie_projections\stats.csv')



prospects = pl.read_csv('rookie_projections\prospects.csv')


indicator = db.query("""
WITH stats_dedup AS (
    SELECT *
    FROM (
        SELECT 
            s.*,
            ROW_NUMBER() OVER (
                PARTITION BY player 
                ORDER BY season ASC
            ) AS rn
        FROM stats s
    )
    WHERE rn = 1
)
SELECT 
    p.*,
    s.*,
    CASE 
        WHEN s.season_rank IS NOT NULL THEN 1
        ELSE 0
    END AS top24_indicator
FROM prospects p
LEFT JOIN stats_dedup s
    ON p.player = s.player
where 
    Pick_num != 'Undrafted'
""")

indicator.to_csv('rookie_projections\\top24_indicator.csv')