import pandas as pd

input_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_last5seasons.csv"
output_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_with_averages.csv"

print("Učitavanje podataka...")
df = pd.read_csv(input_path, parse_dates=['GAME_DATE'])


df = df.sort_values('GAME_DATE')


def rolling_avg_points(df, team_col, pts_col):
   
    rolling_averages = pd.DataFrame()


    for team_id in df[team_col].unique():
        team_games = df[df[team_col] == team_id].copy()
        team_games['AVG_PTS_LAST_5'] = team_games[pts_col].shift(1).rolling(window=5, min_periods=1).mean()
        rolling_averages = pd.concat([rolling_averages, team_games])

    return rolling_averages

print("Računanje proseka poena za timove 1 (TEAM1)...")
df_team1 = rolling_avg_points(df, 'TEAM1_ID', 'TEAM1_PTS')

print("Računanje proseka poena za timove 2 (TEAM2)...")
df_team2 = rolling_avg_points(df, 'TEAM2_ID', 'TEAM2_PTS')


df_avg = pd.merge(df_team1[['GAME_ID', 'TEAM1_ID', 'AVG_PTS_LAST_5']],
                  df_team2[['GAME_ID', 'TEAM2_ID', 'AVG_PTS_LAST_5']],
                  on='GAME_ID',
                  suffixes=('_TEAM1', '_TEAM2'))


df = df.merge(df_avg[['GAME_ID', 'AVG_PTS_LAST_5_TEAM1', 'AVG_PTS_LAST_5_TEAM2']], on='GAME_ID')

df.to_csv(output_path, index=False)
print(f"Proseci poena spremljeni u {output_path}")
