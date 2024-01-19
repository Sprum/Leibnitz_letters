import os

from tqdm.auto import tqdm
import re

# TODO: missing headings: Seiten, bei denen zwei neue Briefe beginnen → handeln!

Missing_headings = (38, 50, 53, 66, 97, 103, 149, 187, 214, 237, 242, 250, 342)

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


def master_func(book: list):
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
        line = lines[0]
        if not identifier in line:
            print(f"found special page:\n-----\n{line}")
        else:
            # check if two letters on one page
            has_two_letters = re.search(two_letters, line)
            if has_two_letters:
                l1, l2 = has_two_letters.groups()
                print(f"letter1: {l1} | letter2: {l2}")
                # Todo: handle two letters on one page

            # get letter number from header
            substr_idx = line.find(identifier)+len(identifier)
            integers = re.findall(r'\d+', line[substr_idx:substr_idx+4])
            # Convert the matched strings to actual integers
            letter_number = [int(num) for num in integers][0]

            # compare line to state of current letter: number after 'nr. ' substring
            if letter_number > active_letter:   # Page contains a new letter
                active_letter = letter_number
                # handle the first letter
                if letter_number == 1:
                    active_letter_content = page
                    print("Heading: 1. nbla bla")
                else:
                    # detect "idx" of new letter start
                    for i_line in range(1,len(lines)):
                        if lines[i_line].startswith(str(letter_number)):
                            print(f"Heading: {lines[i_line]}")
                    pass
                    # slice page before idx of new letter start
                    # concat page before new letter to page before
                    # add concatted letter before to a list

            else:   # page contains same letter as last page
                # concat current page to active letters content
                active_letter_content += f"\n{page}"



    # if read letter == current letter: concat to page before
    # return list of letters

