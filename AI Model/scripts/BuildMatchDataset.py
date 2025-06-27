import pandas as pd

input_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/team_stats_last5seasons.csv"
output_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/match_dataset.csv"

df = pd.read_csv(input_path)


seasons = df["SEASON"].unique()
games = []

for season in seasons:
    season_df = df[df["SEASON"] == season].reset_index(drop=True)
    for i in range(len(season_df)):
        for j in range(len(season_df)):
            if i != j:
                home = season_df.iloc[i]
                away = season_df.iloc[j]
                row = {}
                for col in df.columns:
                    row[f"HOME_{col}"] = home[col]
                    row[f"AWAY_{col}"] = away[col]
                row["SEASON"] = season
                # Dummy target (razlika poena)
                row["POINT_DIFF_TARGET"] = home["PTS"] - away["PTS"]
                games.append(row)

match_df = pd.DataFrame(games)
print("Broj generisanih parova:", len(match_df))
match_df.to_csv(output_path, index=False)
print(f"Spremljeno u {output_path}")
