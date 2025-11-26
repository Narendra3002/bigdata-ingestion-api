import pandas as pd

def basic_cleanup(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1) Drop completely empty rows
    df.dropna(how="all", inplace=True)

    # 2) Strip spaces from string columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()

    # 3) Remove exact duplicate rows
    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    print(f"Removed {before - after} duplicate rows")

    return df
