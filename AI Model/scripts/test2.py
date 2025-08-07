import pandas as pd
import joblib


model_winner = joblib.load(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_winner.pkl")
model_winner_pts = joblib.load(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_winner_pts.pkl")
model_loser_pts = joblib.load(r"C:\Users\tarik\Desktop\nba score predictor\AI Model\models\model_loser_pts.pkl")

csvPath = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025_clean_encoded.csv"
df = pd.read_csv(csvPath)

exclude_cols = ['TEAM1_PTS', 'TEAM2_PTS', 'WINNER', 'WINNER_PTS', 'LOSER_PTS', 'TEAM1_WIN']
feature_cols = [col for col in df.columns if col not in exclude_cols]

X_winner = df[feature_cols]
y_winner = df['TEAM1_WIN']
y_winner_pts = df['WINNER_PTS']
y_loser_pts = df['LOSER_PTS']

from sklearn.model_selection import train_test_split
_, X_test_win, _, y_test_win = train_test_split(X_winner, y_winner, test_size=0.2, random_state=42)
_, X_test_pts_win, _, y_test_pts_win = train_test_split(X_winner, y_winner_pts, test_size=0.2, random_state=42)
_, X_test_pts_lose, _, y_test_pts_lose = train_test_split(X_winner, y_loser_pts, test_size=0.2, random_state=42)


y_pred_win = model_winner.predict(X_test_win)
y_pred_win_pts = model_winner_pts.predict(X_test_pts_win)
y_pred_lose_pts = model_loser_pts.predict(X_test_pts_lose)



print("--- REZULTATI PREDIKCIJA ---")
for i in range(len(X_test_win)):
    stvarni_pobjednik = "TIM1" if y_test_win.iloc[i] == 1 else "TIM2"
    pred_pobjednik = "TIM1" if y_pred_win[i] == 1 else "TIM2"

    stvarni_winner_pts = y_test_pts_win.iloc[i]
    pred_winner_pts = round(y_pred_win_pts[i])

    stvarni_loser_pts = y_test_pts_lose.iloc[i]
    pred_loser_pts = round(y_pred_lose_pts[i])


    print(f"Utakmica {i+1}: {pred_pobjednik} {pred_winner_pts}:{pred_loser_pts} {'TIM2' if pred_pobjednik == 'TIM1' else 'TIM1'} | "
          f"{stvarni_pobjednik} {stvarni_winner_pts}:{stvarni_loser_pts} {'TIM2' if stvarni_pobjednik == 'TIM1' else 'TIM1'}")

