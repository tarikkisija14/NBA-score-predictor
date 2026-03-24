
import json
import joblib
import pandas as pd
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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




ALLOWED_ORIGINS = [
    "http://localhost:5000",
    "https://localhost:5001",
    "http://localhost:4200",
]

# Maps (team1_col, team2_col) → the lookup key in the avg-stats row
_STAT_PAIRS: list[tuple[str, str, str]] = [
    ("TEAM1_AST",        "TEAM2_AST",        "TEAM1_AST"),
    ("TEAM1_REB",        "TEAM2_REB",        "TEAM1_REB"),
    ("TEAM1_FG_PCT",     "TEAM2_FG_PCT",     "TEAM1_FG_PCT"),
    ("TEAM1_FT_PCT",     "TEAM2_FT_PCT",     "TEAM1_FT_PCT"),
    ("TEAM1_PLUS_MINUS", "TEAM2_PLUS_MINUS", "TEAM1_PLUS_MINUS"),
    ("TEAM1_FG3_PCT",    "TEAM2_FG3_PCT",    "TEAM1_FG3_PCT"),
    ("TEAM1_TOV",        "TEAM2_TOV",        "TEAM1_TOV"),
    ("TEAM1_STL",        "TEAM2_STL",        "TEAM1_STL"),
    ("TEAM1_BLK",        "TEAM2_BLK",        "TEAM1_BLK"),
    ("TEAM1_FORM",       "TEAM2_FORM",       "TEAM1_FORM"),
]

_DIFF_MAP: dict[str, tuple[str, str]] = {
    "FG_PCT_DIFF":     ("TEAM1_FG_PCT",     "TEAM2_FG_PCT"),
    "REB_DIFF":        ("TEAM1_REB",        "TEAM2_REB"),
    "AST_DIFF":        ("TEAM1_AST",        "TEAM2_AST"),
    "PLUS_MINUS_DIFF": ("TEAM1_PLUS_MINUS", "TEAM2_PLUS_MINUS"),
    "FG3_PCT_DIFF":    ("TEAM1_FG3_PCT",    "TEAM2_FG3_PCT"),
    "TOV_DIFF":        ("TEAM1_TOV",        "TEAM2_TOV"),
    "STL_DIFF":        ("TEAM1_STL",        "TEAM2_STL"),
    "BLK_DIFF":        ("TEAM1_BLK",        "TEAM2_BLK"),
    "FORM_DIFF":       ("TEAM1_FORM",       "TEAM2_FORM"),
}



_state: dict = {}




@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading models...")
    _state["model_winner"]     = joblib.load(model_path(MODEL_WINNER_FILENAME))
    _state["model_winner_pts"] = joblib.load(model_path(MODEL_WINNER_PTS_FILENAME))
    _state["model_loser_pts"]  = joblib.load(model_path(MODEL_LOSER_PTS_FILENAME))

    with open(model_path(FEATURE_COLS_FILENAME)) as f:
        _state["feature_cols"] = json.load(f)

    avg_stats   = pd.read_csv(data_path(AVG_STATS_FILENAME))
    matchups_df = pd.read_csv(data_path(RAW_DATA_FILENAME))

    _state["stats_lookup"] = {row["TEAM_NAME"]: row for _, row in avg_stats.iterrows()}
    _state["matchups_df"]  = matchups_df

    print(f"Models loaded. Teams available: {len(_state['stats_lookup'])}")
    yield
    _state.clear()




app = FastAPI(title="NBA Predictor API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)




class PredictRequest(BaseModel):
    home_team: str
    away_team: str



def _build_input_row(team1_name: str, team2_name: str) -> pd.DataFrame:
    stats_lookup = _state["stats_lookup"]
    feature_cols = _state["feature_cols"]

    t1 = stats_lookup[team1_name]
    t2 = stats_lookup[team2_name]

    row: dict = {col: 0 for col in feature_cols}

    for col1, col2, lookup_key in _STAT_PAIRS:
        if col1 in row and lookup_key in t1:
            row[col1] = t1[lookup_key]
        if col2 in row and lookup_key in t2:
            row[col2] = t2[lookup_key]

    for diff_col, (c1, c2) in _DIFF_MAP.items():
        if diff_col in row:
            row[diff_col] = row.get(c1, 0) - row.get(c2, 0)

    t1_col = f"TEAM1_{team1_name}"
    t2_col = f"TEAM2_{team2_name}"
    if t1_col in row:
        row[t1_col] = 1
    if t2_col in row:
        row[t2_col] = 1

    return pd.DataFrame([row], columns=feature_cols)


def _validate_teams(home: str, away: str) -> None:
    stats_lookup = _state["stats_lookup"]
    if home.lower() == away.lower():
        raise HTTPException(400, "Home and away teams must be different.")
    if home not in stats_lookup:
        raise HTTPException(400, f"Unknown team: {home}")
    if away not in stats_lookup:
        raise HTTPException(400, f"Unknown team: {away}")




@app.get("/health")
def health():
    return {"status": "ok", "models_loaded": bool(_state)}


@app.post("/predict")
def predict(req: PredictRequest):
    home = req.home_team.strip()
    away = req.away_team.strip()

    _validate_teams(home, away)

    X = _build_input_row(home, away)

    winner_pred     = _state["model_winner"].predict(X)[0]
    winner_pts_pred = int(round(_state["model_winner_pts"].predict(X)[0]))
    loser_pts_pred  = int(round(_state["model_loser_pts"].predict(X)[0]))

    try:
        proba      = _state["model_winner"].predict_proba(X)[0]
        confidence = round(float(max(proba)) * 100, 1)
    except AttributeError:
        confidence = estimate_confidence_from_margin(winner_pts_pred, loser_pts_pred)

    winner_name = home if winner_pred == 1 else away
    loser_name  = away if winner_pred == 1 else home

    return {
        "winner":        winner_name,
        "winner_points": winner_pts_pred,
        "loser":         loser_name,
        "loser_points":  loser_pts_pred,
        "confidence":    confidence,
        "head_to_head":  get_head_to_head(_state["matchups_df"], home, away),
    }




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("predict_api:app", host="127.0.0.1", port=8000, reload=False)