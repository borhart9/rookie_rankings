import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold

features = ["Rec_TDs", "Pick_Num", "Vac_Tar"]

df = pd.read_csv('rookie_projections\\top24_indicator.csv')

X = df[features]
y = df['top24_indicator']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=.25,
    stratify=y,
    random_state=42
)


model = Pipeline([
    ('scale', StandardScaler()),
    ('logit', LogisticRegression())
])

model.fit(X_train,y_train)


probs = model.predict_proba(X_test)[:,1]

auc = roc_auc_score(y_test, probs)

# print(auc)

cv = RepeatedStratifiedKFold(
    n_splits=5,
    n_repeats=20,
    random_state=42
)

scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring='roc_auc'
)

logit = model.named_steps['logit']

# for f,c in zip(features, logit.coef_[0]):
#     print(f,c)

# print(np.exp(logit.coef_[0]))

incoming_rookies = pd.read_csv('rookie_projections\\WR Prospects - 2026.csv')
incoming_rookies = incoming_rookies[["Player", "Team", "Pick_Num", "Rec_TDs", "Vac_Tar"]]
# lemon = pd.DataFrame({'Player': ['Lemon2'], 
#                       'Team': ['PHI'],
#                       'Pick_num': ['20'],
#                       'Rec_TDs': ['11'],
#                       'Vac_Tar': ['35.5']})
# incoming_rookies = pd.concat([incoming_rookies, lemon], ignore_index=True)

incoming_rookies["top24_indicator"] = model.predict_proba(incoming_rookies[features])[:,1]
lemon_data = [[11, 20, 35.5]]

print(model.predict_proba(lemon_data)[:,1])

output = incoming_rookies[["Player", "Team", "Pick_Num", "Rec_TDs", "Vac_Tar", "top24_indicator"]].to_csv('rookie_projections\\projection.csv')


