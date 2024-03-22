from util import detect_letter_start
from tqdm.auto import tqdm
import PyPDF2 as pdf
from util import master_func


def main():
    # read in PDF of book
    file = open("Briefwechsel.pdf", "rb")
    reader = pdf.PdfReader(file)

    # turn Book into a list of pages starting with first letter
    book = []

    for page in tqdm(range(7, 789)):
        content = reader.pages[page].extract_text()
        book.append(content)

    letters = master_func(book)
    for key, val in letters.items():

        print(f"{key}: {val}")
if __name__ == "__main__":
    main()
