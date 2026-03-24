


FORM_WINDOW: int = 10  


DEFAULT_SEASONS: list[str] = [
    "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"
]


PER_TEAM_STAT_COLS: list[str] = [
    "TEAM1_FG_PCT",  "TEAM2_FG_PCT",
    "TEAM1_FT_PCT",  "TEAM2_FT_PCT",
    "TEAM1_REB",     "TEAM2_REB",
    "TEAM1_AST",     "TEAM2_AST",
    "TEAM1_PLUS_MINUS", "TEAM2_PLUS_MINUS",
    "TEAM1_FG3_PCT", "TEAM2_FG3_PCT",
    "TEAM1_TOV",     "TEAM2_TOV",
    "TEAM1_STL",     "TEAM2_STL",
    "TEAM1_BLK",     "TEAM2_BLK",
    "TEAM1_FORM",    "TEAM2_FORM",
]

DIFF_STAT_PAIRS: list[tuple[str, str, str]] = [
    ("TEAM1_FG_PCT",     "TEAM2_FG_PCT",     "FG_PCT_DIFF"),
    ("TEAM1_REB",        "TEAM2_REB",         "REB_DIFF"),
    ("TEAM1_AST",        "TEAM2_AST",         "AST_DIFF"),
    ("TEAM1_PLUS_MINUS", "TEAM2_PLUS_MINUS",  "PLUS_MINUS_DIFF"),
    ("TEAM1_FG3_PCT",    "TEAM2_FG3_PCT",     "FG3_PCT_DIFF"),
    ("TEAM1_TOV",        "TEAM2_TOV",         "TOV_DIFF"),
    ("TEAM1_STL",        "TEAM2_STL",         "STL_DIFF"),
    ("TEAM1_BLK",        "TEAM2_BLK",         "BLK_DIFF"),
    ("TEAM1_FORM",       "TEAM2_FORM",        "FORM_DIFF"),
]

DIFF_STAT_COLS: list[str] = [d for _, _, d in DIFF_STAT_PAIRS]

NULLABLE_NUMERIC_COLS: list[str] = [
    "TEAM1_FT_PCT",  "TEAM2_FT_PCT",
    "TEAM1_FG3_PCT", "TEAM2_FG3_PCT",
    "TEAM1_TOV",     "TEAM2_TOV",
    "TEAM1_STL",     "TEAM2_STL",
    "TEAM1_BLK",     "TEAM2_BLK",
    "TEAM1_FORM",    "TEAM2_FORM",
]

OPTIONAL_STAT_COLS: list[str] = [
    "TEAM1_FG3_PCT", "TEAM2_FG3_PCT",
    "TEAM1_TOV",     "TEAM2_TOV",
    "TEAM1_STL",     "TEAM2_STL",
    "TEAM1_BLK",     "TEAM2_BLK",
]

BASE_FEATURES: list[str] = [
    *PER_TEAM_STAT_COLS,
    *DIFF_STAT_COLS,
    "TEAM1_ID", "TEAM2_ID",
    "SEASON_START",
    "TEAM1_WIN", "TEAM1_PTS", "TEAM2_PTS",
]


STAT_COL_SUFFIXES: frozenset[str] = frozenset({
    "PTS", "AST", "REB", "FG_PCT", "FT_PCT", "FG3_PCT",
    "PLUS_MINUS", "WIN", "TOV", "STL", "BLK", "FORM", "ID",
})


GBM_PARAMS: dict = dict(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=4,
    subsample=0.8,
    random_state=42,
)

TOP_FEATURES_TO_PRINT: int = 15
TEST_SIZE: float = 0.2
RANDOM_STATE: int = 42

RAW_DATA_FILENAME      = "ALL_NBA_matchups_2020_2025.csv"
CLEAN_DATA_FILENAME    = "ALL_NBA_matchups_2020_2025_clean_encoded.csv"
AVG_STATS_FILENAME     = "team_average_stats.csv"
TEAM_MAPPING_SUFFIX    = "_team_mapping.csv"

MODEL_WINNER_FILENAME      = "model_winner.pkl"
MODEL_WINNER_PTS_FILENAME  = "model_winner_pts.pkl"
MODEL_LOSER_PTS_FILENAME   = "model_loser_pts.pkl"
FEATURE_COLS_FILENAME      = "feature_columns.json"


HEAD_TO_HEAD_LIMIT: int = 10
CONFIDENCE_MARGIN_OFFSET: float = 10.0
CONFIDENCE_BASE: float = 50.0
CONFIDENCE_RANGE: float = 38.0