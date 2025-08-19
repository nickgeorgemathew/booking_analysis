import pandas as pd
from pathlib import Path

def load_csv(path:str|Path)->pd.DataFrame:
    return pd.read_csv(path)
