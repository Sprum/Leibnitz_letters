import csv
from pathlib import Path

from tokenizing import read_file
import pandas as pd
from util import read_txts
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


if __name__ == "__main__":
    main_func_letters_to_csv()