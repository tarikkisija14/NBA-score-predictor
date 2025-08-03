from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

def fetch_multiple_seasons(seasons: list, filepath: str):
    all_matchups = []

    for season in seasons:
        print(f"\n Sezone: {season}")
        gf = leaguegamefinder.LeagueGameFinder(
            season_nullable=season,
            season_type_nullable='Regular Season'
        )
        games = gf.get_data_frames()[0]
        games = games.dropna(subset=['GAME_ID'])
        grouped = games.groupby('GAME_ID')

        for game_id, group in grouped:
            if len(group) != 2:
                continue

            team1 = group.iloc[0]
            team2 = group.iloc[1]

            row = {
                'SEASON': season,
                'GAME_ID': game_id,
                'TEAM1_NAME': team1['TEAM_NAME'],
                'TEAM2_NAME': team2['TEAM_NAME'],
                'TEAM1_PTS': team1['PTS'],
                'TEAM2_PTS': team2['PTS'],
                'TEAM1_AST': team1['AST'],
                'TEAM2_AST': team2['AST'],
                'TEAM1_REB': team1['REB'],
                'TEAM2_REB': team2['REB'],
                'TEAM1_FG_PCT': team1['FG_PCT'],
                'TEAM2_FG_PCT': team2['FG_PCT'],
                'TEAM1_FT_PCT': team1['FT_PCT'],
                'TEAM2_FT_PCT': team2['FT_PCT'],
                'TEAM1_PLUS_MINUS': team1['PLUS_MINUS'],
                'TEAM2_PLUS_MINUS': team2['PLUS_MINUS'],
                'TEAM1_WIN': 1 if team1['WL'] == 'W' else 0
            }

            all_matchups.append(row)


    df_all = pd.DataFrame(all_matchups)
    df_all.to_csv(filepath, index=False)
    print(f"\n Ukupno sejvano {len(df_all)} utakmica u: {filepath}")

if __name__ == "__main__":
    seasons = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
    filepath = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025.csv"
    fetch_multiple_seasons(seasons, filepath)



