import os

from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm
import PyPDF2 as pdf

from util import split_into_letters, write_page


def main():
    # read in PDF of book
    file = open("Briefwechsel.pdf", "rb")
    reader = pdf.PdfReader(file)

    # turn Book into a list of pages starting with first letter
    book = []
    # read book into memory
    for page in tqdm(range(7, 789)):
        content = reader.pages[page].extract_text()
        book.append(content)
    # split book into letters
    num_empty_letters = 0
    empty_letters = []
    letters = split_into_letters(book)

    # ask openai to kindly delete the footnotes
    load_dotenv()
    api_key = os.getenv('OPENAI_KEY')
    client = OpenAI(api_key=api_key)
    message_content = letters[1]
    print(message_content)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "you are my assistant. I give you a page of a book containing letters between leibnitz and sophie von Hannover. you will respond with the page i posted to you but you will delete the footnotes."},
            {"role": "user", "content": message_content}
        ]
    )
    print(completion.choices[0].message)


if __name__ == "__main__":
    main()
