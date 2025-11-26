import re
import pandas as pd

def normalize_column_name(col: str) -> str:
    """Convert messy column names into a clean standard format."""
    col = col.strip().lower()              # lowercase
    col = col.replace(" ", "_")            # spaces -> underscore
    col = re.sub(r"[^a-z0-9_]", "", col)   # remove special chars
    col = re.sub(r"_+", "_", col)          # reduce multiple _ to single
    return col

def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply normalization to all column names."""
    df = df.copy()
    df.columns = [normalize_column_name(c) for c in df.columns]
    return df
