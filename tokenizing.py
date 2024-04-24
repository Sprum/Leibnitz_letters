import tiktoken

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")


def read_file(doc_path):
    with open(doc_path, "r") as f:
        body = f.read()
    return body

def get_num_tokens(doc_path):
    """
    counts the number of tokens oftext in a given ´txt file
    :param doc_path:
    :return:
    """
    body = read_file(doc_path)
    enc_body = encoding.encode(body)
    num_tokens = len(enc_body)

    return num_tokens


