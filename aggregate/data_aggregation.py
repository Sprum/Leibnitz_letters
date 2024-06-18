"""Module for aggregating the extracted data"""
from pathlib import Path
from typing import List
from letter_map import letter_map
from pandas import DataFrame

import pandas as pd


def read_csv(path: Path) -> DataFrame:
    df = pd.read_csv(path)
    return df


def letter_num_to_key(path: Path) -> int:
    try:
        key = int(int(path.stem))
        return key
    except Exception as e:
        print(e)
        return


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

def aggregate_all(csv_paths: List[Path]):
    for csv in csv_paths:
        df = read_csv(csv)
        csvs.append(df)

    all_data = aggregate_data(csvs)
    all_data.to_csv("../data/all.csv")
    print(all_data)
def aggregate_person(csv_paths: List[Path], person: str):
    out_path = "../data/per Person/" + person
    for csv in csv_paths:
        df = read_csv(csv)
        csvs.append(df)

    all_data = aggregate_data(csvs)
    all_data.to_csv(out_path)
    print(all_data)

def exec_aggregate_person(person: str):
    sophies_letters = []
    for csv in csv_paths:
        df = pd.read_csv(csv)
        key = letter_num_to_key(csv)
        absendeort = letter_map[key][1]
        if letter_map[key][0]== person:
            sophies_letters.append(csv)
    aggregate_person(sophies_letters,person)

def place_is_present(df: DataFrame, place: str):
    return place in df["Place"].values



if __name__ == "__main__":
    exec_aggregate_person("Sophie")