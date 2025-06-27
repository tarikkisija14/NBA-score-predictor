from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import time

# Definiši sezone koje želiš (zadnjih 5)
seasons = ['2019-20', '2020-21', '2021-22', '2022-23', '2023-24']

all_games = []

for season in seasons:
    print(f"Fetching games for season {season} ...")
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season, league_id_nullable='00')
    games_dict = gamefinder.get_normalized_dict()
    df_games = pd.DataFrame(games_dict['LeagueGameFinderResults'])

    # Čekanje između poziva da ne bi bio blokiran (po potrebi)
    time.sleep(1)

    # Izaberemo samo bitne kolone za identifikaciju utakmice i poene
    df_team_points = df_games[['GAME_ID', 'TEAM_ID', 'PTS', 'GAME_DATE']]

    # Grupiraj po utakmici i izvuci timove i poene
    game_ids = df_team_points['GAME_ID'].unique()

    for gid in game_ids:
        game_data = df_team_points[df_team_points['GAME_ID'] == gid]
        if len(game_data) == 2:
            # Za svaki game_id ima tačno 2 tima
            team1 = game_data.iloc[0]
            team2 = game_data.iloc[1]

            # Odredi home i away tim na osnovu GAME_DATE i ključa (NBA API ne daje direktno home/away, ali kod nas možeš detektovati ako MATCHUP info postoji, ovdje ne)
            # Ovdje samo prvo uzimamo kao home, drugo kao away (može se naknadno dopuniti)
            all_games.append({
                'GAME_ID': gid,
                'SEASON': season,
                'TEAM1_ID': team1['TEAM_ID'],
                'TEAM1_PTS': team1['PTS'],
                'TEAM2_ID': team2['TEAM_ID'],
                'TEAM2_PTS': team2['PTS'],
                'GAME_DATE': team1['GAME_DATE'],
            })

print(f"Total games fetched: {len(all_games)}")

df_all_games = pd.DataFrame(all_games)

# Sačuvaj CSV
output_path = "C:/Users/tarik/Desktop/nba score predictor/AI Model/data/games_last5seasons.csv"
df_all_games.to_csv(output_path, index=False)

print(f"Games dataset for last 5 seasons saved to {output_path}")
