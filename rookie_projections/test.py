import polars as pl
import duckdb

# Create a Polars DataFrame
df = pl.DataFrame({
    "player": ["A", "B", "C"],
    "yards": [800, 1200, 600]
})

print(f"\n{type(df)}")

# Query directly with SQL
result = duckdb.query("""
    SELECT player, yards
    FROM df
    WHERE yards > 700
""").pl()

print(result)