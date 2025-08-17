import sys
import json
from nba_api.stats.endpoints import leaguestandingsv3, leagueleaders, teamdashboardbygeneralsplits
from nba_api.stats.static import teams
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from nba_api.stats.endpoints import leaguedashteamstats


from requests import RequestException

CACHE_DURATION = 60 * 60

CACHE_FILES = {
    "standings": "cache_standings.json",
    "league_leaders": "cache_league_leaders.json",
    "team_leaders": "cache_team_leaders.json"
}


DEFAULT_LOGO = "https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg"

all_teams = teams.get_teams()
nickname_to_id = {team["nickname"]: team["id"] for team in all_teams}



def get_standings():
    data = leaguestandingsv3.LeagueStandingsV3().get_dict()
    rows = data['resultSets'][0]['rowSet']


    east = []
    west = []

    for team in rows:
        team_name = team[4]
        team_id = nickname_to_id.get(team_name)
        logo_url = f"https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg" if team_id else DEFAULT_LOGO


        team_info = {
            "logo": logo_url,
            "team": team[4],
            "wins": team[13],
            "losses": team[14],
            "pct": team[15],
            "gb":team[38],
            "home": team[18],
            "away": team[19],
            "div": team[23],
            "conf": team[24]
        }
        if team[6] == "East":
            east.append(team_info)
        elif team[6] == "West":
            west.append(team_info)

    return {"east": east, "west": west}







def fetch_league_category(stat):
    try:

        leaders = leagueleaders.LeagueLeaders(
            stat_category_abbreviation=stat,
            per_mode48="PerGame",
            season="2024-25",
            season_type_all_star="Regular Season"
        ).get_dict()

        data_set = None
        if "resultSet" in leaders:
            data_set = leaders["resultSet"]
        elif "resultSets" in leaders:
            data_set = leaders["resultSets"][0]

        if not data_set or "rowSet" not in data_set or not data_set["rowSet"]:
            return stat, [{"error": f"No data returned for {stat}"}]

        players = []
        for row in data_set["rowSet"][:5]:
            players.append({
                "player": row[2],
                "team": row[4],
                "value": row[stat_index(stat)]
            })
        return stat, players

    except Exception as e:
        return stat, [{"error": str(e)}]







def get_league_leaders():
    cache_file = CACHE_FILES["league_leaders"]

    cached = read_cache(cache_file)
    if cached:
        return cached


    categories = {
        "PTS": "Points Per Game",
        "REB": "Total Rebounds Per Game",
        "AST": "Assists Per Game",
        "STL": "Steals Per Game",
        "BLK": "Blocks Per Game",
        "MIN": "Minutes Per Game"
    }

    results = {}
    try:
        with ThreadPoolExecutor(max_workers=len(categories)) as executor:
            futures = [executor.submit(fetch_league_category, stat) for stat in categories]
            for future in as_completed(futures):
                stat, players = future.result()
                results[stat] = players

        write_cache(cache_file, results)
        return results
    except Exception as e:
        return cached if cached else {"error": str(e)}



def stat_index(stat):
    mapping = {
        "PTS": 24,
        "REB": 18,
        "AST": 19,
        "STL": 20,
        "BLK": 21,
        "MIN": 6
    }
    return mapping[stat]

import time
from requests.exceptions import RequestException

def fetch_team_stat(team_info, category, retries=3, delay=1):
    for attempt in range(retries):
        try:
            stats = leaguedashteamstats.LeagueDashTeamStats(
                season="2024-25",
                season_type_all_star="Regular Season",
                team_id_nullable=team_info["id"],
                per_mode_detailed="PerGame",
                timeout=30
            ).get_dict()

            row = stats['resultSets'][0]['rowSet'][0]
            return {
                "team": team_info["full_name"],
                "value": row[stat_index_team(category)]
            }
        except RequestException as e:
            if attempt == retries - 1:
                return {"team": team_info["full_name"], "error": str(e)}
            time.sleep(delay * (attempt + 1))
        except Exception as e:
            return {"team": team_info["full_name"], "error": str(e)}
    return {"team": team_info["full_name"], "error": "Max retries exceeded"}


def get_team_leaders():
    cache_file = CACHE_FILES["team_leaders"]
    all_nba_teams = [team for team in teams.get_teams()
                     if not any(x in team['full_name']
                                for x in ['Stars', 'Magic', 'Hustle', 'Go-Go', 'Skyhawks'])]
    team_id_map = {str(team['id']): team['full_name'] for team in all_nba_teams}


    try:
        cached = read_cache(cache_file)
        if cached and any(len(v) > 0 for v in cached.values()):

            if all(not any(x in item['team']
                           for x in ['Stars', 'Magic', 'Hustle'])
                   for cat in cached.values() for item in cat):
                return cached
    except:
        pass

    try:

        response = leaguedashteamstats.LeagueDashTeamStats(
            season="2024-25",
            season_type_all_star="Regular Season",
            per_mode_detailed="PerGame",
            league_id_nullable='00'
        ).get_dict()


        results = {}
        headers = response['resultSets'][0]['headers']
        rows = [row for row in response['resultSets'][0]['rowSet']
                if str(row[headers.index('TEAM_ID')]) in team_id_map]

        stat_indices = {stat: headers.index(stat) for stat in ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT']}

        for stat in stat_indices:
            results[stat] = []

        for row in rows:
            team_id = str(row[headers.index('TEAM_ID')])
            team_name = team_id_map[team_id]  # We already filtered

            for stat, index in stat_indices.items():
                results[stat].append({
                    "team": team_name,
                    "value": row[index]
                })


        final_results = {}
        for stat in results:
            final_results[stat] = sorted(results[stat],
                                         key=lambda x: x["value"],
                                         reverse=True)[:5]

        write_cache(cache_file, final_results)
        return final_results

    except Exception as e:
        print(f"Error: {str(e)}")
        return {stat: [] for stat in ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT']}

def stat_index_team(stat):
    mapping = {
        "PTS": 26,
        "REB": 18,
        "AST": 19,
        "STL": 21,
        "BLK": 22,
        "FG_PCT": 9
    }
    return mapping[stat]


def read_cache(file_path):
    if os.path.exists(file_path) and (time.time() - os.path.getmtime(file_path) < CACHE_DURATION):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None


def write_cache(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except:
        pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No argument provided"}))
        sys.exit(1)

    option = sys.argv[1]

    if option == "standings":
        print(json.dumps(get_standings(), indent=2))
    elif option == "league_leaders":
        print(json.dumps(get_league_leaders(), indent=2))
    elif option == "team_leaders":
        print(json.dumps(get_team_leaders(), indent=2))
    else:
        print(json.dumps({"error": "Invalid option"}))







