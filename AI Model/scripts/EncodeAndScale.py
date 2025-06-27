import pandas as pd
from sklearn.preprocessing import StandardScaler

input_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/match_dataset.csv"
output_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/match_dataset_encoded_scaled.csv"

df = pd.read_csv(input_path)


categorical_cols = [col for col in df.columns if "TEAM_ABBREVIATION" in col]
df = pd.get_dummies(df, columns=categorical_cols)


numeric_cols = [col for col in df.columns if df[col].dtype != "object" and "TARGET" not in col]
scaler = StandardScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

df.to_csv(output_path, index=False)
print(f"Spremljeno u {output_path}")
