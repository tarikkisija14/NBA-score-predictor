import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os


def clean_and_enhance_data(input_csv_path: str, output_csv_path: str):

    df = pd.read_csv(input_csv_path)


    numeric_cols = [
        'TEAM1_FT_PCT', 'TEAM2_FT_PCT',
        'TEAM1_FG3_PCT', 'TEAM2_FG3_PCT',
        'TEAM1_TOV', 'TEAM2_TOV',
        'TEAM1_STL', 'TEAM2_STL',
        'TEAM1_BLK', 'TEAM2_BLK',
        'TEAM1_FORM', 'TEAM2_FORM',
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())


    if 'TEAM1_WIN' not in df.columns:
        df['TEAM1_WIN'] = (df['TEAM1_PTS'] > df['TEAM2_PTS']).astype(int)


    df['FG_PCT_DIFF']   = df['TEAM1_FG_PCT']   - df['TEAM2_FG_PCT']
    df['REB_DIFF']      = df['TEAM1_REB']       - df['TEAM2_REB']
    df['AST_DIFF']      = df['TEAM1_AST']       - df['TEAM2_AST']
    df['PLUS_MINUS_DIFF'] = df['TEAM1_PLUS_MINUS'] - df['TEAM2_PLUS_MINUS']


    if 'TEAM1_FG3_PCT' in df.columns:
        df['FG3_PCT_DIFF'] = df['TEAM1_FG3_PCT'] - df['TEAM2_FG3_PCT']
    if 'TEAM1_TOV' in df.columns:
        df['TOV_DIFF']  = df['TEAM1_TOV']  - df['TEAM2_TOV']   # negative = better
    if 'TEAM1_STL' in df.columns:
        df['STL_DIFF']  = df['TEAM1_STL']  - df['TEAM2_STL']
    if 'TEAM1_BLK' in df.columns:
        df['BLK_DIFF']  = df['TEAM1_BLK']  - df['TEAM2_BLK']
    if 'TEAM1_FORM' in df.columns:
        df['FORM_DIFF'] = df['TEAM1_FORM'] - df['TEAM2_FORM']


    if 'SEASON' in df.columns:
        df['SEASON_START'] = df['SEASON'].str[:4].astype(int)


    le = LabelEncoder()
    all_teams = pd.concat([df['TEAM1_NAME'], df['TEAM2_NAME']]).unique()
    le.fit(all_teams)

    df['TEAM1_ID'] = le.transform(df['TEAM1_NAME'])
    df['TEAM2_ID'] = le.transform(df['TEAM2_NAME'])


    df['WINNER']     = df['TEAM1_WIN']
    df['WINNER_PTS'] = df.apply(
        lambda r: r['TEAM1_PTS'] if r['WINNER'] == 1 else r['TEAM2_PTS'], axis=1)
    df['LOSER_PTS']  = df.apply(
        lambda r: r['TEAM2_PTS'] if r['WINNER'] == 1 else r['TEAM1_PTS'], axis=1)


    base_features = [

        'TEAM1_FG_PCT', 'TEAM2_FG_PCT',
        'TEAM1_FT_PCT', 'TEAM2_FT_PCT',
        'TEAM1_REB',    'TEAM2_REB',
        'TEAM1_AST',    'TEAM2_AST',
        'TEAM1_PLUS_MINUS', 'TEAM2_PLUS_MINUS',


        'TEAM1_FG3_PCT', 'TEAM2_FG3_PCT',
        'TEAM1_TOV',     'TEAM2_TOV',
        'TEAM1_STL',     'TEAM2_STL',
        'TEAM1_BLK',     'TEAM2_BLK',
        'TEAM1_FORM',    'TEAM2_FORM',


        'FG_PCT_DIFF', 'REB_DIFF', 'AST_DIFF', 'PLUS_MINUS_DIFF',
        'FG3_PCT_DIFF', 'TOV_DIFF', 'STL_DIFF', 'BLK_DIFF', 'FORM_DIFF',


        'TEAM1_ID', 'TEAM2_ID',
        'SEASON_START',
        'TEAM1_WIN', 'TEAM1_PTS', 'TEAM2_PTS',
    ]


    final_cols = [c for c in base_features if c in df.columns]
    final_cols += ['WINNER', 'WINNER_PTS', 'LOSER_PTS']

    df_final = df[final_cols]


    team_mapping = pd.DataFrame({
        'team_id':   le.transform(le.classes_),
        'team_name': le.classes_
    })
    team_mapping.to_csv(
        output_csv_path.replace('.csv', '_team_mapping.csv'), index=False)

    df_final.to_csv(output_csv_path, index=False)
    print(f"Podaci spremljeni u: {output_csv_path}")
    print(f"Broj kolona: {len(df_final.columns)}")
    print(f"Kolone: {list(df_final.columns)}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '..', 'data')

    input_path  = os.path.join(data_dir, 'ALL_NBA_matchups_2020_2025.csv')
    output_path = os.path.join(data_dir, 'ALL_NBA_matchups_2020_2025_clean_encoded.csv')

    clean_and_enhance_data(input_path, output_path)