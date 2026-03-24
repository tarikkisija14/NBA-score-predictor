
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from Constants import (
    NULLABLE_NUMERIC_COLS,
    DIFF_STAT_PAIRS,
    BASE_FEATURES,
    TEAM_MAPPING_SUFFIX,
)
from Paths import data_path
from Constants import RAW_DATA_FILENAME, CLEAN_DATA_FILENAME




def _fill_nullable_columns(df: pd.DataFrame) -> None:

    for col in NULLABLE_NUMERIC_COLS:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())


def _add_win_column(df: pd.DataFrame) -> None:

    if "TEAM1_WIN" not in df.columns:
        df["TEAM1_WIN"] = (df["TEAM1_PTS"] > df["TEAM2_PTS"]).astype(int)


def _add_diff_columns(df: pd.DataFrame) -> None:

    for col1, col2, diff_col in DIFF_STAT_PAIRS:
        if col1 in df.columns and col2 in df.columns:
            df[diff_col] = df[col1] - df[col2]


def _add_season_start_column(df: pd.DataFrame) -> None:

    if "SEASON" in df.columns:
        df["SEASON_START"] = df["SEASON"].str[:4].astype(int)


def _encode_teams(df: pd.DataFrame) -> LabelEncoder:

    encoder = LabelEncoder()
    all_teams = pd.concat([df["TEAM1_NAME"], df["TEAM2_NAME"]]).unique()
    encoder.fit(all_teams)
    df["TEAM1_ID"] = encoder.transform(df["TEAM1_NAME"])
    df["TEAM2_ID"] = encoder.transform(df["TEAM2_NAME"])
    return encoder


def _add_outcome_columns(df: pd.DataFrame) -> None:

    df["WINNER"] = df["TEAM1_WIN"]
    df["WINNER_PTS"] = df.apply(
        lambda r: r["TEAM1_PTS"] if r["WINNER"] == 1 else r["TEAM2_PTS"], axis=1
    )
    df["LOSER_PTS"] = df.apply(
        lambda r: r["TEAM2_PTS"] if r["WINNER"] == 1 else r["TEAM1_PTS"], axis=1
    )


def _save_team_mapping(encoder: LabelEncoder, output_csv_path: str) -> None:

    mapping = pd.DataFrame({
        "team_id":   encoder.transform(encoder.classes_),
        "team_name": encoder.classes_,
    })
    mapping_path = output_csv_path.replace(".csv", TEAM_MAPPING_SUFFIX)
    mapping.to_csv(mapping_path, index=False)




def clean_and_enhance_data(input_csv_path: str, output_csv_path: str) -> None:

    df = pd.read_csv(input_csv_path)

    _fill_nullable_columns(df)
    _add_win_column(df)
    _add_diff_columns(df)
    _add_season_start_column(df)

    encoder = _encode_teams(df)
    _add_outcome_columns(df)

    output_cols = [c for c in BASE_FEATURES if c in df.columns]
    output_cols += ["WINNER", "WINNER_PTS", "LOSER_PTS"]
    df_clean = df[output_cols]

    _save_team_mapping(encoder, output_csv_path)
    df_clean.to_csv(output_csv_path, index=False)

    print(f"Data saved to: {output_csv_path}")
    print(f"Column count:  {len(df_clean.columns)}")
    print(f"Columns:       {list(df_clean.columns)}")




if __name__ == "__main__":
    clean_and_enhance_data(
        input_csv_path=data_path(RAW_DATA_FILENAME),
        output_csv_path=data_path(CLEAN_DATA_FILENAME),
    )