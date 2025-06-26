import pandas as pd
import os

def loadClean(csv_path):
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)

    print("Initial data info:")
    print(df.info())

    print("Preview data:")
    print(df.head())

    if 'season' in df.columns:
        print("Season data info:")
        df = df[df['season'] >= 2003]

    print("Missing values per column:")
    print(df.isnull().sum())

    df_clean=df.dropna()
    print("Data info after dropping missing values:")
    print(df_clean.info())

    if __name__ == "__main__":

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


        raw_csv_path = os.path.join(base_dir, 'data', 'nba_all_games.csv')


        cleaned_dir = os.path.join(base_dir, 'data', 'cleaned')


        if not os.path.exists(cleaned_dir):
            os.makedirs(cleaned_dir)

        # Učitaj i očisti podatke
        cleaned_df = loadClean(raw_csv_path)

        # Spremi očišćeni CSV u folder cleaned
        save_path = os.path.join(cleaned_dir, 'nba_cleaned_data.csv')
        cleaned_df.to_csv(save_path, index=False)
        print(f"Cleaned data saved to {save_path}")