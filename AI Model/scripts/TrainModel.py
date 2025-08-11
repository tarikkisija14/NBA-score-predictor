import pandas as pd
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,accuracy_score
import joblib
import json


csvPath=r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025_clean_encoded.csv"

df = pd.read_csv(csvPath)

basic_stats = [
    'TEAM1_AST', 'TEAM2_AST',
    'TEAM1_REB', 'TEAM2_REB',
    'TEAM1_FG_PCT', 'TEAM2_FG_PCT',
    'TEAM1_FT_PCT', 'TEAM2_FT_PCT',

]


team_cols = [
    col for col in df.columns
    if (col.startswith('TEAM1_') or col.startswith('TEAM2_'))
    and not any(x in col for x in ['PTS', 'AST', 'REB', 'FG_PCT', 'FT_PCT', 'PLUS_MINUS', 'WIN'])
]

feature_cols = basic_stats + team_cols

df["WINNER"] = df["TEAM1_WIN"]
X = df[feature_cols]
y_winner = df['WINNER']
y_winner_pts = df['WINNER_PTS']
y_loser_pts = df['LOSER_PTS']

X_train, X_test, y_train_win, y_test_win, y_train_wpts, y_test_wpts, y_train_lpts, y_test_lpts = train_test_split(
    X, y_winner, y_winner_pts, y_loser_pts, test_size=0.2, random_state=42
)

model_winner = RandomForestClassifier(n_estimators=50, random_state=42)
model_winner.fit(X_train, y_train_win)

model_winner_pts = RandomForestRegressor(n_estimators=50, random_state=42)
model_winner_pts.fit(X_train, y_train_wpts)

model_loser_pts = RandomForestRegressor(n_estimators=50, random_state=42)
model_loser_pts.fit(X_train, y_train_lpts)

y_pred_win = model_winner.predict(X_test)
print(f"Tacnost predikcije pobjednika: {accuracy_score(y_test_win, y_pred_win):.4f}")

y_pred_win_pts = model_winner_pts.predict(X_test)
print(f"MSE za poene pobjednika: {mean_squared_error(y_test_wpts, y_pred_win_pts):.3f}")

y_pred_lose_pts = model_loser_pts.predict(X_test)
print(f"MSE za poene gubitnika: {mean_squared_error(y_test_lpts, y_pred_lose_pts):.3f}")

joblib.dump(model_winner, r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_winner.pkl")
joblib.dump(model_winner_pts, r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_winner_pts.pkl")
joblib.dump(model_loser_pts, r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_loser_pts.pkl")


with open(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\feature_columns.json", 'w') as f:
    json.dump(feature_cols, f)


