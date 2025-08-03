import pandas as pd
import matplotlib.pyplot as plt

filepath = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025.csv"
df = pd.read_csv(filepath)
clean_encoded_path = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025_clean_encoded.csv"
df_clean = pd.read_csv(clean_encoded_path)

print("Tipovi podataka po kolonama:")
for col in df.columns:
    print(f"{col}: {df[col].dtype}")

print("Broj NaN vrijednosti po kolonama:")
print(df.isna().sum())

print("\nStatistika numeričkih kolona grupiranih po pobjedi TEAM1:")
print(df.groupby('TEAM1_WIN').describe())

print("------------------------------------------\n")

print("Dimenzije dataset-a:", df_clean.shape)
print("\nTipovi podataka po kolonama:")
print(df_clean.dtypes)

print("\nBroj NaN vrijednosti po kolonama:")
print(df_clean.isna().sum())

print("\nDeskriptivna statistika:")
print(df_clean.describe())

print("\nDistribucija vrijednosti 'TEAM1_WIN':")
print(df_clean['TEAM1_WIN'].value_counts(normalize=True))
