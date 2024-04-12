from util import detect_letter_start, write_page
from tqdm.auto import tqdm
import PyPDF2 as pdf
from util import split_into_letters


def main():
    # read in PDF of book
    file = open("Briefwechsel.pdf", "rb")
    reader = pdf.PdfReader(file)

    # turn Book into a list of pages starting with first letter
    book = []

    for page in tqdm(range(7, 789)):
        content = reader.pages[page].extract_text()
        book.append(content)
    num_empty_letters = 0
    empty_letters = []
    letters = split_into_letters(book)
    for key, val in letters.items():
        if key == 0:
            pass
        else:
            write_page(val, f"letters/brief_{key}")


if __name__ == "__main__":
    main()
