import pandas as pd
import os


def process_features(input_path, output_path):

    print("Starting feature engineering...")

    chunk_iter = pd.read_csv(input_path, chunksize=10000, low_memory=False)
    processed_chunks = []

    for i, chunk in enumerate(chunk_iter):
        print(f"Processing chunk {i + 1}...")


        if 'MATCHUP' in chunk.columns:
            chunk['is_home_team'] = chunk['MATCHUP'].apply(lambda x: 1 if 'vs.' in str(x) else 0)


        if 'PTS' in chunk.columns and 'PLUS_MINUS' in chunk.columns:
            chunk['point_diff'] = chunk['PTS'] - chunk['PLUS_MINUS']


        if 'GAME_DATE' in chunk.columns:
            chunk['season_month'] = pd.to_datetime(chunk['GAME_DATE'], errors='coerce').dt.month

        processed_chunks.append(chunk)


    final_df = pd.concat(processed_chunks, ignore_index=True)
    print("Feature engineering completed.")


    final_df.to_csv(output_path, index=False)
    print(f"Feature engineered data saved to {output_path}")


if __name__ == "__main__":

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


    input_file = os.path.join(base_dir, 'data', 'cleaned', 'nba_cleaned_data.csv')


    output_dir = os.path.join(base_dir, 'data', 'features')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, 'nba_features_data.csv')


    process_features(input_file, output_file)
