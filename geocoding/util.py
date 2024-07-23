"""Module for utility like joining and formatting to raw lat long tables"""
from pathlib import Path
from typing import List

import pandas as pd
from pandas import DataFrame


def join_coordinate_tables(paths: List[Path]) -> DataFrame:
    dfs = []
    for path in paths:
        df = pd.read_csv(path)
        dfs.append(df)
    all = pd.concat(dfs)
    return all

def rename_column(df, old_name, new_name):
    df = df.rename(columns={old_name: new_name})
    return df


if __name__ == '__main__':
    paths = [path for path in Path("./coded").iterdir() if path.suffix == ".csv"]
    all = join_coordinate_tables(paths)
    cols_to_keep = ['original_Place', 'lat','lon','attribution','attribution_license','attribution_url']
    all_cleaned = all.filter(cols_to_keep)
    all_cleaned = rename_column(all_cleaned, 'original_Place', 'Place')
    all_cleaned.to_csv("./coordinates.csv", index=False)