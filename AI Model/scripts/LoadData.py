import pandas as pd

# Putanja do CSV-a
file_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_last5seasons.csv"

# Učitaj podatke
print(f"Loading {file_path} ...")
df = pd.read_csv(file_path)

# Prikaži osnovne informacije
print("Loaded dataframe info:")
print(df.info())
print("\nSample data:")
print(df.head())



