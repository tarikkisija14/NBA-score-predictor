import pandas as pd
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier

X = pd.read_csv("../data/X_filtered.csv")
y = pd.read_csv("../data/y_targets.csv")["HomeWin"]

params = {
    'n_estimators': [100, 300],
    'max_depth': [3, 5],
    'learning_rate': [0.01, 0.05, 0.1],
}

grid = GridSearchCV(
    XGBClassifier(use_label_encoder=False, eval_metric="logloss"),
    param_grid=params,
    scoring="roc_auc",
    cv=3,
    verbose=2,
    n_jobs=-1
)

grid.fit(X, y)

print("✅ Najbolji parametri:", grid.best_params_)
