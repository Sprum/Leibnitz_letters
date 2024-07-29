from typing import List, Set

import pandas as pd
from pandas import DataFrame

from aggregate.letter_map import water_bodies, rivers, continents, nationalities_ethnicities

# TODO: hier noch mal nachsehen: 1. filter fixen, außerdem vermutlich Greiffenstein nochmal droppen -> always drop in die Filter
def give_coordinates(df: DataFrame, coordinates_data: DataFrame, filters: List[Set]) -> DataFrame:
    """
    function to enrich a specified dataframe with coordinates from another dataframe.
    :param df: Daframe to enrich
    :param coordinates_data: Dataframe with coordinates from another dataframe
    :param filters:
    :return: enriched Dataframe
    """
    filtered_data = filter_out_by_set(df, filters)
    merged_data = pd.merge(filtered_data, coordinates_data, on='Place', how='left')
    return merged_data


def filter_out_by_set(df: DataFrame, filters: List[set]) -> DataFrame:
    """
    Method to filter out entries that are present in a list of sets
    :param df:
    :param filters:
    :return: filtered DataFrame
    """
    filtered_df = df.copy()
    for filter in filters:
        filtered_df = filtered_df[~filtered_df['Place'].isin(filter)]
    return filtered_df


if __name__ == '__main__':
    filters = [water_bodies, rivers, continents, nationalities_ethnicities]
    df = pd.read_csv("../data/all.csv")
    coordinates = pd.read_csv("./coordinates.csv")
    print(len(coordinates))
    merged_coordinates = give_coordinates(df, coordinates, filters)
    print(merged_coordinates[merged_coordinates['lat'].isna()])
