import pandas as pd

input_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_processed.csv"
output_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_with_win_streak.csv"

print("Učitavanje podataka...")
df = pd.read_csv(input_path, parse_dates=['GAME_DATE'])


home_df = df[['GAME_ID', 'GAME_DATE', 'TEAM1_ID', 'TEAM1_PTS', 'TEAM2_PTS']].copy()
home_df.rename(columns={
    'TEAM1_ID': 'TEAM_ID',
    'TEAM1_PTS': 'PTS',
    'TEAM2_PTS': 'OPP_PTS'
}, inplace=True)
home_df['IS_HOME'] = 1
home_df['WIN'] = (home_df['PTS'] > home_df['OPP_PTS']).astype(int)


away_df = df[['GAME_ID', 'GAME_DATE', 'TEAM2_ID', 'TEAM2_PTS', 'TEAM1_PTS']].copy()
away_df.rename(columns={
    'TEAM2_ID': 'TEAM_ID',
    'TEAM2_PTS': 'PTS',
    'TEAM1_PTS': 'OPP_PTS'
}, inplace=True)
away_df['IS_HOME'] = 0
away_df['WIN'] = (away_df['PTS'] > away_df['OPP_PTS']).astype(int)


team_games = pd.concat([home_df, away_df], ignore_index=True)


team_games = team_games.sort_values(['TEAM_ID', 'GAME_DATE'])


team_games['WIN_STREAK'] = 0
def calc_streak(wins):
    streak = 0
    streaks = []
    for w in wins:
        if w == 1:
            streak += 1
        else:
            streak = 0
        streaks.append(streak)
    return streaks

team_games['WIN_STREAK'] = team_games.groupby('TEAM_ID')['WIN'].transform(calc_streak)


team_games.to_csv(output_path, index=False)
print(f"Win streak podaci spremljeni u {output_path}")
