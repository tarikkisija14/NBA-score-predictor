import pandas as pd
import numpy as np

input_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_processed.csv"
output_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/team_stats_features.csv"

print("Učitavanje podataka...")
df = pd.read_csv(input_path, parse_dates=['GAME_DATE'])

# Priprema home i away podataka u jedan dataframe za analizu po timu
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

# Sortiraj po timu i datumu
team_games.sort_values(['TEAM_ID', 'GAME_DATE'], inplace=True)

# Win streak funkcija
def calc_win_streak(wins):
    streak = 0
    streaks = []
    for w in wins:
        if w == 1:
            streak += 1
        else:
            streak = 0
        streaks.append(streak)
    return streaks

team_games['WIN_STREAK'] = team_games.groupby('TEAM_ID')['WIN'].transform(calc_win_streak)

# Prosjek poena i primljenih poena u zadnjih 5 utakmica (rolling mean)
team_games['PTS_LAST_5'] = team_games.groupby('TEAM_ID')['PTS'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
team_games['OPP_PTS_LAST_5'] = team_games.groupby('TEAM_ID')['OPP_PTS'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

# Efikasnost napada (proxy) = poeni / broj poena protivnika (primjenjeno na 5 utakmica)
team_games['OFF_EFFICIENCY'] = team_games['PTS_LAST_5'] / team_games['OPP_PTS_LAST_5'].replace(0, np.nan)

# Net rating proxy = prosječni poeni - prosječni primljeni poeni
team_games['NET_RTG_PROXY'] = team_games['PTS_LAST_5'] - team_games['OPP_PTS_LAST_5']

# Usage rate proxy (poeni + poeni protivnika + broj utakmica)
# Ovo nije prava usage rate, ali daje neku indikaciju intenziteta igre
team_games['USAGE_PROXY'] = (team_games['PTS'] + team_games['OPP_PTS']) / 48  # 48 minuta po utakmici

# Dodaj omjere za pobjede i poraze u zadnjih 5 utakmica
team_games['WIN_PCT_LAST_5'] = team_games.groupby('TEAM_ID')['WIN'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

# Popuni NaN sa 0 tamo gdje ima
team_games.fillna(0, inplace=True)

# Na kraju spremi u CSV
team_games.to_csv(output_path, index=False)

print(f"✅ Timske napredne statistike spremljene u {output_path}")
