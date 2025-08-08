import pandas as pd
import json
import joblib
import numpy as np

model_winner = joblib.load(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_winner.pkl")
model_winner_pts = joblib.load(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_winner_pts.pkl")
model_loser_pts = joblib.load(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_loser_pts.pkl")

with open(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\feature_columns.json", 'r') as f:
    feature_cols = json.load(f)

def predict_game(input_data):
    X_input = pd.DataFrame([input_data], columns=feature_cols)


    winner_pred = model_winner.predict(X_input)[0]
    winner_pts_pred = int(round(model_winner_pts.predict(X_input)[0]))
    loser_pts_pred = int(round(model_loser_pts.predict(X_input)[0]))

    return {
        "winner": "TEAM1" if winner_pred == 1 else "TEAM2",
        "winner_points": winner_pts_pred,
        "loser_points": loser_pts_pred
    }


example_input = {

    'TEAM1_AST': 25, 'TEAM2_AST': 22,
    'TEAM1_REB': 45, 'TEAM2_REB': 42,
    'TEAM1_FG_PCT': 0.48, 'TEAM2_FG_PCT': 0.45,
    'TEAM1_FT_PCT': 0.85, 'TEAM2_FT_PCT': 0.78,
    'TEAM1_PLUS_MINUS': 5, 'TEAM2_PLUS_MINUS': -5,


    'TEAM1_Boston Celtics': 1,
    'TEAM1_Los Angeles Lakers': 0,
    'TEAM2_Boston Celtics': 0,
    'TEAM2_Los Angeles Lakers': 1
}

for col in feature_cols:
    if col not in example_input:
        example_input[col] = 0

result = predict_game(example_input)

team1_name = [col.replace('TEAM1_', '') for col in example_input if col.startswith('TEAM1_') and example_input[col] == 1][0]
team2_name = [col.replace('TEAM2_', '') for col in example_input if col.startswith('TEAM2_') and example_input[col] == 1][0]

if result["winner"] == "TEAM1":
    print(f" {team1_name} {result['winner_points']} : {result['loser_points']} {team2_name}")
else:
    print(f"{team1_name} {result['loser_points']} : {result['winner_points']}  {team2_name}")