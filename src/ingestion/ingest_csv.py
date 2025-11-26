import pandas as pd
from .schema_normalizer import normalize_dataframe
from .cleaning import basic_cleanup

def ingest_csv(file_path: str):
    try:
        df = pd.read_csv(file_path, low_memory=False)
        print("CSV Loaded Successfully!")
        print("Raw rows:", len(df))

        # Normalize columns
        df = normalize_dataframe(df)
        print("Normalized Columns:", list(df.columns))

        # Basic cleanup
        df = basic_cleanup(df)
        print("Cleaned rows:", len(df))

        return df

    except Exception as e:
        print("Error reading CSV:", e)
        return None
