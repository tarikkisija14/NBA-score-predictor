import pandas as pd

def clean_and_encode_data(input_csv_path: str, output_csv_path: str):
    df = pd.read_csv(input_csv_path)


    df = df.dropna(subset=['TEAM1_NAME', 'TEAM2_NAME'])


    median_ft_pct = df['TEAM2_FT_PCT'].median()
    df['TEAM2_FT_PCT'] = df['TEAM2_FT_PCT'].fillna(median_ft_pct)


    df['SEASON_START'] = df['SEASON'].str[:4].astype(int)


    team1_dummies = pd.get_dummies(df['TEAM1_NAME'], prefix='TEAM1')
    team2_dummies = pd.get_dummies(df['TEAM2_NAME'], prefix='TEAM2')


    df = pd.concat([df, team1_dummies, team2_dummies], axis=1)


    df_clean = df.drop(columns=['GAME_ID', 'SEASON', 'TEAM1_NAME', 'TEAM2_NAME'])


    df_clean.to_csv(output_csv_path, index=False)
    print(f" Ocisceni i encodirani podaci spremljeni u : {output_csv_path}")


input_path = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025.csv"
output_path = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025_clean_encoded.csv"

clean_and_encode_data(input_path, output_path)
