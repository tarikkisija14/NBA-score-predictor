
import pandas as pd

base_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/"

player_files = [
    "all_players.csv",
    "career_stats_top10.csv",
    "player_stats_2023-24.csv",
    "player_stats_clean.csv",
    "player_stats_cleaned.csv",
    "player_stats_features.csv",
    "player_stats_last5seasons.csv",
    "player_stats_no_duplicates.csv",
    "player_stats_typed.csv"
]

for filename in player_files:
    file_path = base_path + filename
    print(f"\n--- Učitavanje: {filename} ---")
    try:
        df = pd.read_csv(file_path)
        print(f"Dimenzije: {df.shape}")
        print(f"Kolone:\n{list(df.columns)}")
        print(f"Prvih 3 reda:\n{df.head(3)}")
    except Exception as e:
        print(f"Greška pri učitavanju {filename}: {e}")
