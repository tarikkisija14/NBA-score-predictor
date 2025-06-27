import pandas as pd

file_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_clean.csv"
output_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_typed.csv"

df = pd.read_csv(file_path)

# Primjer: pretvori kolonu SEASON u kategoriju
df["SEASON"] = df["SEASON"].astype("category")

# Ako želiš npr. TEAM_ABBREVIATION kao kategoriju
df["TEAM_ABBREVIATION"] = df["TEAM_ABBREVIATION"].astype("category")

# Ako želiš provjeriti sve tipove:
print("Tipovi kolona nakon konverzije:")
print(df.dtypes)

# Snimi dataset
df.to_csv(output_path, index=False)

print(f"Dataset sa konvertiranim kolonama spremljen u {output_path}")
