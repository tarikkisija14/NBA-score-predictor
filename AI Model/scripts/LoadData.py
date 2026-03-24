import os
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder

from Constants import (
    DEFAULT_SEASONS,
    FORM_WINDOW,
    OPTIONAL_STAT_COLS,
)
from Paths import data_path
from Constants import RAW_DATA_FILENAME



def _compute_season_form(games: pd.DataFrame) -> pd.DataFrame:

    form_tracker: dict[str, list[int]] = {}
    rows: list[dict] = []

    for _, row in games.iterrows():
        team_id = row["TEAM_ID"]
        if team_id not in form_tracker:
            form_tracker[team_id] = []

        recent_games = form_tracker[team_id][-FORM_WINDOW:]
        form = round(sum(recent_games) / len(recent_games), 4) if recent_games else 0.5

        rows.append({"GAME_ID": row["GAME_ID"], "TEAM_ID": team_id, "FORM": form})
        form_tracker[team_id].append(1 if row["WL"] == "W" else 0)

    return pd.DataFrame(rows)


def _lookup_team_form(form_df: pd.DataFrame, team_id, game_id) -> float:
    """Return the pre-game form value for a team in a specific game."""
    mask = (form_df["GAME_ID"] == game_id) & (form_df["TEAM_ID"] == team_id)
    result = form_df.loc[mask, "FORM"]
    return float(result.values[0]) if not result.empty else 0.5




def _build_matchup_row(
    season: str,
    game_id,
    team1: pd.Series,
    team2: pd.Series,
    form_df: pd.DataFrame,
) -> dict:

    return {
        "SEASON":    season,
        "GAME_ID":   game_id,
        "GAME_DATE": team1["GAME_DATE"],

        "TEAM1_NAME": team1["TEAM_NAME"],
        "TEAM2_NAME": team2["TEAM_NAME"],

        "TEAM1_PTS": team1["PTS"],
        "TEAM2_PTS": team2["PTS"],

        "TEAM1_AST": team1["AST"],
        "TEAM2_AST": team2["AST"],
        "TEAM1_REB": team1["REB"],
        "TEAM2_REB": team2["REB"],

        "TEAM1_FG_PCT":      team1["FG_PCT"],
        "TEAM2_FG_PCT":      team2["FG_PCT"],
        "TEAM1_FT_PCT":      team1["FT_PCT"],
        "TEAM2_FT_PCT":      team2["FT_PCT"],
        "TEAM1_PLUS_MINUS":  team1["PLUS_MINUS"],
        "TEAM2_PLUS_MINUS":  team2["PLUS_MINUS"],

        "TEAM1_FG3_PCT": team1.get("FG3_PCT"),
        "TEAM2_FG3_PCT": team2.get("FG3_PCT"),
        "TEAM1_TOV":     team1.get("TOV"),
        "TEAM2_TOV":     team2.get("TOV"),
        "TEAM1_STL":     team1.get("STL"),
        "TEAM2_STL":     team2.get("STL"),
        "TEAM1_BLK":     team1.get("BLK"),
        "TEAM2_BLK":     team2.get("BLK"),

        "TEAM1_FORM": _lookup_team_form(form_df, team1["TEAM_ID"], game_id),
        "TEAM2_FORM": _lookup_team_form(form_df, team2["TEAM_ID"], game_id),

        "TEAM1_WIN": 1 if team1["WL"] == "W" else 0,
    }




def fetch_multiple_seasons(seasons: list[str], output_path: str) -> None:

    all_matchups: list[dict] = []

    for season in seasons:
        print(f"\n Season: {season}")
        finder = leaguegamefinder.LeagueGameFinder(
            season_nullable=season,
            season_type_nullable="Regular Season",
        )
        games = finder.get_data_frames()[0]
        games = games.dropna(subset=["GAME_ID"])
        games = games.sort_values(["GAME_DATE", "GAME_ID"])

        form_df = _compute_season_form(games)

        for game_id, group in games.groupby("GAME_ID"):
            if len(group) != 2:
                continue
            team1, team2 = group.iloc[0], group.iloc[1]
            all_matchups.append(
                _build_matchup_row(season, game_id, team1, team2, form_df)
            )

    df = pd.DataFrame(all_matchups)

    for col in OPTIONAL_STAT_COLS:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    df.to_csv(output_path, index=False)
    print(f"\n Saved {len(df)} games to: {output_path}")
    print(f" Columns: {list(df.columns)}")




if __name__ == "__main__":
    output_filepath = data_path(RAW_DATA_FILENAME)
    fetch_multiple_seasons(DEFAULT_SEASONS, output_filepath)