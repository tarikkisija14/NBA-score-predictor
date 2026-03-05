

import os
import json
import joblib
import numpy as np
import pandas as pd
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')
DATA_DIR  = os.path.join(BASE_DIR, '..', 'data')


_state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load models and data ONCE when the server starts."""
    print("Učitavanje modela...")
    _state['model_winner']     = joblib.load(os.path.join(MODEL_DIR, 'model_winner.pkl'))
    _state['model_winner_pts'] = joblib.load(os.path.join(MODEL_DIR, 'model_winner_pts.pkl'))
    _state['model_loser_pts']  = joblib.load(os.path.join(MODEL_DIR, 'model_loser_pts.pkl'))

    with open(os.path.join(MODEL_DIR, 'feature_columns.json')) as f:
        _state['feature_cols'] = json.load(f)

    avg_stats   = pd.read_csv(os.path.join(DATA_DIR, 'team_average_stats.csv'))
    matchups_df = pd.read_csv(os.path.join(DATA_DIR, 'ALL_NBA_matchups_2020_2025.csv'))

    _state['stats_lookup'] = {row['TEAM_NAME']: row for _, row in avg_stats.iterrows()}
    _state['matchups_df']  = matchups_df

    print(f"Modeli učitani. Timovi dostupni: {len(_state['stats_lookup'])}")
    yield
    # Cleanup (if needed)
    _state.clear()


app = FastAPI(title="NBA Predictor API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "https://localhost:5001",
                   "http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)



class PredictRequest(BaseModel):
    home_team: str
    away_team: str




def get_head_to_head(team1_name: str, team2_name: str, limit: int = 10) -> dict:
    matchups_df = _state['matchups_df']
    mask = (
        ((matchups_df['TEAM1_NAME'] == team1_name) & (matchups_df['TEAM2_NAME'] == team2_name)) |
        ((matchups_df['TEAM1_NAME'] == team2_name) & (matchups_df['TEAM2_NAME'] == team1_name))
    )
    subset = matchups_df[mask].copy()

    if subset.empty:
        return {'games': [], 'team1_wins': 0, 'team2_wins': 0, 'total': 0}

    subset = subset.sort_values(['SEASON', 'GAME_ID'], ascending=[False, False]).head(limit)

    games, team1_wins, team2_wins = [], 0, 0

    for _, row in subset.iterrows():
        t1, t2 = row['TEAM1_NAME'], row['TEAM2_NAME']
        t1_pts, t2_pts = int(row['TEAM1_PTS']), int(row['TEAM2_PTS'])
        t1_won = int(row['TEAM1_WIN']) == 1

        if t1 == team1_name:
            home, away, home_pts, away_pts, team1_won_game = t1, t2, t1_pts, t2_pts, t1_won
        else:
            home, away, home_pts, away_pts, team1_won_game = (
                team1_name, team2_name, t2_pts, t1_pts, not t1_won)

        team1_wins += team1_won_game
        team2_wins += not team1_won_game

        games.append({
            'season':   row['SEASON'],
            'home':     home,
            'away':     away,
            'home_pts': home_pts,
            'away_pts': away_pts,
            'winner':   home if team1_won_game else away,
        })

    return {'games': games, 'team1_wins': team1_wins,
            'team2_wins': team2_wins, 'total': len(games)}


def build_input(team1_name: str, team2_name: str) -> pd.DataFrame:
    """Build the feature vector for prediction."""
    stats_lookup = _state['stats_lookup']
    feature_cols = _state['feature_cols']

    t1 = stats_lookup[team1_name]
    t2 = stats_lookup[team2_name]

    row = {col: 0 for col in feature_cols}


    stat_pairs = [
        ('TEAM1_AST',      'TEAM2_AST',      'TEAM1_AST'),
        ('TEAM1_REB',      'TEAM2_REB',      'TEAM1_REB'),
        ('TEAM1_FG_PCT',   'TEAM2_FG_PCT',   'TEAM1_FG_PCT'),
        ('TEAM1_FT_PCT',   'TEAM2_FT_PCT',   'TEAM1_FT_PCT'),
        ('TEAM1_PLUS_MINUS','TEAM2_PLUS_MINUS','TEAM1_PLUS_MINUS'),
        # NEW stats
        ('TEAM1_FG3_PCT',  'TEAM2_FG3_PCT',  'TEAM1_FG3_PCT'),
        ('TEAM1_TOV',      'TEAM2_TOV',       'TEAM1_TOV'),
        ('TEAM1_STL',      'TEAM2_STL',       'TEAM1_STL'),
        ('TEAM1_BLK',      'TEAM2_BLK',       'TEAM1_BLK'),
        ('TEAM1_FORM',     'TEAM2_FORM',      'TEAM1_FORM'),
    ]
    for col1, col2, lookup_key in stat_pairs:
        if col1 in row and lookup_key in t1:
            row[col1] = t1[lookup_key]
        if col2 in row and lookup_key in t2:
            row[col2] = t2[lookup_key]


    diff_map = {
        'FG_PCT_DIFF':    ('TEAM1_FG_PCT',    'TEAM2_FG_PCT'),
        'REB_DIFF':       ('TEAM1_REB',       'TEAM2_REB'),
        'AST_DIFF':       ('TEAM1_AST',       'TEAM2_AST'),
        'PLUS_MINUS_DIFF':('TEAM1_PLUS_MINUS','TEAM2_PLUS_MINUS'),
        'FG3_PCT_DIFF':   ('TEAM1_FG3_PCT',   'TEAM2_FG3_PCT'),
        'TOV_DIFF':       ('TEAM1_TOV',       'TEAM2_TOV'),
        'STL_DIFF':       ('TEAM1_STL',       'TEAM2_STL'),
        'BLK_DIFF':       ('TEAM1_BLK',       'TEAM2_BLK'),
        'FORM_DIFF':      ('TEAM1_FORM',      'TEAM2_FORM'),
    }
    for diff_col, (c1, c2) in diff_map.items():
        if diff_col in row:
            row[diff_col] = row.get(c1, 0) - row.get(c2, 0)


    t1_col = f'TEAM1_{team1_name}'
    t2_col = f'TEAM2_{team2_name}'
    if t1_col in row:
        row[t1_col] = 1
    if t2_col in row:
        row[t2_col] = 1

    return pd.DataFrame([row], columns=feature_cols)




@app.get('/health')
def health():
    return {'status': 'ok', 'models_loaded': bool(_state)}


@app.post('/predict')
def predict(req: PredictRequest):
    stats_lookup  = _state['stats_lookup']
    model_winner  = _state['model_winner']
    model_w_pts   = _state['model_winner_pts']
    model_l_pts   = _state['model_loser_pts']

    home, away = req.home_team.strip(), req.away_team.strip()

    if home.lower() == away.lower():
        raise HTTPException(400, 'Home and away teams must be different.')
    if home not in stats_lookup:
        raise HTTPException(400, f'Unknown team: {home}')
    if away not in stats_lookup:
        raise HTTPException(400, f'Unknown team: {away}')

    X = build_input(home, away)

    winner_pred      = model_winner.predict(X)[0]
    winner_pts_pred  = int(round(model_w_pts.predict(X)[0]))
    loser_pts_pred   = int(round(model_l_pts.predict(X)[0]))

    try:
        proba      = model_winner.predict_proba(X)[0]
        confidence = round(float(max(proba)) * 100, 1)
    except AttributeError:
        margin     = abs(winner_pts_pred - loser_pts_pred)
        confidence = round(50 + (margin / (margin + 10)) * 38, 1)

    winner_name = home if winner_pred == 1 else away
    loser_name  = away if winner_pred == 1 else home

    h2h = get_head_to_head(home, away)

    return {
        'winner':        winner_name,
        'winner_points': winner_pts_pred,
        'loser':         loser_name,
        'loser_points':  loser_pts_pred,
        'confidence':    confidence,
        'head_to_head':  h2h,
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('predict_api:app', host='127.0.0.1', port=8000, reload=False)