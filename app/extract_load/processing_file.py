import pandas as pd
from datetime import datetime

class ProcessFile:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def read_parquet(self):
        dfs = []
        for path in self.file_paths:
            try:
                print(f"Reading {path}...")
                df = pd.read_parquet(path)
                dfs.append(df)
                print(f"{path} read successfully.")
            except Exception as e:
                raise RuntimeError(f"Failed to read {path}: {e}") from e
        return pd.concat(dfs, ignore_index=True)

    def filter_first_day_each_month(self, df, date_column):
        if date_column not in df.columns:
            raise ValueError(f"Column {date_column} not found in DataFrame")
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        filtered_df = df[df[date_column].dt.day == 1]
        return filtered_df
