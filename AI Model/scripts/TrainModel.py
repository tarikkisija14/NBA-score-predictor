import pandas as pd
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,accuracy_score



csvPath=r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025_clean_encoded.csv"

df = pd.read_csv(csvPath)

df["WINNER"] = df["TEAM1_WIN"]
df["WINNER_PTS"] = df.apply(lambda row: row['TEAM1_PTS'] if row['WINNER'] == 1 else row['TEAM2_PTS'], axis=1)
df["LOSER_PTS"] = df.apply(lambda row: row['TEAM2_PTS'] if row['WINNER'] == 1 else row['TEAM1_PTS'], axis=1)


exclude_cols = [
    'TEAM1_PTS', 'TEAM2_PTS',
    'WINNER', 'WINNER_PTS', 'LOSER_PTS'
]
feature_cols = [col for col in df.columns if col not in exclude_cols]


X_winner = df[feature_cols]
y_winner = df['WINNER']

X_winner_pts = df['WINNER_PTS']
y_loser_pts = df['LOSER_PTS']

X_train_win, X_test_win, y_train_win, y_test_win = train_test_split(X_winner, y_winner, test_size=0.2, random_state=42)

model_winner=RandomForestClassifier(n_estimators=100, random_state=42)
model_winner.fit(X_train_win, y_train_win)

y_pred_win = model_winner.predict(X_test_win)
print(f"Tacnost predikcije pobjednika: {accuracy_score(y_test_win, y_pred_win):.4f}")

y_winner_pts = df['WINNER_PTS']
X_points = df[feature_cols]

X_train_pts_win, X_test_pts_win, y_train_pts_win, y_test_pts_win = train_test_split(X_points, y_winner_pts, test_size=0.2, random_state=42)

model_winner_pts=RandomForestRegressor(n_estimators=100, random_state=42)
model_winner_pts.fit(X_train_pts_win, y_train_pts_win)

y_pred_win_pts = model_winner_pts.predict(X_test_pts_win)
print(f"MSE za poene pobjednika: {mean_squared_error(y_test_pts_win, y_pred_win_pts):.3f}")

