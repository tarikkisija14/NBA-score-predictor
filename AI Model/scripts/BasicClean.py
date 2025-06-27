import pandas as pd


input_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_features.csv"
output_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_cleaned.csv"


df = pd.read_csv(input_path)
print("Prije čišćenja:", df.shape)


string_cols = df.select_dtypes(include=["object"]).columns
for col in string_cols:
    df[col] = df[col].str.strip()


df = df.fillna(0)


df = df[df["PLAYER_ID"].notnull()]

print("Nakon čišćenja:", df.shape)
df.to_csv(output_path, index=False)
print(f"Spremljeno u {output_path}")

