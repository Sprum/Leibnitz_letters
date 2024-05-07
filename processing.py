from pathlib import Path

from tokenizing import read_file
from util import read_txts
import spacy

nlp =  spacy.load('de_core_news_lg')

def get_entities_letter(letter):
    doc = nlp(letter)
    return doc





"""
NEUER PLAN:

SCheiß drauf :^)
* schauen ob lemmatisierte texte besser gehandelt werden...
* vlt die Texte noch mal richtig cleanen vorher wegen der vielen beschissenen formatierungen in der pdf (danke Merkel) 
"""

if __name__ == "__main__":
    # dir path
    path=Path("letters/cleaned")
    # read_txts
    letter_paths = [i for i in path.iterdir() if i.is_file()]

    ents_loc = {}

    for i in letter_paths:
        letter = read_file(i)
        doc = get_entities_letter(letter)
        for entity in doc.ents:
            if entity.label_ == 'LOC':
                loc = entity
                if ents_loc.get(loc):
                    ents_loc[loc] += 1
                    # LoGIK KAPUTT, SCHREIBT ALLES AUF 0 wahrscheinlich entity.text oder so, naja
                else:
                    ents_loc[loc]= 0


    print(f"unique entities: {len(ents_loc)}")
    print(ents_loc)
