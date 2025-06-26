import os
import pandas as pd
import re

def load_all_csv(folder_path, game_type, start_season=2003):
    all_dataframes = []
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            match = re.search(r'(\d{4})', file)
            if match:
                season = int(match.group(1))
                if season < start_season:
                    continue
            else:
                continue

            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path, low_memory=False)
            df['season'] = season
            df['game_type'] = game_type
            all_dataframes.append(df)

    if all_dataframes:
        return pd.concat(all_dataframes, ignore_index=True)
    else:
        return pd.DataFrame()

regular_season_folder = r"C:\Users\tarik\Desktop\nba score predictor\backend\data\regular season csv"

regular_season_df = load_all_csv(regular_season_folder, 'Regular Season')

output_folder = r"C:\Users\tarik\Desktop\nba score predictor\backend\data"
os.makedirs(output_folder, exist_ok=True)

output_csv = os.path.join(output_folder, "nba_regular_all.csv")
regular_season_df.to_csv(output_csv, index=False)

print(f"Loaded and saved {len(regular_season_df)} regular season games to {output_csv}")
