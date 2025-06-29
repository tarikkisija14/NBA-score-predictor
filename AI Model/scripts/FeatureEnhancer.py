import pandas as pd

# Učitaj dataset
df = pd.read_csv("../data/merged_full_dataset_imputed.csv")

# Funkcija za rolling prosjek (pomjeren za 1 da se izbjegne leakage)
def rolling_stats(series, n):
    return series.rolling(window=n, min_periods=1).mean().shift(1)

# Lista kolona koje želiš obraditi
rolling_cols = ["HOME_PTS_x", "AWAY_PTS_x", "HOME_OPP_PTS_x", "AWAY_OPP_PTS_x"]

# Provjera koje kolone postoje
existing_cols = [col for col in rolling_cols if col in df.columns]
print(f"✅ Postojeće kolone za rolling: {existing_cols}")

# Generiši rolling feature-e
for col in existing_cols:
    df[f"{col}_ROLL_3"] = (
        df.groupby(df["HOME_TEAM_NAME"])[col].transform(lambda g: rolling_stats(g, 3))
    )

# Sačuvaj poboljšani dataset
df.to_csv("../data/merged_enhanced.csv", index=False)
print("✅ FeatureEnhancer: Dataset spremljen u merged_enhanced.csv")
