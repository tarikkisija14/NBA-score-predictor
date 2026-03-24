
import json
import sys
import joblib
import pandas as pd

from Constants import (
    MODEL_WINNER_FILENAME,
    MODEL_WINNER_PTS_FILENAME,
    MODEL_LOSER_PTS_FILENAME,
    FEATURE_COLS_FILENAME,
    RAW_DATA_FILENAME,
    AVG_STATS_FILENAME,
)
from Paths import model_path, data_path
from PredictionHelpers import estimate_confidence_from_margin, get_head_to_head




_model_winner     = joblib.load(model_path(MODEL_WINNER_FILENAME))
_model_winner_pts = joblib.load(model_path(MODEL_WINNER_PTS_FILENAME))
_model_loser_pts  = joblib.load(model_path(MODEL_LOSER_PTS_FILENAME))

with open(model_path(FEATURE_COLS_FILENAME)) as f:
    _feature_cols: list[str] = json.load(f)

_avg_stats   = pd.read_csv(data_path(AVG_STATS_FILENAME))
_matchups_df = pd.read_csv(data_path(RAW_DATA_FILENAME))

_stats_lookup: dict = {row["TEAM_NAME"]: row for _, row in _avg_stats.iterrows()}




def _validate_teams(team1_name: str, team2_name: str) -> None:
    if team1_name == team2_name:
        raise ValueError("Team 1 and Team 2 must be different teams.")
    for name in (team1_name, team2_name):
        if name not in _stats_lookup:
            raise ValueError(f"Unknown team: {name}")




_STAT_MAP_KEYS = [
    ("TEAM1_AST",        "TEAM2_AST",        "TEAM1_AST"),
    ("TEAM1_REB",        "TEAM2_REB",        "TEAM1_REB"),
    ("TEAM1_FG_PCT",     "TEAM2_FG_PCT",     "TEAM1_FG_PCT"),
    ("TEAM1_FT_PCT",     "TEAM2_FT_PCT",     "TEAM1_FT_PCT"),
]


def _build_input_row(team1_name: str, team2_name: str) -> pd.DataFrame:
    t1 = _stats_lookup[team1_name]
    t2 = _stats_lookup[team2_name]

    input_data = pd.DataFrame([[0] * len(_feature_cols)], columns=_feature_cols)

    for col1, col2, lookup_key in _STAT_MAP_KEYS:
        if col1 in input_data.columns:
            input_data.at[0, col1] = t1[lookup_key]
        if col2 in input_data.columns:
            input_data.at[0, col2] = t2[lookup_key]

    team1_col = f"TEAM1_{team1_name}"
    team2_col = f"TEAM2_{team2_name}"
    if team1_col not in input_data.columns:
        raise ValueError(f"Team not recognised in model: {team1_name}")
    if team2_col not in input_data.columns:
        raise ValueError(f"Team not recognised in model: {team2_name}")

    input_data.at[0, team1_col] = 1
    input_data.at[0, team2_col] = 1

    return input_data



def predict_game(team1_name: str, team2_name: str) -> dict:
    _validate_teams(team1_name, team2_name)

    X = _build_input_row(team1_name, team2_name)

    winner_pred     = _model_winner.predict(X)[0]
    winner_pts_pred = int(round(_model_winner_pts.predict(X)[0]))
    loser_pts_pred  = int(round(_model_loser_pts.predict(X)[0]))

    try:
        proba      = _model_winner.predict_proba(X)[0]
        confidence = round(float(max(proba)) * 100, 1)
    except AttributeError:
        confidence = estimate_confidence_from_margin(winner_pts_pred, loser_pts_pred)

    winner_name = team1_name if winner_pred == 1 else team2_name
    loser_name  = team2_name if winner_pred == 1 else team1_name

    return {
        "winner":        winner_name,
        "winner_points": winner_pts_pred,
        "loser":         loser_name,
        "loser_points":  loser_pts_pred,
        "confidence":    confidence,
        "head_to_head":  get_head_to_head(_matchups_df, team1_name, team2_name),
    }




if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "You must provide two team names"}))
        sys.exit(1)

    try:
        result = predict_game(sys.argv[1], sys.argv[2])
        print(json.dumps(result))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
        sys.exit(1)