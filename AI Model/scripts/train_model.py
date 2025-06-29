import numpy as np
import pandas as pd
import joblib
import json
from xgboost import XGBClassifier, XGBRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, roc_auc_score, mean_absolute_error
from sklearn.utils import class_weight
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import shap



X = pd.read_csv("../data/X_filtered.csv")
y_df = pd.read_csv("../data/y_targets.csv")

y_win = y_df["HomeWin"]
y_home_score = y_df["TEAM1_PTS"]
y_away_score = y_df["TEAM2_PTS"]

full_df = pd.read_csv("../data/merged_full_dataset_imputed.csv")
seasons = full_df["SEASON"].str[:4].astype(int)


train_mask = seasons <= 2020
val_mask = (seasons == 2021)
test_mask = (seasons >= 2022)



X_train = X[train_mask]
X_val = X[val_mask]
X_test = X[test_mask]

y_win_train = y_win[train_mask]
y_win_val = y_win[val_mask]
y_win_test = y_win[test_mask]

y_home_train = y_home_score[train_mask]
y_home_val = y_home_score[val_mask]
y_home_test = y_home_score[test_mask]

y_away_train = y_away_score[train_mask]
y_away_val = y_away_score[val_mask]
y_away_test = y_away_score[test_mask]

print(f"Train size: {X_train.shape}, Val size: {X_val.shape}, Test size: {X_test.shape}")




baseline_clf = LogisticRegression(max_iter=500).fit(X_train, y_win_train)
baseline_home = LinearRegression().fit(X_train, y_home_train)
baseline_away = LinearRegression().fit(X_train, y_away_train)

xgb_clf = XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=4, use_label_encoder=False, eval_metric="logloss")
xgb_home = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4)
xgb_away = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4)

xgb_clf.fit(X_train, y_win_train)
xgb_home.fit(X_train, y_home_train)
xgb_away.fit(X_train, y_away_train)

baseline_acc = accuracy_score(y_win_test, baseline_clf.predict(X_test))
baseline_auc = roc_auc_score(y_win_test, baseline_clf.predict_proba(X_test)[:, 1])
baseline_home_mae = mean_absolute_error(y_home_test, baseline_home.predict(X_test))
baseline_away_mae = mean_absolute_error(y_away_test, baseline_away.predict(X_test))

xgb_acc = accuracy_score(y_win_test, xgb_clf.predict(X_test))
xgb_auc = roc_auc_score(y_win_test, xgb_clf.predict_proba(X_test)[:, 1])
xgb_home_mae = mean_absolute_error(y_home_test, xgb_home.predict(X_test))
xgb_away_mae = mean_absolute_error(y_away_test, xgb_away.predict(X_test))


class_weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_win_train),
    y=y_win_train
)
class_weight_dict = {i : w for i, w in zip(np.unique(y_win_train), class_weights)}
baseline_clf = LogisticRegression(max_iter=500, class_weight=class_weight_dict)

ensemble = VotingClassifier(
    estimators=[
        ('logreg', LogisticRegression(max_iter=500)),
        ('xgb', XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=4, use_label_encoder=False, eval_metric="logloss")),
        ('tree', DecisionTreeClassifier(max_depth=4))
    ],
    voting='soft'
)
ensemble.fit(X_train, y_win_train)

ensemble_acc = accuracy_score(y_win_test, ensemble.predict(X_test))
ensemble_auc = roc_auc_score(y_win_test, ensemble.predict_proba(X_test)[:, 1])

print(f"✅ Ensemble Accuracy: {ensemble_acc:.4f}")
print(f"✅ Ensemble AUC: {ensemble_auc:.4f}")


joblib.dump(xgb_clf, "../models/win_model_clean.pkl")
joblib.dump(xgb_home, "../models/home_score_model_clean.pkl")
joblib.dump(xgb_away, "../models/away_score_model_clean.pkl")
json.dump(list(X.columns), open("../models/features_clean.json", "w"))


metrics = {
    "baseline_accuracy": baseline_acc,
    "baseline_auc": baseline_auc,
    "baseline_home_mae": baseline_home_mae,
    "baseline_away_mae": baseline_away_mae,
    "xgb_accuracy": xgb_acc,
    "xgb_auc": xgb_auc,
    "xgb_home_mae": xgb_home_mae,
    "xgb_away_mae": xgb_away_mae
}
with open("../outputs/metrics_clean.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\n✅ ZAVRŠENO TRENING BEZ LEAKAGE-A")
for key, value in metrics.items():
    print(f"{key}: {value:.4f}")




print("\n📊 Detaljna klasifikacija (XGBoost):")
xgb_preds = xgb_clf.predict(X_test)
print(classification_report(y_win_test, xgb_preds))
explainer = shap.TreeExplainer(xgb_clf)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, feature_names=X_test.columns)