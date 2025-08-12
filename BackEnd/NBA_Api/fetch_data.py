import sys
import json
from nba_api.stats.endpoints import leaguestandingsv3, leagueleaders, teamdashboardbygeneralsplits
from nba_api.stats.static import teams

def get_standings():
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
    if team[5]=="East":
        east.append(team_data)
    else:
        west.append(team_data)
    return {"east": east, "west": west}


def get_league_leaders():
    categories = {
        "PTS": "Points Per Game",
        "REB": "Total Rebounds Per Game",
        "AST": "Assists Per Game",
        "STL": "Steals Per Game",
        "BLK": "Blocks Per Game",
        "FG_PCT": "Field Goal Percentage"
    }
    results = {}

    for stat, name in categories.items():
        leaders = leagueleaders.LeagueLeaders(stat_category_abbreviation=stat, per_mode48="PerGame").get_dict()
        players = []
        for row in leaders['resultSet']['rowSet'][:5]:
            players.append({
                "player": row[2],
                "team": row[4],
                "value": row[stat_index(stat)]
            })
        results[stat] = players

    return results

def stat_index(stat):
    mapping={
        "PTS": 22,
        "REB": 18,
        "AST": 19,
        "STL": 20,
        "BLK": 21,
        "FG_PCT": 8
    }
    return mapping[stat]


def get_team_leaders():
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

    for category in categories:
        leaders_list = []
        for team_info in all_teams:
            stats = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
                team_id=team_info["id"], per_mode_detailed="PerGame"
            ).get_dict()
            row = stats['resultSets'][0]['rowSet'][0]
            leaders_list.append({
                "team": team_info["full_name"],
                "value": row[stat_index_team(category)]
            })
        leaders_list.sort(key=lambda x: x["value"], reverse=True)
        team_stats[category] = leaders_list[:5]

    return team_stats

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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No argument provided"}))
        sys.exit(1)

    option = sys.argv[1]

    if option == "standings":
        print(json.dumps(get_standings()))
    elif option == "league_leaders":
        print(json.dumps(get_league_leaders()))
    elif option == "team_leaders":
        print(json.dumps(get_team_leaders()))
    else:
        print(json.dumps({"error": "Invalid option"}))


