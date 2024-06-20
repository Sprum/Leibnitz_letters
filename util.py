import os
from pathlib import Path
from typing import Dict, List

import pandas as pd
from tqdm.auto import tqdm
import re

Missing_headings = (38, 50, 53, 66, 97, 103, 149, 187, 214, 237, 242, 250, 342)

title_regex = re.compile(r"^\d{2,3}\.", re.IGNORECASE)


def detect_letter_start(text):
    # Regular expression to match lines starting with page number and "nr."

    pattern = re.compile(r'^\d+nr\.\s+[1-9]\d{0,2}.*$')

    # Split the text into lines
    lines = text.split('\n')
    line = lines[0]
    if not "nr." in line:
        return f"special page found:{line[:2]}"
    if "nr. " in line:
        match = pattern.match(line)
        return match
    return False


def save_pages_to_drive(book: list, dir_name: str = "pages"):
    os.makedirs(dir_name, exist_ok=True)
    for i, page in tqdm(enumerate(book)):
        path = f"{dir_name}/page{i}"
        write_page(page, path)


def write_page(txt, path):
    path = path + ".txt"
    with open(path, "w", encoding="utf-8") as t_file:
        t_file.write(txt)


def read_txts(dir):
    for filename in os.listdir(dir):
        # Check if the file has a .txt extension
        if filename.endswith(".txt"):
            filepath = os.path.join(dir, filename)

            # Read lines from the file and append to the list
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()


def check_newline_in_place(df):
    # Check for newline characters in the 'Place' column
    for index, place in df['Place'].items():
        if '\n' in place:
            return True, index, place
    return False, None, None


def split_into_letters(book: list):
    # init letters list and states
    letters = dict()
    active_letter = 0
    active_letter_content = None

    # regex patterns
    identifier = "nr. "
    two_letters = r"(\d+) /(\d+)"

    # iterate over pages in book
    for page in book:
        # detect if special page: !startswith number
        lines = page.split('\n')
        # read first line
        first_line = lines[0]
        if not identifier in first_line:
            print(f"found special page:\n-----\n{first_line}")
        else:
            # check if two letters on one page
            has_two_letters = re.search(two_letters, first_line)
            # if two letters on one page, we need to handle it: we split the page on the headings
            if has_two_letters:
                l1_num, l2_num = has_two_letters.groups()
                print(f"letter1: {l1_num} | letter2: {l2_num}, attempting to find titles:")

                hits = [(idx, match) for idx, s_line in enumerate(lines) if (match := re.search(title_regex, s_line))]
                letter1 = '\n'.join(lines[hits[0][0]:hits[1][0]])
                letter2 = '\n'.join(lines[hits[1][0]:])
                # add letters to dict
                letters[active_letter] = active_letter_content

                letters[int(l1_num)] = letter1
                letters[
                    int(l2_num)] = letter2  # TODO: check if double letters can have second letter span on next page.
                active_letter = int(l2_num)
                active_letter_content = letter2
            # get letter number from header
            substr_idx = first_line.find(identifier) + len(identifier)
            integers = re.findall(r'\d+', first_line[substr_idx:substr_idx + 4])
            # Convert the matched strings to actual integers
            letter_number = [int(num) for num in integers][0]

            # compare line to state of current letter: number after 'nr. ' substring
            if letter_number > active_letter:  # Page contains a new letter
                # if its a new letter, first we need to save the last letter
                letters[active_letter] = active_letter_content

                # handle the first letter
                if letter_number == 1:
                    active_letter = 1
                    active_letter_content = page
                    print("Heading: 1. nbla bla")
                # TODO: findout where to place handling for letter before first letter if two letters hit
                else:
                    # detect "idx" of new letter start
                    for i_line in range(1, len(lines)):
                        if lines[i_line].startswith(str(letter_number)):
                            idx_of_heading = i_line
                            print(f"Heading: {lines[idx_of_heading]}")
                            break
                    # slice page before idx of new letter start
                    # concat page before new letter to page before
                    active_letter_content += f"{''.join(lines[:idx_of_heading])}\n"
                    letters[active_letter] = active_letter_content
                    # then set new letter number as active letter
                    active_letter = letter_number
                    # set new letter content as active letter content
                    active_letter_content = "".join(lines[idx_of_heading:])

            else:  # page contains same letter as last page
                # concat current page to active letters content
                active_letter_content += f"{page}\n"

    comp_list = list(range(0, 382))
    print(comp_list)
    print(list(letters.keys()))
    return letters


def sum_all_places():
    """
    sums up all places per csv so they are unique
    :return:
    """
    print("summing up all places...")
    paths = [path for path in Path("./data/per letter").iterdir()]

    for path in paths:
        df = pd.read_csv(path)
        df = df.groupby('Place', as_index=False)['Count'].sum()
        df.to_csv(path, index=False)

    print("done!")


def search_in_place_column(paths: List[Path], search_str: str) -> Dict[Path, pd.DataFrame]:
    result = {}

    for path in paths:
        df = pd.read_csv(path)

        # Check if 'Place' column exists in the DataFrame
        if 'Place' in df.columns:
            # Filter the DataFrame for rows where 'Place' contains the search string
            filtered_df = df[df['Place'].str.contains(search_str, case=False, na=False)]

            # If there are matching rows, add to the result dictionary
            if not filtered_df.empty:
                result[path] = filtered_df

    return result


def replace_string_in_dataframe(df, old_string, new_string):
    """
    Method to replace
    :param df:
    :param old_string:
    :param new_string:
    :return:
    """
    # Replace occurrences of the old_string with the new_string in the 'Place' column
    df['Place'] = df['Place'].str.replace(old_string, new_string, regex=False)
    return df


def delete_entry(paths: List[Path], search_str: str):
    print(f"deleting '{search_str}'")
    for path in paths:
        df = pd.read_csv(path)
        # Filter out the rows where 'Place' contains the search string
        filtered_df = df[~df['Place'].str.contains(search_str, case=False, na=False)]
        # Save the filtered DataFrame back to the original CSV file
        filtered_df.to_csv(path, index=False)


def rename_entry(paths:  List[Path], search_string: str, new_string: str):
    print(f"renaming {search_string} to {new_string}")
    for path in paths:
        df = pd.read_csv(path)
        df = replace_string_in_dataframe(df, search_string, new_string)
        df.to_csv(path, index=False)


if __name__ == '__main__':
    paths = [path for path in Path("./data/per letter").iterdir()]
    # rename_entry(paths, "Collen", "Köln")
    # sum_all_places()
    delete_entry(paths,"Babylon")