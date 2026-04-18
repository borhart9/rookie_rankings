import polars as pl 

prospect_data = pl.read_excel(
    source="2026 Rookies\\2026 Rookie WR.xlsx",
    sheet_name="Sheet1")

print(prospect_data.head(10))