import polars as pl 
import pandas as pd

def load_prospects(season):
    source = f"rookie_projections\\WR Prospects.xlsx"
    sheet = str(season)
    df = pl.read_excel(
        source=source, 
        sheet_name=sheet)
    return df

seasons = [2020, 2021, 2022, 2024, 2025, 2026]

prospect_df = {}
polars_df = []

for season in seasons:
    df = load_prospects(season)
    df_name = f"prospect_{season}"
    prospect_df[df_name] = df
    print(f"Column names for the {season} season: \n {df.columns}\n\n")
    
# 1. Load all sheets into a dictionary
file_path = 'rookie_projections\\WR Prospects.xlsx'
exclude_sheets = ['2020', '2025', '2026']

# Setting sheet_name=None returns all sheets as a dictionary
all_sheets = pd.read_excel(file_path, sheet_name=None)

# 2. Filter out the sheet you don't want and combine the rest
# Use a list comprehension to get only the DataFrames for sheets not in your exclusion list
df_list = [df for name, df in all_sheets.items() if name not in exclude_sheets]

# 3. Concatenate them into a single DataFrame
# ignore_index=True ensures the final DataFrame has a continuous index
combined_df = pd.concat(df_list, 
                        ignore_index=True).to_csv('rookie_projections\\prospects.csv',
                                                           index=False)