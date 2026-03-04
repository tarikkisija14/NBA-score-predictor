import sys
import json
from nba_api.stats.endpoints import leaguestandingsv3, leagueleaders
from nba_api.stats.static import teams
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from nba_api.stats.endpoints import leaguedashteamstats
from requests.exceptions import RequestException


CACHE_DURATION = 60 * 60  # 1 hour in seconds

CACHE_FILES = {
    "standings": "cache_standings.json",
    "league_leaders": "cache_league_leaders.json",
    "team_leaders": "cache_team_leaders.json"
}

DEFAULT_LOGO = "https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg"

all_teams = teams.get_teams()
nickname_to_id = {team["nickname"]: team["id"] for team in all_teams}


def get_current_nba_season() -> str:
    """
    Returns the current NBA season string (e.g. '2025-26').
    The NBA season starts in October — before October we are still in
    the previous season's playoffs/offseason, so we step back one year.
    """
    import datetime
    now = datetime.datetime.now()
    start_year = now.year if now.month >= 10 else now.year - 1
    end_year = str(start_year + 1)[-2:]
    return f"{start_year}-{end_year}"


CURRENT_SEASON = get_current_nba_season()


# ── STANDINGS ────────────────────────────────────────────────────────────────

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
            "gb": team[38],
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


# ── LEAGUE LEADERS ───────────────────────────────────────────────────────────

def stat_index(stat):
    return {"PTS": 24, "REB": 18, "AST": 19, "STL": 20, "BLK": 21, "MIN": 6}[stat]


def fetch_league_category(stat):
    try:
        leaders = leagueleaders.LeagueLeaders(
            stat_category_abbreviation=stat,
            per_mode48="PerGame",
            season=CURRENT_SEASON,
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

    categories = ["PTS", "REB", "AST", "STL", "BLK", "MIN"]
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
        return {"error": str(e)}


# ── TEAM LEADERS ─────────────────────────────────────────────────────────────

def stat_index_team(stat):
    return {"PTS": 26, "REB": 18, "AST": 19, "STL": 21, "BLK": 22, "FG_PCT": 9}[stat]


def get_team_leaders():
    cache_file = CACHE_FILES["team_leaders"]
    cached = read_cache(cache_file)
    if cached:
        return cached

    all_nba_teams = [
        team for team in teams.get_teams()
        if not any(x in team['full_name'] for x in ['Stars', 'Magic', 'Hustle', 'Go-Go', 'Skyhawks'])
    ]
    team_id_map = {str(team['id']): team['full_name'] for team in all_nba_teams}

    try:
        response = leaguedashteamstats.LeagueDashTeamStats(
            season=CURRENT_SEASON,
            season_type_all_star="Regular Season",
            per_mode_detailed="PerGame",
            league_id_nullable='00'
        ).get_dict()

        headers = response['resultSets'][0]['headers']
        rows = [
            row for row in response['resultSets'][0]['rowSet']
            if str(row[headers.index('TEAM_ID')]) in team_id_map
        ]

        stat_indices = {stat: headers.index(stat) for stat in ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT']}
        results = {stat: [] for stat in stat_indices}

        for row in rows:
            team_id = str(row[headers.index('TEAM_ID')])
            team_name = team_id_map[team_id]
            for stat, idx in stat_indices.items():
                results[stat].append({"team": team_name, "value": row[idx]})

        final_results = {
            stat: sorted(results[stat], key=lambda x: x["value"], reverse=True)[:5]
            for stat in results
        }

        write_cache(cache_file, final_results)
        return final_results

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return {stat: [] for stat in ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT']}


# ── CACHE HELPERS ────────────────────────────────────────────────────────────

def read_cache(file_path):
    """
    Read cache only if valid. Uses a '_cached_at' timestamp INSIDE the JSON
    (not file mtime) so cache works correctly after deploy, unzip, or copy.
    """
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            os.remove(file_path)
            return None

        data = json.loads(content)
        cached_at = data.pop("_cached_at", None)

        # No timestamp = old-format cache (e.g. committed to repo) — treat as expired
        if cached_at is None or (time.time() - cached_at) >= CACHE_DURATION:
            try:
                os.remove(file_path)
            except OSError:
                pass
            return None

        return data

    except (json.JSONDecodeError, OSError):
        # Corrupt or unreadable — delete so next request fetches fresh data
        try:
            os.remove(file_path)
        except OSError:
            pass
        return None


def write_cache(file_path, data):
    try:
        payload = {"_cached_at": time.time(), **data}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except OSError:
        pass


# ── ENTRY POINT ──────────────────────────────────────────────────────────────


# ── LIVE / TODAY SCORES ───────────────────────────────────────────────────────

def get_scores():
    """
    Fetches today's NBA scoreboard using the stable stats API (Scoreboard endpoint).
    Cache is kept short (60 seconds) so live games update frequently.
    """
    import datetime
    cache_file = "cache_scores.json"
    SCORES_CACHE = 60  # 1 minute for live data

    if os.path.exists(cache_file) and (time.time() - os.path.getmtime(cache_file) < SCORES_CACHE):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_content = f.read().strip()
                if cached_content:
                    return json.loads(cached_content)
        except (json.JSONDecodeError, OSError):
            try:
                os.remove(cache_file)
            except OSError:
                pass

    try:
        from nba_api.stats.endpoints import scoreboardv2

        today = datetime.date.today().strftime("%m/%d/%Y")
        board = scoreboardv2.ScoreboardV2(game_date=today, league_id="00")
        board_dict = board.get_dict()

        # resultSets[0] = GameHeader, resultSets[1] = LineScore
        result_sets = {rs["name"]: rs for rs in board_dict["resultSets"]}

        game_header = result_sets.get("GameHeader", {})
        line_score  = result_sets.get("LineScore", {})

        gh_headers = game_header.get("headers", [])
        gh_rows    = game_header.get("rowSet", [])
        ls_headers = line_score.get("headers", [])
        ls_rows    = line_score.get("rowSet", [])

        def idx(headers, name):
            try:
                return headers.index(name)
            except ValueError:
                return None

        # Index helpers for GameHeader
        gh_game_id   = idx(gh_headers, "GAME_ID")
        gh_status    = idx(gh_headers, "GAME_STATUS_TEXT")
        gh_period    = idx(gh_headers, "LIVE_PERIOD")
        gh_home_id   = idx(gh_headers, "HOME_TEAM_ID")
        gh_visitor_id= idx(gh_headers, "VISITOR_TEAM_ID")

        # Index helpers for LineScore
        ls_game_id   = idx(ls_headers, "GAME_ID")
        ls_team_id   = idx(ls_headers, "TEAM_ID")
        ls_tricode   = idx(ls_headers, "TEAM_ABBREVIATION")
        ls_team_name = idx(ls_headers, "TEAM_CITY_NAME")
        ls_pts       = idx(ls_headers, "PTS")

        # Build a lookup: game_id -> {team_id -> line_score row}
        score_lookup = {}
        for row in ls_rows:
            gid = row[ls_game_id]
            tid = str(row[ls_team_id])
            score_lookup.setdefault(gid, {})[tid] = row

        # Build team_id -> full_name lookup from static teams
        all_nba = teams.get_teams()
        id_to_name = {str(t["id"]): t["full_name"] for t in all_nba}

        games = []
        for row in gh_rows:
            game_id   = row[gh_game_id]
            status    = row[gh_status].strip() if gh_status is not None else ""
            period    = row[gh_period] if gh_period is not None else 0
            home_tid  = str(row[gh_home_id])  if gh_home_id   is not None else ""
            away_tid  = str(row[gh_visitor_id]) if gh_visitor_id is not None else ""

            game_scores = score_lookup.get(game_id, {})
            home_row    = game_scores.get(home_tid, [])
            away_row    = game_scores.get(away_tid, [])

            def safe(r, i):
                try:
                    return r[i] if i is not None and r else 0
                except (IndexError, TypeError):
                    return 0

            home_pts     = safe(home_row, ls_pts) or 0
            away_pts     = safe(away_row, ls_pts) or 0
            home_tri     = safe(home_row, ls_tricode) or ""
            away_tri     = safe(away_row, ls_tricode) or ""
            home_city    = safe(home_row, ls_team_name) or id_to_name.get(home_tid, "")
            away_city    = safe(away_row, ls_team_name) or id_to_name.get(away_tid, "")

            games.append({
                "game_id":      game_id,
                "status":       status,
                "period":       period,
                "home_team":    home_city,
                "home_tricode": home_tri,
                "home_score":   home_pts,
                "home_logo":    f"https://cdn.nba.com/logos/nba/{home_tid}/primary/L/logo.svg",
                "away_team":    away_city,
                "away_tricode": away_tri,
                "away_score":   away_pts,
                "away_logo":    f"https://cdn.nba.com/logos/nba/{away_tid}/primary/L/logo.svg",
            })

        result = {"games": games, "count": len(games)}
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(result, f)
        except OSError:
            pass
        return result

    except Exception as e:
        return {"games": [], "count": 0, "error": str(e)}

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
    elif option == "scores":
        print(json.dumps(get_scores(), indent=2))
    else:
        print(json.dumps({"error": "Invalid option"}))