
import os
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, accuracy_score


BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE_DIR, '..', 'data')
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

CSV_PATH = os.path.join(DATA_DIR, 'ALL_NBA_matchups_2020_2025_clean_encoded.csv')


df = pd.read_csv(CSV_PATH)
print(f"Učitano {len(df)} utakmica, {len(df.columns)} kolona")


per_team_stats = [
    'TEAM1_FG_PCT',  'TEAM2_FG_PCT',
    'TEAM1_FT_PCT',  'TEAM2_FT_PCT',
    'TEAM1_REB',     'TEAM2_REB',
    'TEAM1_AST',     'TEAM2_AST',
    'TEAM1_PLUS_MINUS', 'TEAM2_PLUS_MINUS',
    'TEAM1_FG3_PCT', 'TEAM2_FG3_PCT',
    'TEAM1_TOV',     'TEAM2_TOV',
    'TEAM1_STL',     'TEAM2_STL',
    'TEAM1_BLK',     'TEAM2_BLK',
    'TEAM1_FORM',    'TEAM2_FORM',
]

# Diff/delta features — very informative for tree models
diff_stats = [
    'FG_PCT_DIFF', 'REB_DIFF', 'AST_DIFF', 'PLUS_MINUS_DIFF',
    'FG3_PCT_DIFF', 'TOV_DIFF', 'STL_DIFF', 'BLK_DIFF', 'FORM_DIFF',
]


team_cols = [
    col for col in df.columns
    if (col.startswith('TEAM1_') or col.startswith('TEAM2_'))
    and not any(x in col for x in [
        'PTS', 'AST', 'REB', 'FG_PCT', 'FT_PCT', 'FG3_PCT',
        'PLUS_MINUS', 'WIN', 'TOV', 'STL', 'BLK', 'FORM', 'ID'
    ])
]


season_cols = ['SEASON_START'] if 'SEASON_START' in df.columns else []


feature_cols = [
    c for c in (per_team_stats + diff_stats + season_cols + team_cols)
    if c in df.columns
]

print(f"Feature kolone ({len(feature_cols)}): {feature_cols[:15]} ...")

# ── TARGETS ──────────────────────────────────────────────────────────────────
X           = df[feature_cols]
y_winner    = df['WINNER']
y_winner_pts = df['WINNER_PTS']
y_loser_pts  = df['LOSER_PTS']

X_train, X_test, \
y_train_win, y_test_win, \
y_train_wpts, y_test_wpts, \
y_train_lpts, y_test_lpts = train_test_split(
    X, y_winner, y_winner_pts, y_loser_pts,
    test_size=0.2, random_state=42
)

# ── WINNER CLASSIFIER ────────────────────────────────────────────────────────
print("\nTreniranje modela pobjednika (GradientBoostingClassifier)...")
model_winner = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.8,
    random_state=42
)
model_winner.fit(X_train, y_train_win)

y_pred_win = model_winner.predict(X_test)
acc = accuracy_score(y_test_win, y_pred_win)
print(f"  Test accuracy:  {acc:.4f}")

cv_scores = cross_val_score(model_winner, X, y_winner, cv=5, scoring='accuracy')
print(f"  CV accuracy:    {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")


print("\nTreniranje modela poena pobjednika (GradientBoostingRegressor)...")
model_winner_pts = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.8,
    random_state=42
)
model_winner_pts.fit(X_train, y_train_wpts)

y_pred_wpts = model_winner_pts.predict(X_test)
rmse_w = np.sqrt(mean_squared_error(y_test_wpts, y_pred_wpts))
print(f"  RMSE poena pobjednika: {rmse_w:.3f}")


print("\nTreniranje modela poena gubitnika (GradientBoostingRegressor)...")
model_loser_pts = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.8,
    random_state=42
)
model_loser_pts.fit(X_train, y_train_lpts)

y_pred_lpts = model_loser_pts.predict(X_test)
rmse_l = np.sqrt(mean_squared_error(y_test_lpts, y_pred_lpts))
print(f"  RMSE poena gubitnika: {rmse_l:.3f}")


importances = model_winner.feature_importances_
top_idx = np.argsort(importances)[::-1][:15]
print("\nTop 15 najbitnijih feature-a:")
for i in top_idx:
    print(f"  {feature_cols[i]:<35} {importances[i]:.4f}")


joblib.dump(model_winner,     os.path.join(MODEL_DIR, 'model_winner.pkl'))
joblib.dump(model_winner_pts, os.path.join(MODEL_DIR, 'model_winner_pts.pkl'))
joblib.dump(model_loser_pts,  os.path.join(MODEL_DIR, 'model_loser_pts.pkl'))

with open(os.path.join(MODEL_DIR, 'feature_columns.json'), 'w') as f:
    json.dump(feature_cols, f, indent=2)

print(f"\nModeli sačuvani u: {MODEL_DIR}")
print("Gotovo!")