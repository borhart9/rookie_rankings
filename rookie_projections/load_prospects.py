import polars as pl 

def load_prospects(season):
    source = f"rookie_projections\\WR Prospects.xlsx"
    sheet = str(season)
    df = pl.read_excel(
        source=source, 
        sheet_name=sheet)
    return df

seasons = [2020, 2021, 2022, 2024]

prospect_df = {}

for season in seasons:
    df = load_prospects(season)
    df_name = f"prospect_{season}"
    prospect_df[df_name] = df
    print(f"Column names for the {season} season: \n {df.columns}\n\n")

