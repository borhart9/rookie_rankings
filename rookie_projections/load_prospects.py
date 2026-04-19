import polars as pl 

def load_prospects(season):
    source = f"{season} Rookies\\{season} Rookie WR.xlsx"
    df = pl.read_excel(
        source=source)
    return df

seasons = [2020, 2021, 2022, 2024]

prospect_df = {}

for season in seasons:
    df = load_prospects(season)
    df_name = f"prospect_{season}"
    prospect_df[df_name] = df
    print(f"Column names for the {season} season: \n {df.columns}\n\n")

