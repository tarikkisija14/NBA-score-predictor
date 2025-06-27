import pandas as pd

input_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_cleaned.csv"
output_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_no_duplicates.csv"

df = pd.read_csv(input_path)
print("Prije uklanjanja duplikata:", len(df))

df = df.drop_duplicates(subset=["PLAYER_ID", "SEASON"])

print("Nakon uklanjanja duplikata:", len(df))
df.to_csv(output_path, index=False)
print(f"Spremljeno u {output_path}")
