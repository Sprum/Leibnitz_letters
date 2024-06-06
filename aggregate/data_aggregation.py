"""Module for aggregating the extracted data"""
from pathlib import Path
from typing import List

from pandas import DataFrame

import pandas as pd


def read_csv(path: str) -> DataFrame:
    df = pd.read_csv(path)
    return df


# Read in data
csv_paths = [path for path in Path("../data/per letter").iterdir()]
csvs = []


def aggregate_data(csvs: List[DataFrame]):
    """Function to aggregate all the data from a given list of DataFrames to one DataFrame, summing up all Counts for
    unique places"""
    # Concatenate all DataFrames
    all_data = pd.concat(csvs)
    # Sum up all counts by index (Place)
    all_data = all_data.groupby("Place").sum().reset_index()
    return all_data


if __name__ == "__main__":
    for csv in csv_paths:
        df = read_csv(csv)
        csvs.append(df)

    all_data = aggregate_data(csvs)
    all_data.to_csv("../data/all.csv")
    print(all_data)
