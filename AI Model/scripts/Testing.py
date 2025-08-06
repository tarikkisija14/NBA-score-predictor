import pandas as pd
import matplotlib.pyplot as plt

filepath = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025.csv"
df = pd.read_csv(filepath)
clean_encoded_path = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025_clean_encoded.csv"
df_clean = pd.read_csv(clean_encoded_path)

print("Dimenzije dataset-a:", df_clean.shape)
print("\nTipovi podataka po kolonama:")
print(df.dtypes)


print("Tipovi podataka po kolonama:")
for col in df.columns:
    print(f"{col}: {df[col].dtype}")

print("Broj NaN vrijednosti po kolonama:")
print(df.isna().sum())

print("\nStatistika numerickih kolona grupiranih po pobjedi TEAM1:")
print(df.groupby('TEAM1_WIN').describe())

print("------------------------------------------\n")

print("Dimenzije dataset-a:", df_clean.shape)
print("\nTipovi podataka po kolonama:")
print(df_clean.dtypes)

print("\nBroj NaN vrijednosti po kolonama:")
print(df_clean.isna().sum())

print("Tipovi podataka po kolonama:")
for col in df_clean.columns:
    print(f"{col}: {df_clean[col].dtype}")

print("------------------------------------------\n")

print("Kolone u datasetu:")
for col in df_clean.columns:
    print(col)

    
