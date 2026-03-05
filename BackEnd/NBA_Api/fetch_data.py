"""
fetch_data.py  —  NBA Stats fetcher za ASP.NET backend
-------------------------------------------------------
Poboljšanja:
  • Retry logika za NBA API timeouts i rate limit (429)
  • Graceful fallback: vraća cached podatke ako NBA API nije dostupan
  • Bolji error poruke (razlikuje timeout vs rate-limit vs API error)
  • Scores cache ostaje kratak (60s) jer su podaci živi
"""

import sys
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from nba_api.stats.endpoints import (
    leaguestandingsv3, leagueleaders,
    leaguedashteamstats, scoreboardv2
)
from nba_api.stats.static import teams




CACHE_DURATION  = 60 * 60   # 1 hour (standings, leaders)
SCORES_CACHE    = 60        # 60 seconds (live scores)
REQUEST_TIMEOUT = 30        # seconds per NBA API call
MAX_RETRIES     = 3
RETRY_DELAY     = 3         # seconds between retries

CACHE_FILES = {
    "standings":     "cache_standings.json",
    "league_leaders":"cache_league_leaders.json",
    "team_leaders":  "cache_team_leaders.json",
    "scores":        "cache_scores.json",
}

DEFAULT_LOGO = "https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg"

all_teams       = teams.get_teams()
nickname_to_id  = {t["nickname"]: t["id"] for t in all_teams}


# ── SEASON HELPER ─────────────────────────────────────────────────────────────

def get_current_nba_season() -> str:
    import datetime
    now = datetime.datetime.now()
    start_year = now.year if now.month >= 10 else now.year - 1
    end_year   = str(start_year + 1)[-2:]
    return f"{start_year}-{end_year}"


CURRENT_SEASON = get_current_nba_season()


# ── CACHE HELPERS ─────────────────────────────────────────────────────────────

def read_cache(file_path: str, max_age: int = CACHE_DURATION):
    """Read cache if fresh. Returns data dict or None."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return None
        data = json.loads(content)
        cached_at = data.pop("_cached_at", None)
        if cached_at is None or (time.time() - cached_at) >= max_age:
            return None
        return data
    except (json.JSONDecodeError, OSError):
        return None


def write_cache(file_path: str, data: dict):
    try:
        payload = {"_cached_at": time.time(), **data}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except OSError:
        pass


def read_stale_cache(file_path: str):
    """Read cache regardless of age — used as fallback when NBA API is down."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.pop("_cached_at", None)
        return data
    except (json.JSONDecodeError, OSError):
        return None




def with_retry(fn, *args, retries=MAX_RETRIES, delay=RETRY_DELAY, **kwargs):
    """
    Call fn(*args, **kwargs) up to `retries` times.
    Handles ConnectionError, Timeout, and NBA API 429 rate limits.
    Raises the last exception if all attempts fail.
    """
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            return fn(*args, **kwargs)
        except (ConnectionError, Timeout) as e:
            last_exc = e
            print(f"[WARNING] Attempt {attempt}/{retries} failed (network): {e}",
                  file=sys.stderr)
        except RequestException as e:
            last_exc = e
            msg = str(e)
            if "429" in msg or "Too Many Requests" in msg.lower():
                wait = delay * attempt  # back-off
                print(f"[WARNING] Rate-limited by NBA API. Waiting {wait}s...",
                      file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"[WARNING] Attempt {attempt}/{retries} failed: {e}",
                      file=sys.stderr)
        except Exception as e:
            last_exc = e
            print(f"[WARNING] Attempt {attempt}/{retries} unexpected error: {e}",
                  file=sys.stderr)

        if attempt < retries:
            time.sleep(delay)

    raise last_exc or RuntimeError("All retries exhausted")




def _fetch_standings_raw():
    return leaguestandingsv3.LeagueStandingsV3(timeout=REQUEST_TIMEOUT).get_dict()


def get_standings():
    cache_file = CACHE_FILES["standings"]
    cached = read_cache(cache_file)
    if cached:
        return cached

    try:
        data = with_retry(_fetch_standings_raw)
    except Exception as e:
        print(f"[ERROR] standings fetch failed: {e}", file=sys.stderr)
        # Return stale cache as fallback
        stale = read_stale_cache(cache_file)
        if stale:
            print("[INFO] Returning stale standings cache.", file=sys.stderr)
            return {**stale, "_stale": True}
        return {"error": "NBA API unavailable and no cached data exists.", "east": [], "west": []}

    rows = data['resultSets'][0]['rowSet']
    east, west = [], []

    for team in rows:
        team_name = team[4]
        team_id   = nickname_to_id.get(team_name)
        logo_url  = (f"https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg"
                     if team_id else DEFAULT_LOGO)
        info = {
            "logo":   logo_url,
            "team":   team[4],
            "wins":   team[13],
            "losses": team[14],
            "pct":    team[15],
            "gb":     team[38],
            "home":   team[18],
            "away":   team[19],
            "div":    team[23],
            "conf":   team[24],
        }
        (east if team[6] == "East" else west).append(info)

    result = {"east": east, "west": west}
    write_cache(cache_file, result)
    return result




STAT_INDEX = {"PTS": 24, "REB": 18, "AST": 19, "STL": 20, "BLK": 21, "MIN": 6}


def _fetch_league_category(stat: str):
    def _call():
        return leagueleaders.LeagueLeaders(
            stat_category_abbreviation=stat,
            per_mode48="PerGame",
            season=CURRENT_SEASON,
            season_type_all_star="Regular Season",
            timeout=REQUEST_TIMEOUT,
        ).get_dict()

    leaders = with_retry(_call)

    data_set = leaders.get("resultSet") or (
        leaders["resultSets"][0] if "resultSets" in leaders else None)

    if not data_set or not data_set.get("rowSet"):
        return stat, [{"error": f"No data for {stat}"}]

    players = [
        {"player": r[2], "team": r[4], "value": r[STAT_INDEX[stat]]}
        for r in data_set["rowSet"][:5]
    ]
    return stat, players


def get_league_leaders():
    cache_file = CACHE_FILES["league_leaders"]
    cached = read_cache(cache_file)
    if cached:
        return cached

    categories = ["PTS", "REB", "AST", "STL", "BLK", "MIN"]
    results    = {}
    errors     = []

    with ThreadPoolExecutor(max_workers=len(categories)) as executor:
        futures = {executor.submit(_fetch_league_category, s): s for s in categories}
        for future in as_completed(futures):
            stat = futures[future]
            try:
                _, players = future.result()
                results[stat] = players
            except Exception as e:
                errors.append(stat)
                print(f"[ERROR] League leaders {stat}: {e}", file=sys.stderr)
                results[stat] = [{"error": str(e)}]

    if errors:
        stale = read_stale_cache(cache_file)
        if stale:
            print("[INFO] Partial failure — merging with stale cache.", file=sys.stderr)
            for stat in errors:
                results[stat] = stale.get(stat, results[stat])

    write_cache(cache_file, results)
    return results




_NBA_TEAM_IDS = {str(t['id']) for t in all_teams
                 if not any(x in t['full_name']
                            for x in ['Stars', 'Hustle', 'Go-Go', 'Skyhawks'])}
_ID_TO_NAME   = {str(t['id']): t['full_name'] for t in all_teams}


def get_team_leaders():
    cache_file = CACHE_FILES["team_leaders"]
    cached = read_cache(cache_file)
    if cached:
        return cached

    def _call():
        return leaguedashteamstats.LeagueDashTeamStats(
            season=CURRENT_SEASON,
            season_type_all_star="Regular Season",
            per_mode_detailed="PerGame",
            league_id_nullable='00',
            timeout=REQUEST_TIMEOUT,
        ).get_dict()

    try:
        response = with_retry(_call)
    except Exception as e:
        print(f"[ERROR] team leaders fetch failed: {e}", file=sys.stderr)
        stale = read_stale_cache(cache_file)
        if stale:
            return {**stale, "_stale": True}
        return {s: [] for s in ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT']}

    headers = response['resultSets'][0]['headers']
    rows    = [r for r in response['resultSets'][0]['rowSet']
               if str(r[headers.index('TEAM_ID')]) in _NBA_TEAM_IDS]

    stat_keys  = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT']
    stat_idx   = {s: headers.index(s) for s in stat_keys}
    team_id_i  = headers.index('TEAM_ID')

    buckets: dict[str, list] = {s: [] for s in stat_keys}
    for row in rows:
        tid  = str(row[team_id_i])
        name = _ID_TO_NAME.get(tid, tid)
        for s, idx in stat_idx.items():
            buckets[s].append({"team": name, "value": row[idx]})

    final = {
        s: sorted(v, key=lambda x: x["value"], reverse=True)[:5]
        for s, v in buckets.items()
    }
    write_cache(cache_file, final)
    return final




def get_scores():
    import datetime
    cache_file = CACHE_FILES["scores"]
    cached = read_cache(cache_file, max_age=SCORES_CACHE)
    if cached:
        return cached

    def _call():
        today = datetime.date.today().strftime("%m/%d/%Y")
        return scoreboardv2.ScoreboardV2(
            game_date=today, league_id="00", timeout=REQUEST_TIMEOUT
        ).get_dict()

    try:
        board_dict = with_retry(_call, retries=2, delay=2)
    except Exception as e:
        print(f"[ERROR] scores fetch failed: {e}", file=sys.stderr)
        stale = read_stale_cache(cache_file)
        if stale:
            return {**stale, "_stale": True}
        return {"games": [], "count": 0, "error": str(e)}

    result_sets  = {rs["name"]: rs for rs in board_dict["resultSets"]}
    game_header  = result_sets.get("GameHeader", {})
    line_score   = result_sets.get("LineScore", {})

    gh_h = game_header.get("headers", [])
    gh_r = game_header.get("rowSet", [])
    ls_h = line_score.get("headers", [])
    ls_r = line_score.get("rowSet", [])

    def idx(headers, name):
        try:   return headers.index(name)
        except ValueError: return None

    gh_game_id    = idx(gh_h, "GAME_ID")
    gh_status     = idx(gh_h, "GAME_STATUS_TEXT")
    gh_period     = idx(gh_h, "LIVE_PERIOD")
    gh_home_id    = idx(gh_h, "HOME_TEAM_ID")
    gh_visitor_id = idx(gh_h, "VISITOR_TEAM_ID")
    ls_game_id    = idx(ls_h, "GAME_ID")
    ls_team_id    = idx(ls_h, "TEAM_ID")
    ls_tricode    = idx(ls_h, "TEAM_ABBREVIATION")
    ls_team_name  = idx(ls_h, "TEAM_CITY_NAME")
    ls_pts        = idx(ls_h, "PTS")

    score_lookup: dict = {}
    for row in ls_r:
        gid = row[ls_game_id]
        tid = str(row[ls_team_id])
        score_lookup.setdefault(gid, {})[tid] = row

    def safe(r, i):
        try:   return r[i] if i is not None and r else 0
        except (IndexError, TypeError): return 0

    games = []
    for row in gh_r:
        game_id  = row[gh_game_id]
        home_tid = str(row[gh_home_id])  if gh_home_id   is not None else ""
        away_tid = str(row[gh_visitor_id]) if gh_visitor_id is not None else ""
        gs       = score_lookup.get(game_id, {})
        home_row = gs.get(home_tid, [])
        away_row = gs.get(away_tid, [])

        games.append({
            "game_id":      game_id,
            "status":       (row[gh_status].strip() if gh_status is not None else ""),
            "period":       (row[gh_period] if gh_period is not None else 0),
            "home_team":    safe(home_row, ls_team_name) or _ID_TO_NAME.get(home_tid, ""),
            "home_tricode": safe(home_row, ls_tricode) or "",
            "home_score":   safe(home_row, ls_pts) or 0,
            "home_logo":    f"https://cdn.nba.com/logos/nba/{home_tid}/primary/L/logo.svg",
            "away_team":    safe(away_row, ls_team_name) or _ID_TO_NAME.get(away_tid, ""),
            "away_tricode": safe(away_row, ls_tricode) or "",
            "away_score":   safe(away_row, ls_pts) or 0,
            "away_logo":    f"https://cdn.nba.com/logos/nba/{away_tid}/primary/L/logo.svg",
        })

    result = {"games": games, "count": len(games)}
    write_cache(cache_file, result)
    return result




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No argument provided"}))
        sys.exit(1)

    option = sys.argv[1]
    handlers = {
        "standings":     get_standings,
        "league_leaders":get_league_leaders,
        "team_leaders":  get_team_leaders,
        "scores":        get_scores,
    }

    if option not in handlers:
        print(json.dumps({"error": f"Invalid option: {option}"}))
        sys.exit(1)

    print(json.dumps(handlers[option](), indent=2))