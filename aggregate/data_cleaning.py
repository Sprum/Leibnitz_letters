from pathlib import Path

import pandas as pd
from pandas import DataFrame


def merge_with_max_counts(df1:DataFrame, df2:DataFrame):
    """
    Merges two DataFrames on the 'Place' column and returns a new DataFrame with
    all unique places and the highest counts from either DataFrame.

    Parameters:
    df1 (pd.DataFrame): First DataFrame with 'Place' and 'Count' columns
    df2 (pd.DataFrame): Second DataFrame with 'Place' and 'Count' columns

    Returns:
    pd.DataFrame: A new DataFrame with all unique places and the highest counts
                  from either DataFrame.
    """
    # Ensure the 'Place' and 'Count' columns exist in both DataFrames
    if 'Place' not in df1.columns or 'Count' not in df1.columns:
        raise ValueError("df1 must contain 'Place' and 'Count' columns")
    if 'Place' not in df2.columns or 'Count' not in df2.columns:
        raise ValueError("df2 must contain 'Place' and 'Count' columns")

    # Merge the two DataFrames on the 'Place' column
    merged_df = pd.merge(df1, df2, on='Place', how='outer', suffixes=('_df1', '_df2'))

    # Initialize lists to store the places and their maximum counts
    places = []
    max_counts = []

    # Iterate through each row in the merged DataFrame
    for _, row in merged_df.iterrows():
        place = row['Place']
        count_df1 = row['Count_df1'] if pd.notna(row['Count_df1']) else 0
        count_df2 = row['Count_df2'] if pd.notna(row['Count_df2']) else 0

        # Append the place and the maximum count to the respective lists
        places.append(place)
        max_counts.append(max(count_df1, count_df2))

    # Create a new DataFrame with the places and their maximum counts
    result_df = pd.DataFrame({
        'Place': places,
        'Count': max_counts
    })

    return result_df


def clean_dataframe(df):
    """
    Cleans a DataFrame by dropping all rows with NA values, dropping rows that
    contain only a comma (","), and converting 'Count' column values to integers if they are floats.

    Parameters:
    df (pd.DataFrame): The input DataFrame to be cleaned

    Returns:
    pd.DataFrame: The cleaned DataFrame
    """
    # Drop all rows with NA values
    df_cleaned = df.dropna()

    # Drop rows that contain only a comma (",") in any column
    df_cleaned = df_cleaned[~df_cleaned.apply(lambda row: row.astype(str).str.strip().eq(',').any(), axis=1)]

    # Convert 'Count' column values to integers if they are floats
    if 'Count' in df_cleaned.columns:
        df_cleaned['Count'] = df_cleaned['Count'].astype(float).astype(int)

    return df_cleaned

if __name__ == '__main__':
    paths = [path for path in Path("../data/archive/per letter").iterdir()]
    for path in paths:
        df = pd.read_csv(path)
        cleaned_df = clean_dataframe(df)
        cleaned_df.to_csv(path, index=False)
