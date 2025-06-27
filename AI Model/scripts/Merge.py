import pandas as pd

data_dir = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/"


games = pd.read_csv(data_dir + "games_processed.csv")
games_avg = pd.read_csv(data_dir + "games_with_averages.csv")
win_streak = pd.read_csv(data_dir + "games_with_win_streak.csv")
team_features = pd.read_csv(data_dir + "games_team_features.csv")
team_stats = pd.read_csv(data_dir + "team_stats_features.csv")

print("Games shape:", games.shape)
print("Games averages shape:", games_avg.shape)
print("Win streak shape:", win_streak.shape)
print("Team features shape:", team_features.shape)
print("Team stats shape:", team_stats.shape)


df = pd.merge(
    games,
    games_avg,
    how='left',
    left_on=['GAME_ID', 'TEAM1_ID'],
    right_on=['GAME_ID', 'TEAM1_ID'],
    suffixes=('', '_AVG')
)


win_streak_home = win_streak.rename(columns=lambda x: 'HOME_' + x if x not in ['GAME_ID', 'TEAM_ID'] else x)
df = pd.merge(
    df,
    win_streak_home,
    how='left',
    left_on=['GAME_ID', 'TEAM1_ID'],
    right_on=['GAME_ID', 'TEAM_ID']
)
df.drop(columns=['TEAM_ID'], inplace=True)


win_streak_away = win_streak.rename(columns=lambda x: 'AWAY_' + x if x not in ['GAME_ID', 'TEAM_ID'] else x)
df = pd.merge(
    df,
    win_streak_away,
    how='left',
    left_on=['GAME_ID', 'TEAM2_ID'],
    right_on=['GAME_ID', 'TEAM_ID']
)
df.drop(columns=['TEAM_ID'], inplace=True)


df = pd.merge(
    df,
    team_features,
    how='left',
    on=['GAME_ID', 'TEAM1_ID', 'TEAM2_ID', 'SEASON', 'GAME_DATE'],
    suffixes=('', '_TEAMFEAT')
)


team_stats_home = team_stats.rename(columns=lambda x: 'HOME_' + x if x not in ['GAME_ID', 'TEAM_ID'] else x)
df = pd.merge(
    df,
    team_stats_home,
    how='left',
    left_on=['GAME_ID', 'TEAM1_ID'],
    right_on=['GAME_ID', 'TEAM_ID']
)
df.drop(columns=['TEAM_ID'], inplace=True)


team_stats_away = team_stats.rename(columns=lambda x: 'AWAY_' + x if x not in ['GAME_ID', 'TEAM_ID'] else x)
df = pd.merge(
    df,
    team_stats_away,
    how='left',
    left_on=['GAME_ID', 'TEAM2_ID'],
    right_on=['GAME_ID', 'TEAM_ID']
)
df.drop(columns=['TEAM_ID'], inplace=True)

print("Final merged shape:", df.shape)
print("Primjer kolona u finalnom datasetu:")
print(df.columns.tolist())


df.to_csv(data_dir + "merged_full_dataset.csv", index=False)
print("✅ Merge završen. Dataset spremljen kao merged_full_dataset.csv")
