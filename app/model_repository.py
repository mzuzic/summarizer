import spacy
import pytextrank

from app.constants import SPACY_MODEL


nlp = spacy.load(SPACY_MODEL)
nlp.add_pipe("textrank")
