import csv
import re
from collections import defaultdict
from pathlib import Path

from pandas import read_csv

from aggregate.letter_map import places_set
from tokenizing import read_file
import pandas as pd
from util import read_txts, read_text_file, extract_letter_number
import spacy

nlp = spacy.load('de_core_news_lg')


def get_entities_letter(letter):
    doc = nlp(letter)
    return doc


def letter_to_places_dict(letter_path: Path) -> dict:
    ents_letter_loc = {}
    letter_body = read_file(letter_path)
    doc = get_entities_letter(letter_body)
    for entity in doc.ents:
        if entity.label_ == 'LOC':
            loc = entity.text
            if ents_letter_loc.get(loc):
                ents_letter_loc[loc] += 1
            else:
                ents_letter_loc[loc] = 1
    return ents_letter_loc


def data_dict_to_csv(write_path: str, data_dict: dict) -> None:
    """
    Method to make a CSV and write it to specified dir from data dicts.
    :param write_path: The directory path where the CSV file will be saved.
    :param data_dict: The dictionary containing data to be written to the CSV file.
                      It should have a "letter_num" key for the file name and a "data" key which is a list of dictionaries.
    :return: None
    """
    # Construct the file path
    file_path = write_path + data_dict["letter_num"] + ".csv"

    data = data_dict["data"]
    print(file_path, data)
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Place', 'Count'])
    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)


def main_func_letters_to_csv():
    path = Path("letters/cleaned")
    # read_txts
    letter_paths = [i for i in path.iterdir() if i.is_file()]

    letters_data = []

    for letter_path in letter_paths:
        data_dict = {"letter_num": letter_path.name.split(".")[0], "data": None}
        places_dict = letter_to_places_dict(letter_path)
        data_dict["data"] = places_dict

        data_dict_to_csv("./data/", data_dict)

        letters_data.append(data_dict)

    print(letters_data)


def get_unique_entries(df, column_name):
    """
    Returns a set of all unique entries in the specified column of the DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.
    column_name (str): The column name from which to extract unique entries.

    Returns:
    set: A set of unique entries in the specified column.
    """
    if column_name in df.columns:
        unique_entries = set(df[column_name].dropna().unique())
        return unique_entries
    else:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")


def count_substring_occurrences(sub_string, search_string):
    """
    Searches for the given substring in the search string as a regular expression,
    counting occurrences where the substring may have numbers appended to it.

    Args:
        sub_string (str): The substring to search for.
        search_string (str): The string to search within.

    Returns:
        dict: A dictionary with the substring as the key and the count of occurrences as the value.
    """
    # Construct the regular expression pattern
    pattern = rf"{re.escape(sub_string)}\d*"

    # Find all matches in the search string
    matches = re.findall(pattern, search_string)

    # Count the total number of matches
    total_count = len(matches)

    return total_count


def exec_extract_placecount_per_letter():
    paths = [path for path in Path("./letters/cleaned").iterdir()]
    # iter over letters
    for path in paths:
        print("processing:", path)
        letter_num = extract_letter_number(path)
        df_rows = [{"Place": None, "Count": None}]
        searchstr = read_text_file(path)
        # iter over places
        for place in places_set:
            place_count = count_substring_occurrences(place, searchstr)
            if place_count > 0:
                df_rows.append({"Place": place, "Count": place_count})
        df = pd.DataFrame(df_rows)
        df.to_csv(f"./data/per letter/{letter_num}.csv", index=False)


if __name__ == "__main__":
    exec_extract_placecount_per_letter()
