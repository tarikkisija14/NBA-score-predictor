from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import os

def fetch_multiple_seasons(seasons: list, filepath: str):
    all_matchups = []

    for season in seasons:
        print(f"\n Sezona: {season}")
        gf = leaguegamefinder.LeagueGameFinder(
            season_nullable=season,
            season_type_nullable='Regular Season'
        )
        games = gf.get_data_frames()[0]
        games = games.dropna(subset=['GAME_ID'])


        games = games.sort_values(['GAME_DATE', 'GAME_ID'])


        FORM_WINDOW = 10
        form_tracker: dict[str, list[int]] = {}


        team_game_rows = []
        for _, row in games.iterrows():
            tid = row['TEAM_ID']
            if tid not in form_tracker:
                form_tracker[tid] = []
            prev = form_tracker[tid][-FORM_WINDOW:]
            form = round(sum(prev) / len(prev), 4) if prev else 0.5
            team_game_rows.append({
                'GAME_ID': row['GAME_ID'],
                'TEAM_ID': tid,
                'FORM': form
            })
            form_tracker[tid].append(1 if row['WL'] == 'W' else 0)

        form_df = pd.DataFrame(team_game_rows)

        grouped = games.groupby('GAME_ID')

        for game_id, group in grouped:
            if len(group) != 2:
                continue

            team1 = group.iloc[0]
            team2 = group.iloc[1]

            def get_form(team_id, gid):
                r = form_df[(form_df['GAME_ID'] == gid) & (form_df['TEAM_ID'] == team_id)]
                return float(r['FORM'].values[0]) if not r.empty else 0.5

            row = {
                'SEASON':         season,
                'GAME_ID':        game_id,
                'GAME_DATE':      team1['GAME_DATE'],


                'TEAM1_NAME':     team1['TEAM_NAME'],
                'TEAM2_NAME':     team2['TEAM_NAME'],


                'TEAM1_PTS':      team1['PTS'],
                'TEAM2_PTS':      team2['PTS'],


                'TEAM1_AST':      team1['AST'],
                'TEAM2_AST':      team2['AST'],
                'TEAM1_REB':      team1['REB'],
                'TEAM2_REB':      team2['REB'],
                'TEAM1_FG_PCT':   team1['FG_PCT'],
                'TEAM2_FG_PCT':   team2['FG_PCT'],
                'TEAM1_FT_PCT':   team1['FT_PCT'],
                'TEAM2_FT_PCT':   team2['FT_PCT'],
                'TEAM1_PLUS_MINUS': team1['PLUS_MINUS'],
                'TEAM2_PLUS_MINUS': team2['PLUS_MINUS'],


                'TEAM1_FG3_PCT':  team1.get('FG3_PCT', None),
                'TEAM2_FG3_PCT':  team2.get('FG3_PCT', None),
                'TEAM1_TOV':      team1.get('TOV', None),
                'TEAM2_TOV':      team2.get('TOV', None),
                'TEAM1_STL':      team1.get('STL', None),
                'TEAM2_STL':      team2.get('STL', None),
                'TEAM1_BLK':      team1.get('BLK', None),
                'TEAM2_BLK':      team2.get('BLK', None),


                'TEAM1_FORM':     get_form(team1['TEAM_ID'], game_id),
                'TEAM2_FORM':     get_form(team2['TEAM_ID'], game_id),

                'TEAM1_WIN':      1 if team1['WL'] == 'W' else 0
            }

            all_matchups.append(row)

    df_all = pd.DataFrame(all_matchups)


    for col in ['TEAM1_FG3_PCT', 'TEAM2_FG3_PCT', 'TEAM1_TOV', 'TEAM2_TOV',
                'TEAM1_STL', 'TEAM2_STL', 'TEAM1_BLK', 'TEAM2_BLK']:
        if col in df_all.columns:
            df_all[col] = df_all[col].fillna(df_all[col].median())

    df_all.to_csv(filepath, index=False)
    print(f"\n Ukupno sejvano {len(df_all)} utakmica u: {filepath}")
    print(f" Kolone: {list(df_all.columns)}")


if __name__ == "__main__":
    seasons = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25']


    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, '..', 'data', 'ALL_NBA_matchups_2020_2025.csv')

    fetch_multiple_seasons(seasons, filepath)