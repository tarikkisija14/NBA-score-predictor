# PrepareFeatures.py
import pandas as pd

# Učitaj dataset
df = pd.read_csv("../data/merged_full_dataset_imputed.csv")

# Pretvori datum u datetime
df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
df["GAME_YEAR"] = df["GAME_DATE"].dt.year
df["GAME_MONTH"] = df["GAME_DATE"].dt.month
df["GAME_DAY"] = df["GAME_DATE"].dt.day
df["GAME_DOW"] = df["GAME_DATE"].dt.weekday

# Label encode za timove
from sklearn.preprocessing import LabelEncoder
le_home = LabelEncoder()
le_away = LabelEncoder()
df["HOME_TEAM_ENC"] = le_home.fit_transform(df["HOME_TEAM_NAME"])
df["AWAY_TEAM_ENC"] = le_away.fit_transform(df["AWAY_TEAM_NAME"])

# Target kolone (koje se ne smiju koristiti kao inputi)
targets = ["HomeWin", "TEAM1_PTS", "TEAM2_PTS"]

# Dozvoljeni feature-i:
allowed_cols = [
    "TEAM1_ID", "TEAM2_ID",
    "HOME_TEAM_ENC", "AWAY_TEAM_ENC",
    "GAME_YEAR", "GAME_MONTH", "GAME_DAY", "GAME_DOW"
]

# X samo sa čistim kolumnama
X_clean = df[allowed_cols].copy()
X_clean.to_csv("../data/X_filtered.csv", index=False)

# Također snimi targete (da ne učitavaš svaki put)
df[targets].to_csv("../data/y_targets.csv", index=False)

print("✅ X_filtered.csv sačuvan. Oblik:", X_clean.shape)
print("📋 Kolone:", X_clean.columns.tolist())
