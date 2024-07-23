"""Module for aggregating the extracted data"""
from pathlib import Path
from typing import List
from aggregate.letter_map import letter_map, year_set
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


def aggregate_data(csvs: List[DataFrame]) -> DataFrame:
    """Function to aggregate all the data from a given list of DataFrames to one DataFrame, summing up all Counts for
    unique places"""
    # Concatenate all DataFrames
    all_data = pd.concat(csvs)
    # Sum up all counts by index (Place)
    all_data = all_data.groupby("Place").sum().reset_index()
    return all_data


def aggregate_all(csv_paths: List[Path], out_path: str):
    csvs = []
    for csv in csv_paths:
        df = read_csv(csv)
        csvs.append(df)

    all_data = aggregate_data(csvs)
    all_data.to_csv(out_path, index=False)


def aggregate_person(csv_paths: List[Path], person: str):
    csvs = [read_csv(csv) for csv in csv_paths]
    all_data = aggregate_data(csvs)
    out_path = f"../data/per Person/{person}.csv"
    all_data.to_csv(out_path, index=False)


def exec_aggregate_person(person: str):
    person_letters = [csv for csv in csv_paths if
                      letter_num_to_key(csv) is not None and letter_map[letter_num_to_key(csv)][0] == person]
    if person_letters:
        aggregate_person(person_letters, person)


def aggregate_year(csv_paths: List[Path], year: int):
    csvs = [read_csv(csv) for csv in csv_paths]
    all_data = aggregate_data(csvs)
    out_path = f"../data/per year/{year}.csv"
    all_data.to_csv(out_path, index=False)


def exec_aggregate_year(csv_paths: List[Path], year: int):
    year_letters = [csv for csv in csv_paths if
                    letter_num_to_key(csv) is not None and letter_map[letter_num_to_key(csv)][2] == year]
    if year_letters:
        aggregate_year(year_letters, year)


def place_is_present(df: DataFrame, place: str):
    return place in df["Place"].values


if __name__ == "__main__":
    # Read in data
    csv_paths = [path for path in Path("../data/per letter").iterdir()]

    # for year in year_set:
    #     exec_aggregate_year(csv_paths, year)

    names = ["Leibnitz", "Sophie"]
    for name in names:
        exec_aggregate_person(name)

    # aggregate_all(csv_paths, "../data/all.csv")
