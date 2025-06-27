
import pandas as pd


file_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_last5seasons.csv"
output_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_clean.csv"


df = pd.read_csv(file_path)


df = df.drop_duplicates()


df = df.dropna(how='all')


df = df.reset_index(drop=True)


df.to_csv(output_path, index=False)

print(f"Očišćeni podaci su spremljeni u {output_path}")
