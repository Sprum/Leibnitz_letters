from pathlib import Path

import tiktoken
from tqdm import tqdm

encoding_35 = tiktoken.encoding_for_model("gpt-3.5-turbo")
# encoding_4 = tiktoken.encoding_for_model()

def read_file(doc_path: str | Path) -> str:
    with open(doc_path, "r") as f:
        body = f.read()
    return body


def get_num_tokens(body: str) -> int:
    """
    counts the number of tokens oftext in a given ´txt file
    :param doc_path: str
    :return: int
    """

    enc_body = encoding_35.encode(body)
    num_tokens = len(enc_body)

    return num_tokens


if __name__ == "__main__":
    token_len_list = []
    path = Path("letters/cleaned")
    file_list = list(path.iterdir())

    for file in tqdm(file_list, desc="Tokenizing files", unit="file"):
        print(f"processing: {file}")
        if file.is_file():
            body = read_file(file)
            token_len_list.append(get_num_tokens(body))
    print(f"Summe:{sum(token_len_list)}")
    print(max(token_len_list))
