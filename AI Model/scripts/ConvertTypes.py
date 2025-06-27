import pandas as pd

input_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_no_duplicates.csv"
output_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_typed.csv"

df = pd.read_csv(input_path)

for col in df.columns:
    if df[col].dtype == "object":
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass  # ostavi string kolonu ako ne može

print(df.dtypes)

df.to_csv(output_path, index=False)
print(f"Spremljeno u {output_path}")
