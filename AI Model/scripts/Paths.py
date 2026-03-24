
import os

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_AI_MODEL_DIR = os.path.join(_SCRIPTS_DIR, "..")

DATA_DIR: str = os.path.normpath(os.path.join(_AI_MODEL_DIR, "data"))
MODEL_DIR: str = os.path.normpath(os.path.join(_AI_MODEL_DIR, "models"))

os.makedirs(DATA_DIR,  exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


def data_path(filename: str) -> str:

    return os.path.join(DATA_DIR, filename)


def model_path(filename: str) -> str:
    
    return os.path.join(MODEL_DIR, filename)