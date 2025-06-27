import pandas as pd

# Putanje - promijeni ako treba
games_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_last5seasons.csv"
team_stats_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/team_stats_last5seasons.csv"
output_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_team_features.csv"

print("Učitavanje podataka...")

df_games = pd.read_csv(games_path)
df_team = pd.read_csv(team_stats_path)

print(f"Ukupno utakmica: {len(df_games)}")
print(f"Ukupno timskih zapisa: {len(df_team)}")

# Pripremi za spajanje - za home timove
home_stats = df_team.rename(columns=lambda x: "HOME_" + x if x not in ['TEAM_ID', 'SEASON'] else x)
# Filtriraj po timovima koji su u df_games kao HOME (TEAM1_ID)
home_stats = home_stats[home_stats['TEAM_ID'].isin(df_games['TEAM1_ID'])]

# Za away timove
away_stats = df_team.rename(columns=lambda x: "AWAY_" + x if x not in ['TEAM_ID', 'SEASON'] else x)
away_stats = away_stats[away_stats['TEAM_ID'].isin(df_games['TEAM2_ID'])]

# Spoji home stats u df_games
df_merged = pd.merge(df_games, home_stats, left_on=['TEAM1_ID', 'SEASON'], right_on=['TEAM_ID', 'SEASON'], how='left')
# Spoji away stats u df_games
df_merged = pd.merge(df_merged, away_stats, left_on=['TEAM2_ID', 'SEASON'], right_on=['TEAM_ID', 'SEASON'], how='left', suffixes=('_HOME', '_AWAY'))

# Očistimo duplikate kolona TEAM_ID koje su preostale iz merganja
df_merged.drop(columns=['TEAM_ID_HOME', 'TEAM_ID_AWAY'], inplace=True)

# Definiši target varijable
df_merged['HomeWin'] = (df_merged['HOME_PTS'] > df_merged['AWAY_PTS']).astype(int)
df_merged['PointDiff'] = df_merged['HOME_PTS'] - df_merged['AWAY_PTS']

# Pretvori GAME_DATE u datetime i izračunaj dan u sedmici
df_merged['GAME_DATE'] = pd.to_datetime(df_merged['GAME_DATE'])
df_merged['DAY_OF_WEEK'] = df_merged['GAME_DATE'].dt.dayofweek  # 0=Monday, 6=Sunday

# Spremi u CSV
df_merged.to_csv(output_path, index=False)
print(f"Dataset za utakmice s timskim statistikama spremljen u {output_path}")
