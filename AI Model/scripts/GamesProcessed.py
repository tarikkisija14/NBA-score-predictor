import pandas as pd

input_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_last5seasons.csv"
output_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_processed.csv"

print("Učitavanje raw podataka o utakmicama...")
df = pd.read_csv(input_path)

# Pretpostavimo da imaš kolone:
# 'GAME_ID', 'GAME_DATE', 'TEAM1_ID', 'TEAM1_PTS', 'TEAM2_ID', 'TEAM2_PTS', 'HOME_TEAM_NAME', 'AWAY_TEAM_NAME', itd.

print("Kreiranje target kolona...")

df['HomeWin'] = (df['TEAM1_PTS'] > df['TEAM2_PTS']).astype(int)
df['PointDiff'] = df['TEAM1_PTS'] - df['TEAM2_PTS']

df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
df['DAY_OF_WEEK'] = df['GAME_DATE'].dt.dayofweek  # 0=ponedeljak ... 6=nedelja

# Dodaj ostale korisne feature ako imaš

print("Spremanje pripremljenog dataset-a...")
df.to_csv(output_path, index=False)

print(f"games_processed.csv spremljen u: {output_path}")
