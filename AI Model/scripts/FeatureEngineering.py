import pandas as pd
import numpy as np

input_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_typed.csv"
output_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/player_stats_features.csv"

df = pd.read_csv(input_path)

print("Broj redova prije obrade:", len(df))


df["PTS_PER_GAME"] = df["PTS"] / df["GP"]
df["REB_PER_GAME"] = df["REB"] / df["GP"]
df["AST_PER_GAME"] = df["AST"] / df["GP"]
df["STL_PER_GAME"] = df["STL"] / df["GP"]
df["BLK_PER_GAME"] = df["BLK"] / df["GP"]
df["TOV_PER_GAME"] = df["TOV"] / df["GP"]

df["PTS_PER_MIN"] = df["PTS"] / df["MIN"]
df["REB_PER_MIN"] = df["REB"] / df["MIN"]
df["AST_PER_MIN"] = df["AST"] / df["MIN"]
df["STL_PER_MIN"] = df["STL"] / df["MIN"]
df["BLK_PER_MIN"] = df["BLK"] / df["MIN"]
df["TOV_PER_MIN"] = df["TOV"] / df["MIN"]

df["PTS_PER_36"] = df["PTS"] * (36 / df["MIN"])


df["FG_EFFICIENCY"] = df["FGM"] / df["FGA"].replace(0, np.nan)
df["FG3_EFFICIENCY"] = df["FG3M"] / df["FG3A"].replace(0, np.nan)
df["FT_EFFICIENCY"] = df["FTM"] / df["FTA"].replace(0, np.nan)


df["TS_PCT"] = df["PTS"] / (2 * (df["FGA"] + 0.44 * df["FTA"])).replace(0, np.nan)


df["EFG_PCT"] = (df["FGM"] + 0.5 * df["FG3M"]) / df["FGA"].replace(0, np.nan)


df["AST_TO_TOV_RATIO"] = df["AST"] / df["TOV"].replace(0, np.nan)


df["USG_RATE_PROXY"] = (df["FGA"] + 0.44 * df["FTA"] + df["TOV"]) / df["MIN"]


df["OFF_RTG_PROXY"] = df["PTS"] / df["FGA"].replace(0, np.nan)


df["DEF_RTG_PROXY"] = (df["STL"] + df["BLK"]) / df["MIN"]


df["NET_RTG_PROXY"] = df["OFF_RTG_PROXY"] - df["DEF_RTG_PROXY"]


df["PER_PROXY"] = (
    (df["PTS"] + df["REB"] + df["AST"] + df["STL"] + df["BLK"])
    - (df["FGA"] - df["FGM"])
    - (df["FTA"] - df["FTM"])
    - df["TOV"]
) / df["MIN"]


metrics = ["PTS", "REB", "AST", "STL", "BLK", "TOV"]
for metric in metrics:
    df[metric + "_PERCENTILE"] = df[metric].rank(pct=True)


df["HAS_DD2"] = (df["DD2"] > 0).astype(int)
df["HAS_TD3"] = (df["TD3"] > 0).astype(int)


df["DEF_IMPACT"] = df["STL"] + df["BLK"]


df["OFF_CONTRIBUTION"] = df["PTS"] + df["AST"]


df["PFD_TO_PF_RATIO"] = df["PFD"] / df["PF"].replace(0, np.nan)


df = df.fillna(0)


print("Broj redova nakon obrade:", len(df))
print("Sve nove kolone:")
print([c for c in df.columns if c not in ["PLAYER_ID","PLAYER_NAME","NICKNAME","TEAM_ID","TEAM_ABBREVIATION","SEASON"]])

df.to_csv(output_path, index=False)
print(f"\n✅ OGROMNA Feature Engineering skripta završena.\nDataset spremljen u {output_path}")
