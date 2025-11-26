import os
import pandas as pd
import dask.dataframe as dd
import numpy as np
import csv
from api.database import SessionLocal
from api.models import MasterData
from .schema_normalizer import normalize_dataframe
from .cleaning import basic_cleanup


def clean_nans(df: pd.DataFrame) -> pd.DataFrame:
    """Convert all NaN/NaT values to None so JSON is valid."""
    df = df.copy()

    # Convert to object so None is allowed everywhere
    df = df.astype(object)

    # Replace pandas NaN/NaT with None
    df = df.where(pd.notnull(df), None)

    return df


def save_to_db(df, source_file: str, chunk_size: int = 1000):
    """Save a pandas or Dask dataframe into master_data in chunks."""
    db = SessionLocal()
    try:
        # If it's a Dask dataframe, compute to pandas
        if not isinstance(df, pd.DataFrame):
            df = df.compute()

        # Make JSON-safe (no NaN, only None)
        df = clean_nans(df)

        records = df.to_dict(orient="records")
        total = len(records)
        print(f"Preparing to insert {total} rows from {source_file}")

        for start in range(0, total, chunk_size):
            end = start + chunk_size
            batch = records[start:end]

            objs = [
                MasterData(
                    source_file=source_file,
                    raw_data=row,
                    normalized_data=row,
                )
                for row in batch
            ]

            db.bulk_save_objects(objs)
            db.commit()
            print(f"Inserted rows {start}-{min(end, total)}")

        print(f"✅ Finished inserting {total} rows from {source_file}")

    except Exception as e:
        print("DB Insert Error:", e)
        raise

    finally:
        db.close()


def ingest_file(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    print(f"\n🔍 Processing file: {file_path}")
    print(f"Detected type: {ext}")

    # ---------- TSV ----------
    if ext == ".tsv":
        df = pd.read_csv(file_path, sep="\t", low_memory=False)
        df = normalize_dataframe(df)
        df = basic_cleanup(df)
        save_to_db(df, file_path)
        return df

    # ---------- CSV ----------
    elif ext == ".csv":
        file_size = os.path.getsize(file_path)
        print("File size:", file_size, "bytes")

        # Large file → Dask, partitioned
        if file_size > 500 * 1024 * 1024:
            print("Using Dask for large CSV ingestion (partitioned)...")
            ddf = dd.read_csv(
    file_path,
    dtype=str,
    assume_missing=True,
    sep=",",
    engine="python",          # more tolerant parser
    on_bad_lines="skip",      # ✅ skip malformed rows
    quoting=csv.QUOTE_MINIMAL
)


            n_partitions = ddf.npartitions
            print(f"Dask partitions: {n_partitions}")

            for i in range(n_partitions):
                print(f"\n🔹 Processing partition {i+1}/{n_partitions}")
                part = ddf.get_partition(i).compute()  # only this chunk in RAM

                part = normalize_dataframe(part)
                part = basic_cleanup(part)
                save_to_db(part, file_path)

            print(f"✅ Finished all partitions for {file_path}")
            return None

        # Small/medium CSV → pandas
        else:
            df = pd.read_csv(file_path, low_memory=False)
            df = normalize_dataframe(df)
            df = basic_cleanup(df)
            save_to_db(df, file_path)
            return df

    # ---------- Excel ----------
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path, engine="openpyxl")
        df = normalize_dataframe(df)
        df = basic_cleanup(df)
        save_to_db(df, file_path)
        return df

    else:
        print("❌ Unsupported file type:", ext)
        return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m ingestion.ingest_all <file_path>")
    else:
        ingest_file(sys.argv[1])
