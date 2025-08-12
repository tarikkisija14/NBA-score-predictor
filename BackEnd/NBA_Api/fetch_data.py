import sys
import json
from nba_api.stats.endpoints import leaguestandingsv3, leagueleaders, teamdashboardbygeneralsplits
from nba_api.stats.static import teams
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

CACHE_DURATION = 60 * 60

CACHE_FILES = {
    "standings": "cache_standings.json",
    "league_leaders": "cache_league_leaders.json",
    "team_leaders": "cache_team_leaders.json"
}

def get_standings():
    cache_file = CACHE_FILES["standings"]

    cached = read_cache(cache_file)
    if cached:
        return cached

    try:
        standings = leaguestandingsv3.LeagueStandingsV3().get_dict()
        east = []
        west = []

        for team in standings['resultSets'][0]['rowSet']:
            team_data = {
                "team": team[4],
                "wins": team[13],
                "losses": team[14],
                "pct": team[15],
                "gb": team[18],
                "home": team[21],
                "away": team[22],
                "div": team[23],
                "conf": team[24]
            }
            if team[5] == "East":
                east.append(team_data)
            else:
                west.append(team_data)

        result = {"east": east, "west": west}
        write_cache(cache_file, result)
        return result
    except Exception as e:
        return cached if cached else {"error": str(e)}


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
        "FG_PCT": "Field Goal Percentage"
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
        "PTS": 22,
        "REB": 18,
        "AST": 19,
        "STL": 20,
        "BLK": 21,
        "FG_PCT": 8
    }
    return mapping[stat]

def fetch_team_stat(team_info, category):

    try:
        stats = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
            team_id=team_info["id"], per_mode_detailed="PerGame"
        ).get_dict()
        row = stats['resultSets'][0]['rowSet'][0]
        return {
            "team": team_info["full_name"],
            "value": row[stat_index_team(category)]
        }
    except Exception as e:
        return {"team": team_info["full_name"], "error": str(e)}



def get_team_leaders():
    cache_file = CACHE_FILES["team_leaders"]

    cached = read_cache(cache_file)
    if cached:
        return cached

    categories = {
        "PTS": "Points Per Game",
        "REB": "Total Rebounds Per Game",
        "AST": "Assists Per Game",
        "STL": "Steals Per Game",
        "BLK": "Blocks Per Game",
        "FG_PCT": "Field Goal Percentage"
    }

    all_teams = teams.get_teams()
    team_stats = {}

    try:
        for category in categories:
            leaders_list = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(fetch_team_stat, team_info, category) for team_info in all_teams]
                for future in as_completed(futures):
                    leaders_list.append(future.result())

            leaders_list = [t for t in leaders_list if "error" not in t]  # makni errore iz liste
            leaders_list.sort(key=lambda x: x["value"], reverse=True)
            team_stats[category] = leaders_list[:5]

        write_cache(cache_file, team_stats)
        return team_stats
    except Exception as e:
        return cached if cached else {"error": str(e)}

def stat_index_team(stat):
    mapping = {
        "PTS": 26,
        "REB": 20,
        "AST": 21,
        "STL": 22,
        "BLK": 23,
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







