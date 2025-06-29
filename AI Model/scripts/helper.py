import pandas as pd

# Učitaj CSV
df = pd.read_csv("../data/player_stats_no_duplicates.csv")

# Ispis svih kolona
print("✅ Kolone u DataFrame-u:")
print(df.columns.tolist())

# Ispis prvih nekoliko redova
print("\n✅ Prvih 5 redova:")
print(df.head())
