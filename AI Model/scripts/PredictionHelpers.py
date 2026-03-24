
import pandas as pd

from Constants import (
    HEAD_TO_HEAD_LIMIT,
    CONFIDENCE_BASE,
    CONFIDENCE_RANGE,
    CONFIDENCE_MARGIN_OFFSET,
)


# ---------------------------------------------------------------------------
# Confidence estimation
# ---------------------------------------------------------------------------

def estimate_confidence_from_margin(winner_pts: int, loser_pts: int) -> float:
    """
    Derive a confidence percentage from the predicted score margin.

    Used as a fallback when the model does not support predict_proba.
    """
    margin = abs(winner_pts - loser_pts)
    return round(
        CONFIDENCE_BASE + (margin / (margin + CONFIDENCE_MARGIN_OFFSET)) * CONFIDENCE_RANGE,
        1,
    )


# ---------------------------------------------------------------------------
# Head-to-head lookup
# ---------------------------------------------------------------------------

def get_head_to_head(
    matchups_df: pd.DataFrame,
    team1_name: str,
    team2_name: str,
    limit: int = HEAD_TO_HEAD_LIMIT,
) -> dict:
    """
    Return the last *limit* head-to-head matchups between two teams,
    always presented from team1's perspective.
    """
    mask = (
        ((matchups_df["TEAM1_NAME"] == team1_name) & (matchups_df["TEAM2_NAME"] == team2_name))
        | ((matchups_df["TEAM1_NAME"] == team2_name) & (matchups_df["TEAM2_NAME"] == team1_name))
    )
    subset = matchups_df[mask].copy()

    if subset.empty:
        return {"games": [], "team1_wins": 0, "team2_wins": 0, "total": 0}

    subset = subset.sort_values(
        ["SEASON", "GAME_ID"], ascending=[False, False]
    ).head(limit)

    games: list[dict] = []
    team1_wins = 0
    team2_wins = 0

    for _, row in subset.iterrows():
        t1, t2         = row["TEAM1_NAME"], row["TEAM2_NAME"]
        t1_pts, t2_pts = int(row["TEAM1_PTS"]), int(row["TEAM2_PTS"])
        t1_won         = int(row["TEAM1_WIN"]) == 1

        if t1 == team1_name:
            home, away, home_pts, away_pts, team1_won_game = (
                t1, t2, t1_pts, t2_pts, t1_won
            )
        else:
            home, away, home_pts, away_pts, team1_won_game = (
                team1_name, team2_name, t2_pts, t1_pts, not t1_won
            )

        team1_wins += team1_won_game
        team2_wins += not team1_won_game

        games.append({
            "season":   row["SEASON"],
            "home":     home,
            "away":     away,
            "home_pts": home_pts,
            "away_pts": away_pts,
            "winner":   home if team1_won_game else away,
        })

    return {
        "games":       games,
        "team1_wins":  team1_wins,
        "team2_wins":  team2_wins,
        "total":       len(games),
    }