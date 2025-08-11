import pandas as pd


csvPath = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\ALL_NBA_matchups_2020_2025_clean_encoded.csv"

df = pd.read_csv(csvPath)


team1_onehot_cols = [col for col in df.columns if col.startswith('TEAM1_') and not col.startswith('TEAM1_AST') and not col.startswith('TEAM1_REB') and not col.startswith('TEAM1_FG_PCT') and not col.startswith('TEAM1_FT_PCT') and not col.startswith('TEAM1_PLUS_MINUS')]
team2_onehot_cols = [col for col in df.columns if col.startswith('TEAM2_') and not col.startswith('TEAM2_AST') and not col.startswith('TEAM2_REB') and not col.startswith('TEAM2_FG_PCT') and not col.startswith('TEAM2_FT_PCT') and not col.startswith('TEAM2_PLUS_MINUS')]


def get_team_name(row, prefix_cols, prefix):
    for col in prefix_cols:
        if row[col] == 1:
            return col.replace(prefix, '')
    return None


df['TEAM1_NAME'] = df.apply(lambda row: get_team_name(row, team1_onehot_cols, 'TEAM1_'), axis=1)
df['TEAM2_NAME'] = df.apply(lambda row: get_team_name(row, team2_onehot_cols, 'TEAM2_'), axis=1)


stat_cols = ['AST', 'REB', 'FG_PCT', 'FT_PCT', 'PLUS_MINUS']


team1_stats = df[[f'TEAM1_{stat}' for stat in stat_cols]].copy()
team1_stats.columns = stat_cols
team1_stats['TEAM'] = df['TEAM1_NAME']

team2_stats = df[[f'TEAM2_{stat}' for stat in stat_cols]].copy()
team2_stats.columns = stat_cols
team2_stats['TEAM'] = df['TEAM2_NAME']


all_stats = pd.concat([team1_stats, team2_stats], ignore_index=True)
avg_stats = all_stats.groupby('TEAM').mean().reset_index()


output_path = r"C:\Users\tarik\Desktop\nba score predictor\AI Model\data\team_average_stats.csv"
avg_stats.to_csv(output_path, index=False)

print(f"Prosjecne statistike po timu spremljene u {output_path}")
