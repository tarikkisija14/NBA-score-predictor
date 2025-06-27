import pandas as pd
from sklearn.model_selection import train_test_split

input_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/match_dataset_encoded_scaled.csv"
train_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/train.csv"
test_path = r"C:/Users/tarik/Desktop/nba score predictor/AI Model/data/test.csv"

df = pd.read_csv(input_path)

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

print("Train:", len(train_df))
print("Test:", len(test_df))

train_df.to_csv(train_path, index=False)
test_df.to_csv(test_path, index=False)
print("Train i test setovi spremljeni.")
