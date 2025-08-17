import pandas as pd
import json
import joblib
import numpy as np
import sys


model_winner = joblib.load(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_winner.pkl")
model_winner_pts = joblib.load(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_winner_pts.pkl")
model_loser_pts = joblib.load(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_loser_pts.pkl")


with open(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\feature_columns.json", 'r') as f:
    feature_cols = json.load(f)


avg_stats = pd.read_csv(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\team_average_stats.csv")

def predict_game(team1_name, team2_name):
    input_data = pd.DataFrame([[0] * len(feature_cols)], columns=feature_cols)

    team1_col = f"TEAM1_{team1_name}"
    team2_col = f"TEAM2_{team2_name}"

    if team1_col in input_data.columns:
        input_data.at[0, team1_col] = 1
    else:
        raise ValueError(f"Ne postoji kolona {team1_col}!")

    if team2_col in input_data.columns:
        input_data.at[0, team2_col] = 1
    else:
        raise ValueError(f"Ne postoji kolona {team2_col}!")


    winner_pred = model_winner.predict(input_data)[0]
    winner_pts_pred = int(round(model_winner_pts.predict(input_data)[0]))
    loser_pts_pred = int(round(model_loser_pts.predict(input_data)[0]))

    winner_name = team1_name if winner_pred == 1 else team2_name
    loser_name = team1_name if winner_pred == 0 else team2_name

    return {
        "winner": winner_name,
        "winner_points": winner_pts_pred,
        "loser": loser_name,
        "loser_points": loser_pts_pred
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