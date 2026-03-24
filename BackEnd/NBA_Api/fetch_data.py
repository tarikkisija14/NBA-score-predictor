"""
fetch_data.py  —  NBA Stats fetcher za ASP.NET backend
-------------------------------------------------------
Strategija: stale cache uvijek ima prioritet nad sporo/blokirano NBA API.
  - Ako postoji ijedan cache fajl (svjež ili star) → odmah ga vrati, bez mrežnog poziva
  - Ako nema nikakvih podataka → pokušaj NBA API, sačuvaj u cache
  - Refresh se desi samo u pozadini (background warm-up iz Program.cs)
  - Nema retry čekanja za ConnectionResetError — odmah odustaj
"""

import sys
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.static import teams


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CACHE_DURATION  = 60 * 60 * 6  # 6 sati — duži TTL jer NBA API je nestabilan
SCORES_CACHE    = 60            # 60 sec  (live scores)
REQUEST_TIMEOUT = 15            # kraći timeout — brže pada na cache
MAX_RETRIES     = 1             # samo 1 pokušaj — nema čekanja na retry
RETRY_DELAY     = 0

CACHE_FILES = {
    "standings":      "cache_standings.json",
    "league_leaders": "cache_league_leaders.json",
    "team_leaders":   "cache_team_leaders.json",
    "scores":         "cache_scores.json",
}

DEFAULT_LOGO = "https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg"

NBA_HEADERS = {
    "Host":               "stats.nba.com",
    "User-Agent":         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept":             "application/json, text/plain, */*",
    "Accept-Language":    "en-US,en;q=0.9",
    "Accept-Encoding":    "gzip, deflate, br",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token":  "true",
    "Referer":            "https://www.nba.com/",
    "Origin":             "https://www.nba.com",
    "Connection":         "keep-alive",
    "Sec-Fetch-Dest":     "empty",
    "Sec-Fetch-Mode":     "cors",
    "Sec-Fetch-Site":     "same-site",
}

all_teams      = teams.get_teams()
nickname_to_id = {t["nickname"]: t["id"] for t in all_teams}
_ID_TO_NAME    = {str(t["id"]): t["full_name"] for t in all_teams}
_NBA_TEAM_IDS  = {str(t["id"]) for t in all_teams
                  if not any(x in t["full_name"]
                             for x in ["Stars", "Hustle", "Go-Go", "Skyhawks"])}


# ---------------------------------------------------------------------------
# Season helper
# ---------------------------------------------------------------------------

def get_current_nba_season() -> str:
    import datetime
    now        = datetime.datetime.now()
    start_year = now.year if now.month >= 10 else now.year - 1
    return f"{start_year}-{str(start_year + 1)[-2:]}"


CURRENT_SEASON = get_current_nba_season()


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def read_cache(file_path: str, max_age: int = CACHE_DURATION):
    """Čita cache ako je svjež. Vraća dict ili None."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cached_at = data.pop("_cached_at", None)
        if cached_at is None or (time.time() - cached_at) >= max_age:
            return None
        return data
    except (json.JSONDecodeError, OSError):
        return None


def read_stale_cache(file_path: str):
    """Čita cache bez obzira na starost."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.pop("_cached_at", None)
        return data
    except (json.JSONDecodeError, OSError):
        return None


def write_cache(file_path: str, data: dict):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"_cached_at": time.time(), **data}, f, indent=2)
    except OSError:
        pass


def serve_cache_or_fetch(cache_file: str, fetch_fn, max_age: int = CACHE_DURATION,
                         empty_fallback: dict = None):
    """
    Glavna strategija:
      1. Svježi cache  → odmah vrati (0ms)
      2. Stale cache   → odmah vrati sa _stale=True (0ms), ne čekaj NBA API
      3. Nema cachea   → pokušaj fetch, sačuvaj, vrati
      4. Fetch padne   → vrati empty_fallback
    """
    # 1. Svježi cache
    fresh = read_cache(cache_file, max_age)
    if fresh is not None:
        return fresh

    # 2. Stale cache — vrati odmah, ne čekaj NBA API
    stale = read_stale_cache(cache_file)
    if stale is not None:
        print(f"[INFO] Serving stale cache for {cache_file}", file=sys.stderr)
        return {**stale, "_stale": True}

    # 3. Nema ničega — prvi pokretanje, moramo fetchovati
    print(f"[INFO] No cache found, fetching from NBA API...", file=sys.stderr)
    try:
        result = fetch_fn()
        write_cache(cache_file, result)
        return result
    except Exception as e:
        print(f"[ERROR] fetch failed: {e}", file=sys.stderr)
        return empty_fallback or {}


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _get(url: str, params: dict = None) -> dict:
    session = requests.Session()
    session.headers.update(NBA_HEADERS)
    resp = session.get(url, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Standings
# ---------------------------------------------------------------------------

def _fetch_standings() -> dict:
    data = _get("https://stats.nba.com/stats/leaguestandingsv3", params={
        "LeagueID": "00", "Season": CURRENT_SEASON, "SeasonType": "Regular Season",
    })
    rows = data["resultSets"][0]["rowSet"]
    east, west = [], []
    for team in rows:
        team_name = team[4]
        team_id   = nickname_to_id.get(team_name)
        logo_url  = (f"https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg"
                     if team_id else DEFAULT_LOGO)
        info = {
            "logo": logo_url, "team": team[4],
            "wins": team[13], "losses": team[14], "pct": team[15],
            "gb": team[38], "home": team[18], "away": team[19],
            "div": team[23], "conf": team[24],
        }
        (east if team[6] == "East" else west).append(info)
    return {"east": east, "west": west}


def get_standings():
    return serve_cache_or_fetch(
        CACHE_FILES["standings"], _fetch_standings,
        empty_fallback={"east": [], "west": [], "error": "No data available"})


# ---------------------------------------------------------------------------
# League leaders
# ---------------------------------------------------------------------------

STAT_INDEX = {"PTS": 24, "REB": 18, "AST": 19, "STL": 20, "BLK": 21, "MIN": 6}


def _fetch_one_league_category(stat: str):
    leaders  = leagueleaders.LeagueLeaders(
        stat_category_abbreviation=stat, per_mode48="PerGame",
        season=CURRENT_SEASON, season_type_all_star="Regular Season",
        timeout=REQUEST_TIMEOUT,
    ).get_dict()
    data_set = leaders.get("resultSet") or (
        leaders["resultSets"][0] if "resultSets" in leaders else None)
    if not data_set or not data_set.get("rowSet"):
        return stat, [{"error": f"No data for {stat}"}]
    players = [
        {"player": r[2], "team": r[4], "value": r[STAT_INDEX[stat]]}
        for r in data_set["rowSet"][:5]
    ]
    return stat, players


def _fetch_league_leaders() -> dict:
    categories = ["PTS", "REB", "AST", "STL", "BLK", "MIN"]
    results = {}
    with ThreadPoolExecutor(max_workers=len(categories)) as executor:
        futures = {executor.submit(_fetch_one_league_category, s): s for s in categories}
        for future in as_completed(futures):
            stat = futures[future]
            try:
                _, players    = future.result()
                results[stat] = players
            except Exception as e:
                print(f"[ERROR] League leaders {stat}: {e}", file=sys.stderr)
                results[stat] = [{"error": str(e)}]
    return results


def get_league_leaders():
    return serve_cache_or_fetch(
        CACHE_FILES["league_leaders"], _fetch_league_leaders,
        empty_fallback={s: [] for s in ["PTS", "REB", "AST", "STL", "BLK", "MIN"]})


# ---------------------------------------------------------------------------
# Team leaders
# ---------------------------------------------------------------------------

def _fetch_team_leaders() -> dict:
    response = _get("https://stats.nba.com/stats/leaguedashteamstats", params={
        "Conference": "", "DateFrom": "", "DateTo": "", "Division": "",
        "GameScope": "", "GameSegment": "", "Height": "", "LastNGames": "0",
        "LeagueID": "00", "Location": "", "MeasureType": "Base", "Month": "0",
        "OpponentTeamID": "0", "Outcome": "", "PORound": "0", "PaceAdjust": "N",
        "PerMode": "PerGame", "Period": "0", "PlayerExperience": "",
        "PlayerPosition": "", "PlusMinus": "N", "Rank": "N",
        "Season": CURRENT_SEASON, "SeasonSegment": "", "SeasonType": "Regular Season",
        "ShotClockRange": "", "StarterBench": "", "TeamID": "0",
        "TwoWay": "0", "VsConference": "", "VsDivision": "",
    })
    headers   = response["resultSets"][0]["headers"]
    rows      = [r for r in response["resultSets"][0]["rowSet"]
                 if str(r[headers.index("TEAM_ID")]) in _NBA_TEAM_IDS]
    stat_keys = ["PTS", "REB", "AST", "STL", "BLK", "FG_PCT"]
    stat_idx  = {s: headers.index(s) for s in stat_keys}
    team_id_i = headers.index("TEAM_ID")
    buckets: dict[str, list] = {s: [] for s in stat_keys}
    for row in rows:
        tid  = str(row[team_id_i])
        name = _ID_TO_NAME.get(tid, tid)
        for s, idx in stat_idx.items():
            buckets[s].append({"team": name, "value": row[idx]})
    return {
        s: sorted(v, key=lambda x: x["value"], reverse=True)[:5]
        for s, v in buckets.items()
    }


def get_team_leaders():
    return serve_cache_or_fetch(
        CACHE_FILES["team_leaders"], _fetch_team_leaders,
        empty_fallback={s: [] for s in ["PTS", "REB", "AST", "STL", "BLK", "FG_PCT"]})


# ---------------------------------------------------------------------------
# Scores
# ---------------------------------------------------------------------------

def _fetch_scores() -> dict:
    import datetime
    today      = datetime.date.today().strftime("%m/%d/%Y")
    board_dict = _get("https://stats.nba.com/stats/scoreboardv2", params={
        "DayOffset": "0", "GameDate": today, "LeagueID": "00",
    })
    result_sets = {rs["name"]: rs for rs in board_dict["resultSets"]}
    game_header = result_sets.get("GameHeader", {})
    line_score  = result_sets.get("LineScore", {})
    gh_h = game_header.get("headers", [])
    gh_r = game_header.get("rowSet", [])
    ls_h = line_score.get("headers", [])
    ls_r = line_score.get("rowSet", [])

    def idx(hdrs, name):
        try:   return hdrs.index(name)
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
        score_lookup.setdefault(row[ls_game_id], {})[str(row[ls_team_id])] = row

    def safe(r, i):
        try:   return r[i] if i is not None and r else 0
        except (IndexError, TypeError): return 0

    games = []
    for row in gh_r:
        game_id  = row[gh_game_id]
        home_tid = str(row[gh_home_id])    if gh_home_id    is not None else ""
        away_tid = str(row[gh_visitor_id]) if gh_visitor_id is not None else ""
        gs       = score_lookup.get(game_id, {})
        home_row = gs.get(home_tid, [])
        away_row = gs.get(away_tid, [])
        games.append({
            "game_id":      game_id,
            "status":       row[gh_status].strip() if gh_status is not None else "",
            "period":       row[gh_period] if gh_period is not None else 0,
            "home_team":    safe(home_row, ls_team_name) or _ID_TO_NAME.get(home_tid, ""),
            "home_tricode": safe(home_row, ls_tricode) or "",
            "home_score":   safe(home_row, ls_pts) or 0,
            "home_logo":    f"https://cdn.nba.com/logos/nba/{home_tid}/primary/L/logo.svg",
            "away_team":    safe(away_row, ls_team_name) or _ID_TO_NAME.get(away_tid, ""),
            "away_tricode": safe(away_row, ls_tricode) or "",
            "away_score":   safe(away_row, ls_pts) or 0,
            "away_logo":    f"https://cdn.nba.com/logos/nba/{away_tid}/primary/L/logo.svg",
        })
    return {"games": games, "count": len(games)}


def get_scores():
    return serve_cache_or_fetch(
        CACHE_FILES["scores"], _fetch_scores, max_age=SCORES_CACHE,
        empty_fallback={"games": [], "count": 0})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No argument provided"}))
        sys.exit(1)

    handlers = {
        "standings":      get_standings,
        "league_leaders": get_league_leaders,
        "team_leaders":   get_team_leaders,
        "scores":         get_scores,
    }

    option = sys.argv[1]
    if option not in handlers:
        print(json.dumps({"error": f"Invalid option: {option}"}))
        sys.exit(1)

    print(json.dumps(handlers[option](), indent=2))