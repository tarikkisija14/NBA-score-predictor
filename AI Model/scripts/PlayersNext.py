import pandas as pd

df = pd.read_csv("../data/player_stats_no_duplicates.csv")


df['GAME_ORDER'] = df.groupby('PLAYER_ID').cumcount() + 1

target_cols = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'TOV', 'MIN', 'PLUS_MINUS']

df = df.sort_values(['PLAYER_ID', 'GAME_ORDER'])

rolling_features = (
    df
    .groupby('PLAYER_ID')[target_cols]
    .rolling(window=5, min_periods=1)
    .mean()
)

for col in target_cols:
    df[f"{col}_rolling5"] = rolling_features[col].values

df.to_csv("../data/boxscore_prediction_dataset.csv", index=False)

print("✅ Dataset sa rolling prosek statistikama spremljen.")
