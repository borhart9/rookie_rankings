from sklearn.feature_selection import mutual_info_classif
from scipy.stats import pointbiserialr
import pandas as pd
import duckdb 

features = [
'Pick_Num','Rec_Yds','Col_FPPG','Dominator',
'Vac_Tar','Age','Rec_TDs', 'draft_tier'
]

df = pd.read_csv('rookie_projections\\top24_indicator.csv')

df = duckdb.query("""
    select
        *,
        case when Pick_Num <= 32
            then 1
            when Pick_Num > 32 and Pick_Num <= 64
            then 2
            else 3
        end as draft_tier
    from 
        df               
""").df()

X = df[features]
y = df['top24_indicator']

# Mutual information
mi = mutual_info_classif(X.fillna(X.median()), y)

for f,m in zip(features,mi):
    print(f,m)

for i in range(10):
    print(mutual_info_classif(X.fillna(X.median()),y, random_state=i))