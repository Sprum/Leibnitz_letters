from pathlib import Path

import pandas as pd
from pandas import DataFrame


def compare_places(df1:DataFrame, df2:DataFrame) -> set:
    """
    Compares two DataFrames on the 'Place' column and returns a set of entries
    present in df1 but not in df2.

    Parameters:
    df1 (pd.DataFrame): First DataFrame
    df2 (pd.DataFrame): Second DataFrame

    Returns:
    set: Set of entries in df1 that are not in df2 based on the 'Place' column
    """
    # Ensure the 'Place' column exists in both DataFrames
    if 'Place' not in df1.columns or 'Place' not in df2.columns:
        raise ValueError("Both DataFrames must contain a 'Place' column")

    # Get the unique places from both DataFrames
    places_df1 = set(df1['Place'])
    places_df2 = set(df2['Place'])

    # Find places that are in df1 but not in df2
    difference = places_df1 - places_df2

    return difference


def compare_counts(df1, df2):
    """
    Compares two DataFrames on the 'Place' and 'Count' columns and returns a dictionary
    indicating which DataFrame has the higher count for each unique place.

    Parameters:
    df1 (pd.DataFrame): First DataFrame with 'Place' and 'Count' columns
    df2 (pd.DataFrame): Second DataFrame with 'Place' and 'Count' columns

    Returns:
    dict: A dictionary where the keys are places and the values indicate which DataFrame
          has the higher count for that place.
    """
    # Ensure the 'Place' and 'Count' columns exist in both DataFrames
    if 'Place' not in df1.columns or 'Count' not in df1.columns:
        raise ValueError("df1 must contain 'Place' and 'Count' columns")
    if 'Place' not in df2.columns or 'Count' not in df2.columns:
        raise ValueError("df2 must contain 'Place' and 'Count' columns")

    # Merge the two DataFrames on the 'Place' column
    merged_df = pd.merge(df1, df2, on='Place', how='outer', suffixes=('_df1', '_df2'))

    # Initialize an empty dictionary to store the results
    result = {}

    # Iterate through each row in the merged DataFrame
    for _, row in merged_df.iterrows():
        place = row['Place']
        count_df1 = row['Count_df1'] if pd.notna(row['Count_df1']) else 0
        count_df2 = row['Count_df2'] if pd.notna(row['Count_df2']) else 0

        if count_df1 > count_df2:
            result[place] = 'df1'
        elif count_df2 > count_df1:
            result[place] = 'df2'
        else:
            result[place] = 'equal'

    return result




if __name__ == '__main__':
    df1s = [path for path in Path("../data/archive/per letter").iterdir()]
    df2s = [path for path in Path("../data/archive/per letter old").iterdir()]
    for i in range(len(df1s)):
        df1 = pd.read_csv(df1s[i])
        df2 = pd.read_csv(df2s[i])

        differences = compare_counts(df1,df2)
        print(differences)