import spacy

from sentence_transformers import SentenceTransformer
from app.constants import SPACY_MODEL, CLAUSE_ENCODER


nlp = spacy.load(SPACY_MODEL)
clause_encoder = SentenceTransformer(CLAUSE_ENCODER)
