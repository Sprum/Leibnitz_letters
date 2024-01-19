import PyPDF2 as pdf
import spacy

from util import save_pages_to_drive
from tqdm.auto import tqdm

SAVE = True
# pages containing only images etc.
SPECIAL_PAGES = [176, 247, 403, 501, 583]
# load spacy model for NER
nlp = spacy.load('de_core_news_sm')

# read in PDF of book
file = open("Briefwechsel.pdf", "rb")
reader = pdf.PdfReader(file)

# turn Book into a list of pages starting with first letter
book = []

for page in tqdm(range(7, 789)):
    content = reader.pages[page].extract_text()
    book.append(content)

# save pages as txt if SAVE true
if SAVE:
    save_pages_to_drive(book)




