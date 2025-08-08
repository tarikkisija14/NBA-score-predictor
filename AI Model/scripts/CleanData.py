import pandas as pd
from sklearn.preprocessing import LabelEncoder


def clean_and_enhance_data(input_csv_path: str, output_csv_path: str):

    df = pd.read_csv(input_csv_path)



    median_ft_pct = df['TEAM2_FT_PCT'].median()
    df['TEAM2_FT_PCT'] = df['TEAM2_FT_PCT'].fillna(median_ft_pct)


    if 'TEAM1_WIN' not in df.columns:
        df['TEAM1_WIN'] = (df['TEAM1_PTS'] > df['TEAM2_PTS']).astype(int)


    df['FG_PCT_DIFF'] = df['TEAM1_FG_PCT'] - df['TEAM2_FG_PCT']
    df['REB_DIFF'] = df['TEAM1_REB'] - df['TEAM2_REB']
    df['AST_DIFF'] = df['TEAM1_AST'] - df['TEAM2_AST']
    df['PLUS_MINUS_DIFF'] = df['TEAM1_PLUS_MINUS'] - df['TEAM2_PLUS_MINUS']


    le = LabelEncoder()
    all_teams = pd.concat([df['TEAM1_NAME'], df['TEAM2_NAME']]).unique()
    le.fit(all_teams)

    df['TEAM1_ID'] = le.transform(df['TEAM1_NAME'])
    df['TEAM2_ID'] = le.transform(df['TEAM2_NAME'])


    essential_features = [

        'FG_PCT_DIFF', 'REB_DIFF', 'AST_DIFF', 'PLUS_MINUS_DIFF',

        'TEAM1_FG_PCT', 'TEAM2_FG_PCT',
        'TEAM1_FT_PCT', 'TEAM2_FT_PCT',
        'TEAM1_REB', 'TEAM2_REB',
        'TEAM1_AST', 'TEAM2_AST',
        'TEAM1_PLUS_MINUS', 'TEAM2_PLUS_MINUS',

        'TEAM1_ID', 'TEAM2_ID',

        'TEAM1_WIN', 'TEAM1_PTS', 'TEAM2_PTS'
    ]


    df['WINNER'] = df['TEAM1_WIN']
    df['WINNER_PTS'] = df.apply(lambda row: row['TEAM1_PTS'] if row['WINNER'] == 1 else row['TEAM2_PTS'], axis=1)
    df['LOSER_PTS'] = df.apply(lambda row: row['TEAM2_PTS'] if row['WINNER'] == 1 else row['TEAM1_PTS'], axis=1)


    final_columns = essential_features + ['WINNER', 'WINNER_PTS', 'LOSER_PTS']
    df_final = df[final_columns]


    team_mapping = pd.DataFrame({
        'team_id': le.transform(le.classes_),
        'team_name': le.classes_
    })
    team_mapping.to_csv(output_csv_path.replace('.csv', '_team_mapping.csv'), index=False)


    df_final.to_csv(output_csv_path, index=False)
    print(f"Poboljšani podaci spremljeni u: {output_csv_path}")
    print(f"Broj kolona: {len(df_final.columns)} (original: {len(df.columns)})")
    print(f"Primjer kolona: {list(df_final.columns[:10])}")


# Pokretanje
input_path = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025.csv"
output_path = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025_enhanced.csv"

clean_and_enhance_data(input_path, output_path)