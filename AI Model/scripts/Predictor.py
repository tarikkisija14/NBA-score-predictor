import pandas as pd
import json
import joblib
import numpy as np
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

model_winner     = joblib.load(os.path.join(MODEL_DIR, "model_winner.pkl"))
model_winner_pts = joblib.load(os.path.join(MODEL_DIR, "model_winner_pts.pkl"))
model_loser_pts  = joblib.load(os.path.join(MODEL_DIR, "model_loser_pts.pkl"))

with open(os.path.join(MODEL_DIR, "feature_columns.json"), "r") as f:
    feature_cols = json.load(f)

avg_stats = pd.read_csv(os.path.join(DATA_DIR, "team_average_stats.csv"))


stats_lookup = {row["TEAM_NAME"]: row for _, row in avg_stats.iterrows()}


def predict_game(team1_name, team2_name):
    if team1_name == team2_name:
        raise ValueError("Team 1 and Team 2 must be different teams.")
    if team1_name not in stats_lookup:
        raise ValueError(f"Unknown team: {team1_name}")
    if team2_name not in stats_lookup:
        raise ValueError(f"Unknown team: {team2_name}")

    input_data = pd.DataFrame([[0] * len(feature_cols)], columns=feature_cols)


    t1 = stats_lookup[team1_name]
    t2 = stats_lookup[team2_name]

    stat_map = {
        "TEAM1_AST":    t1["TEAM1_AST"],
        "TEAM2_AST":    t2["TEAM1_AST"],
        "TEAM1_REB":    t1["TEAM1_REB"],
        "TEAM2_REB":    t2["TEAM1_REB"],
        "TEAM1_FG_PCT": t1["TEAM1_FG_PCT"],
        "TEAM2_FG_PCT": t2["TEAM1_FG_PCT"],
        "TEAM1_FT_PCT": t1["TEAM1_FT_PCT"],
        "TEAM2_FT_PCT": t2["TEAM1_FT_PCT"],
    }

    for col, val in stat_map.items():
        if col in input_data.columns:
            input_data.at[0, col] = val

    # One-hot encode team names
    team1_col = f"TEAM1_{team1_name}"
    team2_col = f"TEAM2_{team2_name}"

    if team1_col not in input_data.columns:
        raise ValueError(f"Team not recognised in model: {team1_name}")
    if team2_col not in input_data.columns:
        raise ValueError(f"Team not recognised in model: {team2_name}")

    input_data.at[0, team1_col] = 1
    input_data.at[0, team2_col] = 1

    winner_pred      = model_winner.predict(input_data)[0]
    winner_pts_pred  = int(round(model_winner_pts.predict(input_data)[0]))
    loser_pts_pred   = int(round(model_loser_pts.predict(input_data)[0]))

    winner_name = team1_name if winner_pred == 1 else team2_name
    loser_name  = team2_name if winner_pred == 1 else team1_name

    return {
        "winner":        winner_name,
        "winner_points": winner_pts_pred,
        "loser":         loser_name,
        "loser_points":  loser_pts_pred,
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "You must provide two team names"}))
        sys.exit(1)

    team1 = sys.argv[1]
    team2 = sys.argv[2]

    try:
        result = predict_game(team1, team2)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)