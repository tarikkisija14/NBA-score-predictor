import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import json

# Učitavanje podataka
df = pd.read_csv("../data/merged_enhanced.csv")
target = df["HomeWin"]

# Drop target i druge nepotrebne kolone
X = df.drop(columns=[col for col in ["HomeWin", "TEAM1_PTS", "TEAM2_PTS", "GAME_ID", "GAME_DATE", "HOME_TEAM_NAME", "AWAY_TEAM_NAME", "TEAM_MATCHUP", "SEASON"] if col in df.columns])

# Samo numeričke kolone
X = X.select_dtypes(include=["number"])

# Fit Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, target)

# Rangiraj feature-e po važnosti
feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
top_features = feature_importances.head(25)

# Sačuvaj top feature-e
top_features.to_csv("../outputs/top_features_HomeWin.csv")
json.dump(list(top_features.index), open("../data/top_features_HomeWin.json", "w"))

print("✅ Selektovani top feature-i za HomeWin:")
print(top_features)
