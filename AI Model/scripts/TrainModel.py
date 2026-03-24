
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, accuracy_score

from Constants import (
    PER_TEAM_STAT_COLS,
    DIFF_STAT_COLS,
    STAT_COL_SUFFIXES,
    GBM_PARAMS,
    TOP_FEATURES_TO_PRINT,
    TEST_SIZE,
    RANDOM_STATE,
    CLEAN_DATA_FILENAME,
    MODEL_WINNER_FILENAME,
    MODEL_WINNER_PTS_FILENAME,
    MODEL_LOSER_PTS_FILENAME,
    FEATURE_COLS_FILENAME,
)
from Paths import data_path, model_path


# ---------------------------------------------------------------------------
# Feature selection helpers
# ---------------------------------------------------------------------------

def _get_team_indicator_cols(df: pd.DataFrame) -> list[str]:
    """Return one-hot team-indicator columns (TEAM1_<Name>, TEAM2_<Name>)."""
    return [
        col for col in df.columns
        if (col.startswith("TEAM1_") or col.startswith("TEAM2_"))
        and not any(suffix in col for suffix in STAT_COL_SUFFIXES)
    ]


def _build_feature_cols(df: pd.DataFrame) -> list[str]:
    """Assemble the ordered list of feature columns that exist in *df*."""
    season_cols = ["SEASON_START"] if "SEASON_START" in df.columns else []
    candidates = (
        PER_TEAM_STAT_COLS
        + DIFF_STAT_COLS
        + season_cols
        + _get_team_indicator_cols(df)
    )
    return [c for c in candidates if c in df.columns]




def _train_winner_classifier(X_train, y_train, X_test, y_test, X_all, y_all):
    model = GradientBoostingClassifier(**GBM_PARAMS)
    model.fit(X_train, y_train)

    accuracy  = accuracy_score(y_test, model.predict(X_test))
    cv_scores = cross_val_score(model, X_all, y_all, cv=5, scoring="accuracy")
    print(f"  Test accuracy:  {accuracy:.4f}")
    print(f"  CV accuracy:    {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    return model


def _train_score_regressor(X_train, y_train, X_test, y_test, label: str):
    model = GradientBoostingRegressor(**GBM_PARAMS)
    model.fit(X_train, y_train)

    rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
    print(f"  RMSE {label}: {rmse:.3f}")
    return model


def _print_top_features(model, feature_cols: list[str]) -> None:
    importances = model.feature_importances_
    top_indices = np.argsort(importances)[::-1][:TOP_FEATURES_TO_PRINT]
    print(f"\nTop {TOP_FEATURES_TO_PRINT} features:")
    for i in top_indices:
        print(f"  {feature_cols[i]:<35} {importances[i]:.4f}")



def main() -> None:
    df = pd.read_csv(data_path(CLEAN_DATA_FILENAME))
    print(f"Loaded {len(df)} games, {len(df.columns)} columns")

    feature_cols = _build_feature_cols(df)
    print(f"Feature columns ({len(feature_cols)}): {feature_cols[:15]} ...")

    X            = df[feature_cols]
    y_winner     = df["WINNER"]
    y_winner_pts = df["WINNER_PTS"]
    y_loser_pts  = df["LOSER_PTS"]

    (X_train, X_test,
     y_train_win,  y_test_win,
     y_train_wpts, y_test_wpts,
     y_train_lpts, y_test_lpts) = train_test_split(
        X, y_winner, y_winner_pts, y_loser_pts,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    print("\nTraining winner classifier (GradientBoostingClassifier)...")
    model_winner = _train_winner_classifier(
        X_train, y_train_win, X_test, y_test_win, X, y_winner
    )

    print("\nTraining winner-score regressor (GradientBoostingRegressor)...")
    model_winner_pts = _train_score_regressor(
        X_train, y_train_wpts, X_test, y_test_wpts, "winner points"
    )

    print("\nTraining loser-score regressor (GradientBoostingRegressor)...")
    model_loser_pts = _train_score_regressor(
        X_train, y_train_lpts, X_test, y_test_lpts, "loser points"
    )

    _print_top_features(model_winner, feature_cols)

    joblib.dump(model_winner,     model_path(MODEL_WINNER_FILENAME))
    joblib.dump(model_winner_pts, model_path(MODEL_WINNER_PTS_FILENAME))
    joblib.dump(model_loser_pts,  model_path(MODEL_LOSER_PTS_FILENAME))

    with open(model_path(FEATURE_COLS_FILENAME), "w") as f:
        json.dump(feature_cols, f, indent=2)

    print(f"\nModels saved to: {model_path('')}")
    print("Done!")


if __name__ == "__main__":
    main()