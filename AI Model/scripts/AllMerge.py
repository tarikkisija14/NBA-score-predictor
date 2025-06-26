import pandas as pd
import os

chunk_size = 1_000_000
data_folder = r"C:\Users\tarik\Desktop\nba score predictor\backend\data"

regular_path = os.path.join(data_folder, "nba_regular_all.csv")
playoff_path = os.path.join(data_folder, "nba_playoff_all.csv")
output_path = os.path.join(data_folder, "nba_all_games.csv")

# Prvo očitavanje zaglavlja i zajedničkih kolona
regular_cols = pd.read_csv(regular_path, nrows=0).columns.tolist()
playoff_cols = pd.read_csv(playoff_path, nrows=0).columns.tolist()

common_columns = list(set(regular_cols).intersection(set(playoff_cols)))

print(f"Common columns: {common_columns}")

# Funkcija za stream čitanje i pisanje
def stream_csv_to_output(input_path, output_path, columns, write_header):
    reader = pd.read_csv(input_path, usecols=columns, chunksize=chunk_size)
    for i, chunk in enumerate(reader):
        mode = 'w' if write_header and i == 0 else 'a'  # piši header samo prvi put
        chunk.to_csv(output_path, mode=mode, header=(mode=='w'), index=False)
        print(f"Procesirano {len(chunk)} redova iz {input_path}")

# Prvo upiši regular season
stream_csv_to_output(regular_path, output_path, common_columns, write_header=True)
# Nakon toga dodaj playoff podatke
stream_csv_to_output(playoff_path, output_path, common_columns, write_header=False)

print(f"\n✅ Spojeni podaci spremljeni u {output_path}")
